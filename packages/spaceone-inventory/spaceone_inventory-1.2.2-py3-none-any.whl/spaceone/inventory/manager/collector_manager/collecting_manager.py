# -*- coding: utf-8 -*-

import logging
import json
import time

from google.protobuf.json_format import MessageToDict

from spaceone.core import config, cache
from spaceone.core import queue
from spaceone.core.error import *
from spaceone.core.manager import BaseManager
from spaceone.inventory.error import *
from spaceone.inventory.lib import rule_matcher

_LOGGER = logging.getLogger(__name__)

######################################################################
#    ************ Very Important ************
#
# This is resource map for collector
# If you add new service and manager for specific RESOURCE_TYPE,
# add here for collector
######################################################################
RESOURCE_MAP = {
    'SERVER': 'ServerManager',
    'NETWORK': 'NetworkManager',
    'NETWORK_POLICY': 'NetworkPolicyManager',
    'SUBNET': 'SubnetManager',
    'CLOUD_SERVICE': 'CloudServiceManager',
    'CLOUD_SERVICE_TYPE': 'CloudServiceTypeManager',
    'inventory.Server': 'ServerManager',
    'inventory.FilterCache': 'FilterManager',
    'inventory.CloudService': 'CloudServiceManager',
    'inventory.CloudServiceType': 'CloudServiceTypeManager',
    'inventory.Region': 'RegionManager',
}

SERVICE_MAP = {
    'SERVER': 'ServerService',
    'NETWORK': 'NetworkService',
    'NETWORK_POLICY': 'NetworkService',
    'SUBNET': 'NetworkService',
    'CLOUD_SERVICE': 'CloudServiceService',
    'CLOUD_SERVICE_TYPE': 'CloudServiceTypeService',
    'inventory.Server': 'ServerService',
    'inventory.FilterCache': 'CollectorService',
    'inventory.CloudService': 'CloudServiceService',
    'inventory.CloudServiceType': 'CloudServiceTypeService',
    'inventory.Region': 'RegionService',
}

DB_QUEUE_NAME = 'db_q'
CREATED = 1
UPDATED = 2
ERROR = 3

#################################################
# Collecting Resource and Update DB
#################################################
class CollectingManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret = None      # secret info for update meta
        self.initialize()

    def initialize(self):
        _LOGGER.debug(f'[initialize] initialize Worker configuration')
        queues = config.get_global('QUEUES')
        if DB_QUEUE_NAME in queues:
            self.use_db_queue = True
            self.db_queue = DB_QUEUE_NAME
        else:
            self.use_db_queue = False
        _LOGGER.debug(f'[initialize] use db_queue: {self.use_db_queue}')

    ##########################################################
    # collect
    #
    # links: https://pyengine.atlassian.net/wiki/spaces/CLOUD/pages/682459145/3.+Collector+Rule+Management
    #
    ##########################################################
    def collecting_resources(self, plugin_info, secret_id, filters, domain_id, **kwargs):
        """ This is single call of real plugin with endpoint

        All parameter should be primitive type(Json), not object.
        Because this method will be executed by worker.
        Args:
            plugin_info(dict)
            kwargs: {
                'job_id': 'str',
                'use_cache': bool
            }
        """

        # Check Job State first, if job state is canceled, stop process
        job_mgr = self.locator.get_manager('JobManager')
        job_task_mgr = self.locator.get_manager('JobTaskManager')

        job_task_id = kwargs['job_task_id']

        job_id = kwargs['job_id']
        job_vo = job_mgr.get(job_id, domain_id)
        if job_mgr.should_cancel(job_id, domain_id):
            job_mgr.decrease_remained_tasks(job_id, domain_id)
            self._update_job_task(job_task_id, 'FAILURE', domain_id)
            raise ERROR_COLLECT_CANCELED(job_id=job_id)

        # Create proper connector
        connector = self._get_connector(plugin_info, domain_id)

        collect_filter = filters
        try:
            # use_cache
            use_cache = kwargs['use_cache']
            if use_cache:
                key = f'collector-filter:{kwargs["collector_id"]}:{secret_id}'
                value = cache.get(key)
                _LOGGER.debug(f'[collecting_resources] cache -> {key}: {value}')
                if value:
                    collect_filter.update(value)
            else:
                _LOGGER.debug(f'[collecting_resources] no cache mode')

        except Exception as e:
            _LOGGER.debug(f'[collecting_resources] cache error,{e}')

        try:
            secret_mgr = self.locator.get_manager('SecretManager')
            secret_data = secret_mgr.get_secret_data(secret_id, domain_id)
            self.secret = secret_mgr.get_secret(secret_id, domain_id)

        except ERROR_BASE as e:
            _LOGGER.error(f'[collecting_resources] fail to get secret_data: {secret_id}')
            job_task_mgr.add_error(job_task_id, domain_id,
                                   e.error_code,
                                   e.message,
                                   {'resource_type': 'secret.Secret', 'resource_id': secret_id}
                                   )
            job_mgr.decrease_remained_tasks(job_id, domain_id)
            raise ERROR_COLLECTOR_SECRET(plugin_info=plugin_info, param=secret_id)


        except Exception as e:
            _LOGGER.error(f'[collecting_resources] fail to get secret_data: {secret_id}')
            job_task_mgr.add_error(job_task_id, domain_id,
                                   'ERROR_COLLECTOR_SECRET',
                                   e,
                                   {'resource_type': 'secret.Secret', 'resource_id': secret_id}
                                   )
            job_mgr.decrease_remained_tasks(job_id, domain_id)
            raise ERROR_COLLECTOR_SECRET(plugin_info=plugin_info, param=secret_id)

        try:
            # Update JobTask (In-progress)
            self._update_job_task(job_task_id, 'IN_PROGRESS', domain_id, secret=self.secret)
        except Exception as e:
            _LOGGER.error(f'[collecing_resources] fail to update job_task: {e}')

        ##########################################################
        # Call method
        ##########################################################
        try:
            _LOGGER.debug('[collect] Before call collect')
            results = connector.collect(plugin_info['options'], secret_data.data, collect_filter)
            _LOGGER.debug('[collect] generator: %s' % results)

        except ERROR_BASE as e:
            _LOGGER.error(f'[collecting_resources] fail to get secret_data: {secret_id}')
            job_task_mgr.add_error(job_task_id, domain_id,
                                   e.error_code,
                                   e.message,
                                   {'resource_type': 'secret.Secret', 'resource_id': secret_id}
                                   )
            job_mgr.decrease_remained_tasks(job_id, domain_id)
            raise ERROR_COLLECTOR_COLLECTING(plugin_info=plugin_info, filters=collect_filter)

        except Exception as e:
            job_task_mgr.add_error(job_task_id, domain_id,
                                   'ERROR_COLLECTOR_COLLECTING',
                                   e,
                                   {'resource_type': 'secret.Secret', 'resource_id': secret_id}
                                   )
            job_mgr.decrease_remained_tasks(job_id, domain_id)
            raise ERROR_COLLECTOR_COLLECTING(plugin_info=plugin_info, filters=collect_filter)

        ##############################################################
        # Processing Result
        # Type 1: use_db_queue == False, processing synchronously
        # Type 2: use_db_queue == True, processing asynchronously
        ##############################################################
        try:
            stat = self._process_results(results,
                                  job_id,
                                  job_task_id,
                                  kwargs['collector_id'],
                                  secret_id,
                                  domain_id
                                  )
            if stat['failure_count'] > 0:
                JOB_TASK_STATE = 'FAILURE'
            else:
                JOB_TASK_STATE = 'SUCCESS'
            # Update Statistics of JobTask
            self._update_job_task(job_task_id, JOB_TASK_STATE, domain_id, stat=stat)

        except ERROR_BASE as e:
            _LOGGER.error(f'[collecting_resources] {e}')
            job_task_mgr.add_error(job_task_id, domain_id,
                                   e.error_code,
                                   e.message,
                                   {'resource_type': 'secret.Secret', 'resource_id': secret_id}
                                   )
            self._update_job_task(job_task_id, 'FAILURE', domain_id)

        except Exception as e:
            _LOGGER.error(f'[collecting_resources] {e}')
            job_task_mgr.add_error(job_task_id, domain_id,
                                   'ERROR_COLLECTOR_COLLECTING',
                                   e,
                                   {'resource_type': 'secret.Secret', 'resource_id': secret_id}
                                   )
            self._update_job_task(job_task_id, 'FAILURE', domain_id)

        finally:
            job_mgr.decrease_remained_tasks(kwargs['job_id'], domain_id)

        return True

    def _process_results(self, results, job_id, job_task_id, collector_id, secret_id, domain_id):
        # update meta
        self.transaction.set_meta('job_id', job_id)
        self.transaction.set_meta('job_task_id', job_task_id)
        self.transaction.set_meta('collector_id', collector_id)
        self.transaction.set_meta('secret.secret_id', secret_id)
        if 'provider' in self.secret:
            self.transaction.set_meta('secret.provider', self.secret['provider'])
        if 'project_id' in self.secret:
            self.transaction.set_meta('secret.project_id', self.secret['project_id'])
        if 'service_account_id' in self.secret:
            self.transaction.set_meta('secret.service_account_id', self.secret['service_account_id'])

        created = 0
        updated = 0
        failure = 0

        idx = 0
        for res in results:
            try:
                params = {
                    'domain_id': domain_id,
                    'job_id': job_id,
                    'job_task_id': job_task_id,
                    'collector_id': collector_id,
                    'secret_id': secret_id
                }
                res_dict = MessageToDict(res, preserving_proto_field_name=True)

                idx += 1
                ######################################
                # Asynchronous DB Updater (using Queue)
                ######################################
                if self.use_db_queue:
                    _LOGGER.debug(f'[_process_results] use db queue: {idx}')
                    # Create Asynchronus Task
                    pushed = self._create_db_update_task(res_dict, params)
                    if pushed == False:
                        failure += 1
                    continue

                #####################################
                # Synchrous Update
                # If you here, processing in worker
                #####################################
                res_state = self._process_single_result(res_dict, params)
                if res_state == 1:
                    created += 1
                elif res_state == 2:
                    updated += 1
                else:
                    failure += 1

            except Exception as e:
                _LOGGER.error(f'[_process_results] failed single result {e}')

        # Update JobTask
        return {
            'total_count': idx,
            'created_count': created,
            'updated_count': updated,
            'failure_count': failure
        }

    def _process_single_result(self, resource, params):
        """ Process single resource (Add/Update)
            Args:
                resource (message_dict): resource from collector
                params (dict): {
                    'domain_id': 'str',
                    'job_id': 'str',
                    'job_task_id': 'str',
                    'collector_id': 'str',
                    'secret_id': 'str'
                }
            Returns:
                1: created
                2: updated
                3: error
        """
        # update meta
        domain_id = params['domain_id']
        resource_type = resource['resource_type']
        data = resource['resource']

        _LOGGER.debug(f'[_process_single_result] {resource_type}')
        (svc, mgr) = self._get_resource_map(resource_type)

        # FiterCache
        if resource_type == 'inventory.FilterCache' or resource_type == 'FILTER_CACHE':
            return mgr.cache_filter(params['collector_id'],
                                    params['secret_id'],
                                    data)

        data['domain_id'] = domain_id
        # General Resource like Server, CloudService
        match_rules = resource.get('match_rules', {})
        ##################################
        # Match rules
        ##################################
        start = time.time()
        try:
            res_info, total_count = self._query_with_match_rules(data,
                                                                 match_rules,
                                                                 domain_id,
                                                                 mgr
                                                                 )
            _LOGGER.debug(f'[_process_single_result] matched resources count = {total_count}')
        except Exception as e:
            _LOGGER.error(f'[_process_single_result] failed to match: {e}')
            _LOGGER.warning(f'[_process_single_result] assume new resource, create')
            total_count = 0

        end = time.time()
        diff = end - start
        _LOGGER.error(f'query time: {diff}')

        #########################################
        # Create / Update to DB
        #########################################
        response = ERROR
        res_id = "Unknown"
        try:
            job_id = params['job_id']
            job_task_id = params['job_task_id']
            # For book-keeping
            if total_count == 0:
                # Create
                res_msg = svc.create(data)
                diff = time.time() - end
                _LOGGER.error(f'insert: {diff}')
                response = CREATED

            elif total_count == 1:
                # Update
                data.update(res_info[0])
                res_msg = svc.update(data)
                diff = time.time() - end
                _LOGGER.error(f'update: {diff}')
                response = UPDATED

            elif total_count > 1:
                # Ambiguous
                # TODO: duplicate
                _LOGGER.debug(f'[_process_single_result] Too many resources matched. (count={total_count})')
                _LOGGER.warning(f'[_process_single_result] match_rules: {match_rules}')
                response = ERROR

        except ERROR_BASE as e:
            job_task_mgr = self.locator.get_manager('JobTaskManager')
            job_task_mgr.add_error(job_task_id, domain_id,
                                   e.error_code,
                                   e.message,
                                   {'resource_type': resource_type, 'resource_id': res_id}
                                   )

        except Exception as e:
            # TODO: create error message
            _LOGGER.debug(f'[_process_single_result] service error: {svc}, {e}')
            response = ERROR
        finally:
            # Update statistics
            return RESPONSE

    def _get_resource_map(self, resource_type):
        """ Base on resource type

        Returns: (service, manager)
        """
        if resource_type not in RESOURCE_MAP:
            raise ERROR_UNSUPPORTED_RESOURCE_TYPE(resource_type=resource_type)
        if resource_type not in SERVICE_MAP:
            raise ERROR_UNSUPPORTED_RESOURCE_TYPE(resource_type=resource_type)

        # Get proper manager
        # Create new manager or service, since transaction is variable
        svc = self.locator.get_service(SERVICE_MAP[resource_type], metadata=self.transaction.meta)
        mgr = self.locator.get_manager(RESOURCE_MAP[resource_type])
        return (svc, mgr)

    def _update_job_task(self, job_task_id, state, domain_id, secret=None, stat=None):
        """ Update JobTask
        - state (Pending -> In-progress)
        - started_time
        - secret_info
        """
        job_task_mgr = self.locator.get_manager('JobTaskManager')

        # Update Secret also
        secret_info = None
        if secret:
            secret_info = {
                'secret_id': secret['secret_id']
            }
            provider = secret.get('provider', None)
            service_account_id = secret.get('service_account_id', None)
            project_id = secret.get('project_id', None)
            if provider:
                secret_info.update({'provider': provider})
            if service_account_id:
                secret_info.update({'service_account_id': service_account_id})
            if project_id:
                secret_info.update({'project_id': project_id})
            _LOGGER.debug(f'[_update_job_task] secret_info: {secret_info}')

        if state == 'IN_PROGRESS':
            job_task_mgr.make_inprogress(job_task_id, domain_id, secret_info, stat)
        elif state == 'SUCCESS':
            job_task_mgr.make_success(job_task_id, domain_id, secret_info, stat)
        elif state == 'FAILURE':
            job_task_mgr.make_failure(job_task_id, domain_id, secret_info, stat)
        else:
            _LOGGER.error(f'[_update_job_task] undefined state: {state}')
            job_task_mgr.make_failure(job_task_id, domain_id, secret_info, stat)


    ######################
    # Internal
    ######################
    def _get_connector(self, plugin_info, domain_id, **kwargs):
        """ Find proper connector(plugin)

        Returns: connector (object)
        """
        connector = self.locator.get_connector('CollectorPluginConnector')
        # get endpoint
        endpoint = self._get_endpoint(plugin_info, domain_id)
        _LOGGER.debug('[collect] endpoint: %s' % endpoint)
        connector.initialize(endpoint)

        return connector

    def _get_endpoint(self, plugin_info, domain_id):
        """ get endpoint from plugin_info

        Args:
            plugin_info (dict) : {
                'plugin_id': 'str',
                'version': 'str',
                'options': 'dict',
                'secret_id': 'str',
                'secret_group_id': 'str',
                'provider': 'str',
                'capabilities': 'dict'
                }
            domain_id (str)

        Returns: Endpoint Object

        """
        # Call Plugin Service
        plugin_id = plugin_info['plugin_id']
        version = plugin_info['version']

        plugin_connector = self.locator.get_connector('PluginConnector')
        # TODO: label match

        endpoint = plugin_connector.get_plugin_endpoint(plugin_id, version, domain_id)
        return endpoint

    def _query_with_match_rules(self, resource, match_rules, domain_id, mgr):
        """ match resource based on match_rules

        Args:
            resource: ResourceInfo(Json) from collector plugin
            match_rules:
                ex) {1:['data.vm.vm_id'], 2:['zone_id', 'data.ip_addresses']}

        Return:
            resource_id : resource_id for resource update (ex. {'server_id': 'server-xxxxxx'})
            True: can not determine resources (ambiguous)
            False: no matched
        """

        found_resource = None
        total_count = 0

        match_rules = rule_matcher.dict_key_int_parser(match_rules)

        match_order = match_rules.keys()

        for order in sorted(match_order):
            query = rule_matcher.make_query(order, match_rules, resource, domain_id)
            _LOGGER.debug(f'[_query_with_match_rules] query generated: {query}')
            found_resource, total_count = mgr.find_resources(query)
            if found_resource and total_count == 1:
                return found_resource, total_count

        return found_resource, total_count

    ########################
    # Asynchronous DB Update
    ########################
    def _create_db_update_task(self, res, param):
        """ Create Asynchronous Task
        """
        try:
            # Push Queue
            task = {'res': res, 'param': param, 'meta': self.transaction.meta}
            json_task = json.dumps(task)
            queue.put(self.db_queue, json_task)
            return True
        except Exception as e:
            _LOGGER.error(f'[_create_db_update_task] {e}')
            return False


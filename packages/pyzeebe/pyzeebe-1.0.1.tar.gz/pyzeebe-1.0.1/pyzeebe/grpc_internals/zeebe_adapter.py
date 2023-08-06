import json
import logging
import os.path
from typing import List, Generator, Dict

import grpc

from pyzeebe.grpc_internals.zeebe_pb2 import *
from pyzeebe.grpc_internals.zeebe_pb2_grpc import GatewayStub
from pyzeebe.task.task_context import TaskContext


class ZeebeAdapter:
    def __init__(self, hostname: str = None, port: int = None, channel: grpc.Channel = None, **kwargs):
        self._connection_uri = f'{hostname}:{port}' or os.getenv('ZEEBE_ADDRESS') or 'localhost:26500'
        if channel:
            self._channel = channel
        else:
            if hostname or port:
                self._connection_uri = f'{hostname or "localhost"}:{port or 26500}'
            else:
                self._connection_uri = os.getenv('ZEEBE_ADDRESS') or 'localhost:26500'
            self._channel = grpc.insecure_channel(self._connection_uri)

        self.connected = False
        self.retrying_connection = True
        self._channel.subscribe(self._check_connectivity, try_to_connect=True)
        self.gateway_stub = GatewayStub(self._channel)

    def _check_connectivity(self, value: grpc.ChannelConnectivity) -> None:
        logging.debug(f'Grpc channel connectivity changed to: {value}')
        if value in [grpc.ChannelConnectivity.READY, grpc.ChannelConnectivity.IDLE]:
            logging.debug('Connected to Zeebe')
            self.connected = True
            self.retrying_connection = False
        elif value in [grpc.ChannelConnectivity.CONNECTING, grpc.ChannelConnectivity.TRANSIENT_FAILURE]:
            logging.warning('No connection to Zeebe, recoverable. Reconnecting...')
            self.connected = False
            self.retrying_connection = True
        elif value == grpc.ChannelConnectivity.SHUTDOWN:
            logging.error('Failed to establish connection to Zeebe. Non recoverable')
            self.connected = False
            self.retrying_connection = False
            raise ConnectionAbortedError(f'Lost connection to {self._connection_uri}')

    def activate_jobs(self, task_type: str, worker: str, timeout: int, max_jobs_to_activate: int,
                      variables_to_fetch: List[str], request_timeout: int) -> Generator[TaskContext, None, None]:
        for response in self.gateway_stub.ActivateJobs(
                ActivateJobsRequest(type=task_type, worker=worker, timeout=timeout,
                                    maxJobsToActivate=max_jobs_to_activate,
                                    fetchVariable=variables_to_fetch, requestTimeout=request_timeout)):
            for job in response.jobs:
                context = self._create_task_context_from_job(job)
                logging.debug(f'Got job: {context} from zeebe')
                yield context

    @staticmethod
    def _create_task_context_from_job(job) -> TaskContext:
        return TaskContext(key=job.key, _type=job.type,
                           workflow_instance_key=job.workflowInstanceKey,
                           bpmn_process_id=job.bpmnProcessId,
                           workflow_definition_version=job.workflowDefinitionVersion,
                           workflow_key=job.workflowKey,
                           element_id=job.elementId,
                           element_instance_key=job.elementInstanceKey,
                           custom_headers=json.loads(job.customHeaders),
                           worker=job.worker,
                           retries=job.retries,
                           deadline=job.deadline,
                           variables=json.loads(job.variables))

    def complete_job(self, job_key: int, variables: Dict) -> CompleteJobResponse:
        return self.gateway_stub.CompleteJob(CompleteJobRequest(jobKey=job_key, variables=json.dumps(variables)))

    def fail_job(self, job_key: int, message: str) -> FailJobResponse:
        return self.gateway_stub.FailJob(FailJobRequest(jobKey=job_key, errorMessage=message))

    def throw_error(self, job_key: int, message: str) -> ThrowErrorResponse:
        return self.gateway_stub.ThrowError(
            ThrowErrorRequest(jobKey=job_key, errorMessage=message))

    def create_workflow_instance(self, bpmn_process_id: str, version: int, variables: Dict) -> str:
        response = self.gateway_stub.CreateWorkflowInstance(
            CreateWorkflowInstanceRequest(bpmnProcessId=bpmn_process_id, version=version,
                                          variables=json.dumps(variables)))
        return response.workflowInstanceKey

    def create_workflow_instance_with_result(self, bpmn_process_id: str, version: int, variables: Dict,
                                             timeout: int, variables_to_fetch) -> Dict:
        response = self.gateway_stub.CreateWorkflowInstanceWithResult(
            CreateWorkflowInstanceWithResultRequest(
                request=CreateWorkflowInstanceRequest(bpmnProcessId=bpmn_process_id, version=version,
                                                      variables=json.dumps(variables)),
                requestTimeout=timeout, fetchVariables=variables_to_fetch))
        return json.loads(response.variables)

    def publish_message(self, name: str, correlation_key: str, time_to_live_in_milliseconds: int,
                        variables: Dict) -> PublishMessageResponse:
        return self.gateway_stub.PublishMessage(
            PublishMessageRequest(name=name, correlationKey=correlation_key, timeToLive=time_to_live_in_milliseconds,
                                  variables=json.dumps(variables)))

    def deploy_workflow(self, *workflow_file_path: str) -> DeployWorkflowResponse:
        return self.gateway_stub.DeployWorkflow(
            DeployWorkflowRequest(workflows=map(self._get_workflow_request_object, workflow_file_path)))

    @staticmethod
    def _get_workflow_request_object(workflow_file_path: str) -> WorkflowRequestObject:
        return WorkflowRequestObject(name=os.path.split(workflow_file_path)[-1],
                                     definition=open(workflow_file_path).read())

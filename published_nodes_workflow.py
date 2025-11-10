# /// script
# dependencies = []
# 
# [tool.griptape-nodes]
# name = "simple_published_workflow"
# schema_version = "0.13.0"
# engine_version_created_with = "0.62.0"
# node_libraries_referenced = [["Griptape Nodes Library", "0.50.0"]]
# node_types_used = [["Griptape Nodes Library", "Agent"], ["Griptape Nodes Library", "EndFlow"], ["Griptape Nodes Library", "StartFlow"]]
# is_griptape_provided = false
# is_template = false
# creation_date = 2025-11-10T20:54:47.009680Z
# last_modified_date = 2025-11-10T22:26:32.753052Z
# workflow_shape = "{\"inputs\":{\"Start Flow\":{\"execution_environment\":{\"name\":\"execution_environment\",\"tooltip\":\"Environment that the node should execute in\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":\"Local Execution\",\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"simple_dropdown\":[\"Local Execution\",\"Private Execution\",\"AWS Deadline Cloud Library\",\"Griptape Cloud Library\"],\"show_search\":true,\"search_filter\":\"\",\"hide\":true},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"job_group\":{\"name\":\"job_group\",\"tooltip\":\"Groupings of multiple nodes to send up as a Deadline Cloud job.\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":\"\",\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"hide\":true},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"exec_out\":{\"name\":\"exec_out\",\"tooltip\":\"Connection to the next node in the execution chain\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Flow Out\"},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"prompt\":{\"name\":\"prompt\",\"tooltip\":\"New parameter\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":\"\",\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"multiline\":true,\"placeholder_text\":\"Talk with the Agent.\",\"is_custom\":true,\"is_user_added\":true},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":\"\",\"parent_element_name\":null}}},\"outputs\":{\"End Flow\":{\"execution_environment\":{\"name\":\"execution_environment\",\"tooltip\":\"Environment that the node should execute in\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":\"Local Execution\",\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"simple_dropdown\":[\"Local Execution\",\"Private Execution\",\"AWS Deadline Cloud Library\",\"Griptape Cloud Library\"],\"show_search\":true,\"search_filter\":\"\",\"hide\":true},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"job_group\":{\"name\":\"job_group\",\"tooltip\":\"Groupings of multiple nodes to send up as a Deadline Cloud job.\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":\"\",\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"hide\":true},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"exec_in\":{\"name\":\"exec_in\",\"tooltip\":\"Control path when the flow completed successfully\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Succeeded\"},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"failed\":{\"name\":\"failed\",\"tooltip\":\"Control path when the flow failed\",\"type\":\"parametercontroltype\",\"input_types\":[\"parametercontroltype\"],\"output_type\":\"parametercontroltype\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"display_name\":\"Failed\"},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"was_successful\":{\"name\":\"was_successful\",\"tooltip\":\"Indicates whether it completed without errors.\",\"type\":\"bool\",\"input_types\":[\"bool\"],\"output_type\":\"bool\",\"default_value\":false,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{},\"settable\":false,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"result_details\":{\"name\":\"result_details\",\"tooltip\":\"Details about the operation result\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":null,\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"multiline\":true,\"placeholder_text\":\"Details about the completion or failure will be shown here.\"},\"settable\":false,\"is_user_defined\":true,\"parent_container_name\":null,\"parent_element_name\":null},\"output\":{\"name\":\"output\",\"tooltip\":\"New parameter\",\"type\":\"str\",\"input_types\":[\"str\"],\"output_type\":\"str\",\"default_value\":\"\",\"tooltip_as_input\":null,\"tooltip_as_property\":null,\"tooltip_as_output\":null,\"ui_options\":{\"multiline\":true,\"placeholder_text\":\"Agent response\",\"markdown\":false,\"is_custom\":true,\"is_user_added\":true},\"settable\":true,\"is_user_defined\":true,\"parent_container_name\":\"\",\"parent_element_name\":null}}}}"
# 
# ///

import argparse
import asyncio
import json
import pickle
from griptape_nodes.bootstrap.workflow_executors.local_workflow_executor import LocalWorkflowExecutor
from griptape_nodes.bootstrap.workflow_executors.workflow_executor import WorkflowExecutor
from griptape_nodes.drivers.storage.storage_backend import StorageBackend
from griptape_nodes.node_library.library_registry import IconVariant, NodeDeprecationMetadata, NodeMetadata
from griptape_nodes.retained_mode.events.connection_events import CreateConnectionRequest
from griptape_nodes.retained_mode.events.flow_events import CreateFlowRequest, GetTopLevelFlowRequest, GetTopLevelFlowResultSuccess
from griptape_nodes.retained_mode.events.library_events import LoadLibrariesRequest
from griptape_nodes.retained_mode.events.node_events import CreateNodeRequest
from griptape_nodes.retained_mode.events.parameter_events import AddParameterToNodeRequest, AlterParameterDetailsRequest, SetParameterValueRequest
from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes

GriptapeNodes.handle_request(LoadLibrariesRequest())

context_manager = GriptapeNodes.ContextManager()

if not context_manager.has_current_workflow():
    context_manager.push_workflow(workflow_name='simple_published_workflow')

"""
1. We've collated all of the unique parameter values into a dictionary so that we do not have to duplicate them.
   This minimizes the size of the code, especially for large objects like serialized image files.
2. We're using a prefix so that it's clear which Flow these values are associated with.
3. The values are serialized using pickle, which is a binary format. This makes them harder to read, but makes
   them consistently save and load. It allows us to serialize complex objects like custom classes, which otherwise
   would be difficult to serialize.
"""
top_level_unique_values_dict = {'25cb62ab-365b-42c9-ae07-a0fe7915c079': pickle.loads(b'\x80\x04\x95\n\x00\x00\x00\x00\x00\x00\x00\x8c\x06Say hi\x94.')}

'# Create the Flow, then do work within it as context.'

flow0_name = GriptapeNodes.handle_request(CreateFlowRequest(parent_flow_name=None, set_as_new_context=False, metadata={})).flow_name

with GriptapeNodes.ContextManager().flow(flow0_name):
    node0_name = GriptapeNodes.handle_request(CreateNodeRequest(node_type='StartFlow', specific_library_name='Griptape Nodes Library', node_name='Start Flow', metadata={'position': {'x': -6009.690032360479, 'y': -819.4184844577405}, 'tempId': 'placing-1762808098661-fd71', 'library_node_metadata': NodeMetadata(category='workflows', description='Define the start of a workflow and pass parameters into the flow', display_name='Start Flow', tags=None, icon=None, color=None, group='create', deprecation=None), 'library': 'Griptape Nodes Library', 'node_type': 'StartFlow', 'showaddparameter': True, 'size': {'width': 600, 'height': 293}}, initial_setup=True)).node_name
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(AddParameterToNodeRequest(parameter_name='prompt', default_value='', tooltip='New parameter', type='str', input_types=['str'], output_type='str', ui_options={'multiline': True, 'placeholder_text': 'Talk with the Agent.', 'is_custom': True, 'is_user_added': True}, mode_allowed_input=True, mode_allowed_property=True, mode_allowed_output=True, parent_container_name='', initial_setup=True))
    node1_name = GriptapeNodes.handle_request(CreateNodeRequest(node_type='EndFlow', specific_library_name='Griptape Nodes Library', node_name='End Flow', metadata={'position': {'x': -3542.0584674092906, 'y': -819.4184844577405}, 'tempId': 'placing-1762808103838-qbemy', 'library_node_metadata': NodeMetadata(category='workflows', description='Define the end of a workflow and return parameters from the flow', display_name='End Flow', tags=None, icon=None, color=None, group='create', deprecation=None), 'library': 'Griptape Nodes Library', 'node_type': 'EndFlow', 'showaddparameter': True, 'size': {'width': 640, 'height': 623}, 'category': 'workflows'}, initial_setup=True)).node_name
    with GriptapeNodes.ContextManager().node(node1_name):
        GriptapeNodes.handle_request(AddParameterToNodeRequest(parameter_name='output', default_value='', tooltip='New parameter', type='str', input_types=['str'], output_type='str', ui_options={'multiline': True, 'placeholder_text': 'Agent response', 'markdown': False, 'is_custom': True, 'is_user_added': True}, mode_allowed_input=True, mode_allowed_property=True, mode_allowed_output=True, parent_container_name='', initial_setup=True))
    node2_name = GriptapeNodes.handle_request(CreateNodeRequest(node_type='Agent', specific_library_name='Griptape Nodes Library', node_name='Agent', metadata={'position': {'x': -4544.659973961012, 'y': -819.4184844577405}, 'tempId': 'placing-1762808109028-j4ftie', 'library_node_metadata': NodeMetadata(category='agents', description='Creates an AI agent with conversation memory and the ability to use tools', display_name='Agent', tags=None, icon=None, color=None, group='create', deprecation=None), 'library': 'Griptape Nodes Library', 'node_type': 'Agent', 'showaddparameter': False, 'size': {'width': 600, 'height': 864}, 'category': 'agents'}, initial_setup=True)).node_name
    GriptapeNodes.handle_request(CreateConnectionRequest(source_node_name=node0_name, source_parameter_name='exec_out', target_node_name=node2_name, target_parameter_name='exec_in', initial_setup=True))
    GriptapeNodes.handle_request(CreateConnectionRequest(source_node_name=node2_name, source_parameter_name='exec_out', target_node_name=node1_name, target_parameter_name='exec_in', initial_setup=True))
    GriptapeNodes.handle_request(CreateConnectionRequest(source_node_name=node0_name, source_parameter_name='prompt', target_node_name=node2_name, target_parameter_name='prompt', initial_setup=True))
    GriptapeNodes.handle_request(CreateConnectionRequest(source_node_name=node2_name, source_parameter_name='output', target_node_name=node1_name, target_parameter_name='output', initial_setup=True))
    with GriptapeNodes.ContextManager().node(node0_name):
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='prompt', node_name=node0_name, value=top_level_unique_values_dict['25cb62ab-365b-42c9-ae07-a0fe7915c079'], initial_setup=True, is_output=False))
    with GriptapeNodes.ContextManager().node(node2_name):
        GriptapeNodes.handle_request(SetParameterValueRequest(parameter_name='prompt', node_name=node2_name, value=top_level_unique_values_dict['25cb62ab-365b-42c9-ae07-a0fe7915c079'], initial_setup=True, is_output=False))

def _ensure_workflow_context():
    context_manager = GriptapeNodes.ContextManager()
    if not context_manager.has_current_flow():
        top_level_flow_request = GetTopLevelFlowRequest()
        top_level_flow_result = GriptapeNodes.handle_request(top_level_flow_request)
        if isinstance(top_level_flow_result, GetTopLevelFlowResultSuccess) and top_level_flow_result.flow_name is not None:
            flow_manager = GriptapeNodes.FlowManager()
            flow_obj = flow_manager.get_flow_by_name(top_level_flow_result.flow_name)
            context_manager.push_flow(flow_obj)

def execute_workflow(input: dict, storage_backend: str='local', workflow_executor: WorkflowExecutor | None=None, pickle_control_flow_result: bool=False) -> dict | None:
    return asyncio.run(aexecute_workflow(input=input, storage_backend=storage_backend, workflow_executor=workflow_executor, pickle_control_flow_result=pickle_control_flow_result))

async def aexecute_workflow(input: dict, storage_backend: str='local', workflow_executor: WorkflowExecutor | None=None, pickle_control_flow_result: bool=False) -> dict | None:
    _ensure_workflow_context()
    storage_backend_enum = StorageBackend(storage_backend)
    workflow_executor = workflow_executor or LocalWorkflowExecutor(storage_backend=storage_backend_enum)
    async with workflow_executor as executor:
        await executor.arun(flow_input=input, pickle_control_flow_result=pickle_control_flow_result)
    return executor.output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--storage-backend', choices=['local', 'gtc'], default='local', help="Storage backend to use: 'local' for local filesystem or 'gtc' for Griptape Cloud")
    parser.add_argument('--json-input', default=None, help='JSON string containing parameter values. Takes precedence over individual parameter arguments if provided.')
    parser.add_argument('--execution_environment', default=None, help='Environment that the node should execute in')
    parser.add_argument('--job_group', default=None, help='Groupings of multiple nodes to send up as a Deadline Cloud job.')
    parser.add_argument('--exec_out', default=None, help='Connection to the next node in the execution chain')
    parser.add_argument('--prompt', default=None, help='New parameter')
    args = parser.parse_args()
    flow_input = {}
    if args.json_input is not None:
        flow_input = json.loads(args.json_input)
    if args.json_input is None:
        if 'Start Flow' not in flow_input:
            flow_input['Start Flow'] = {}
        if args.execution_environment is not None:
            flow_input['Start Flow']['execution_environment'] = args.execution_environment
        if args.job_group is not None:
            flow_input['Start Flow']['job_group'] = args.job_group
        if args.exec_out is not None:
            flow_input['Start Flow']['exec_out'] = args.exec_out
        if args.prompt is not None:
            flow_input['Start Flow']['prompt'] = args.prompt
    workflow_output = execute_workflow(input=flow_input, storage_backend=args.storage_backend)
    print(workflow_output)

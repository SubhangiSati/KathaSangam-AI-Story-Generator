import os # portable way for integrating with os
import streamlit as st

# Streamlit secrets
USER_ID = st.secrets["USER_ID"]
PAT = st.secrets["PAT"]
APP_ID = st.secrets["APP_ID"]
WORKFLOW_ID_TEXT = st.secrets["WORKFLOW_ID_TEXT"]

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel #manage comm with Clarifai API server using gRPC(Google Remote Procedure Call)
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc #contain protocol buffer definitions and gRPC service definitions 
from clarifai_grpc.grpc.api.status import status_code_pb2# definitions for representing status codes used in communication with the Clarifai API

@st.cache_data(persist=True)
def generate_story_from_text(user_input):

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,  
            workflow_id=WORKFLOW_ID_TEXT,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            # url=TEXT_FILE_URL
                            raw=user_input
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)
        raise Exception("Post workflow results failed, status: " + post_workflow_results_response.status.description)

    # Initialize an empty list to store the outputs
    outputs = []

    # Iterate over each result
    for result in post_workflow_results_response.results:
        # Iterate over each output in the result
        for output in result.outputs:
            # Append the raw text of the output to the list of outputs
            outputs.append(output.data.text.raw)

    # Join the outputs into a single string and return
    return "\n".join(outputs)

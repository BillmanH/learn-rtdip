from rtdip_sdk.pipelines.execute import PipelineJob, PipelineStep, PipelineTask
from rtdip_sdk.pipelines.sources import SparkEventhubSource
from rtdip_sdk.pipelines.transformers import BinaryToStringTransformer
from rtdip_sdk.pipelines.destinations import SparkDeltaDestination
from rtdip_sdk.pipelines.secrets import PipelineSecret, DatabricksSecrets
import json
import os


step_list = []

# read step
eventhub_configuration = {
    "eventhubs.connectionString": os.environ.get("EVENT_HUB_CON_STR"),
    "eventhubs.consumerGroup": "$Default",
    "eventhubs.startingPosition": json.dumps({"offset": "0", "seqNo": -1, "enqueuedTime": None, "isInclusive": True})
}

step_list.append(PipelineStep(
    name="read_eventhub",
    description="Connects to eventhub and reads data. Sends data to the output step.",
    component=SparkEventhubSource,
    component_parameters={"options": eventhub_configuration},
    provide_output_to_step=["arbitrary_transform"]
))

# transform step
step_list.append(PipelineStep(
    name="arbitrary_transform",
    description="test_step2",
    component=BinaryToStringTransformer,
    component_parameters={
        "source_column_name": "body",
        "target_column_name": "body"
    },
    depends_on_step=["read_eventhub"],
    provide_output_to_step=["write_data"]
))

# write step
step_list.append(PipelineStep(
    name="write_data",
    description="writes the data to a delta file",
    component=SparkDeltaDestination,
    component_parameters={
        "destination": "test_table",
        "options": {},
        "mode": "overwrite"    
    },
    depends_on_step=["arbitrary_transform"]
))


task = PipelineTask(
    name="test_task",
    description="test_task",
    step_list=step_list,
    batch_task=True
)

pipeline_job = PipelineJob(
    name="test_job",
    description="test_job", 
    version="0.0.1",
    task_list=[task]
)


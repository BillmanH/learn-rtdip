from rtdip_sdk.pipelines.execute import PipelineJobExecute
from pipeline import pipeline_job

pipeline = PipelineJobExecute(pipeline_job)

result = pipeline.run() 
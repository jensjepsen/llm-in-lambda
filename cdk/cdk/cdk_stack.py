from aws_cdk import (
    Stack,
    CfnOutput
)
from constructs import Construct

from .constructs import model_lambda

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ml = model_lambda.ModelLambda(self, "ModelLambda")

        CfnOutput(self, "ModelLambdaUrl", value=ml.url)
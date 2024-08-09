from aws_cdk import (
    aws_lambda as _lambda,
    aws_ecr_assets as ecr_assets,
    Duration
)

from constructs import Construct

class ModelLambda(Construct):
    
        def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
            super().__init__(scope, construct_id, **kwargs)
    
            
            # example resource
            lambda_function = _lambda.DockerImageFunction(
                self, "ModelLambda",
                code=_lambda.DockerImageCode.from_image_asset(
                      directory="../",
                      file="model_lambda/Dockerfile",
                      exclude=["cdk", "tests"],
                      platform=ecr_assets.Platform.LINUX_AMD64
                ),
                function_name="PHI3-ModelLambda",
                environment={
                    "AWS_LWA_INVOKE_MODE": "RESPONSE_STREAM"
                },
                timeout=Duration.minutes(5),
                memory_size=10240
            )

            function_url = lambda_function.add_function_url(
                  auth_type=_lambda.FunctionUrlAuthType.AWS_IAM,
                  invoke_mode=_lambda.InvokeMode.RESPONSE_STREAM
            )

            self.url = function_url.url

from aws_cdk import (
    aws_lambda,
    aws_iam,
    core
)


class LambdaStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # ==================================================
        # ================= IAM ROLE =======================
        # ==================================================
        role = aws_iam.Role(
            scope=self,
            id='role',
            assumed_by=aws_iam.ServicePrincipal(
                service='lambda.amazonaws.com'
            )
        )
        role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
        )

        # ==================================================
        # =================== ECR IMAGE ====================
        # ==================================================
        ecr_image = aws_lambda.DockerImageCode.from_image_asset(
            repository_name='lambda-inference',
            directory='lambda_image'
        )

        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        aws_lambda.DockerImageFunction(
            scope=self,
            id='lambda',
            function_name='r-inference',
            code=ecr_image,
            memory_size=3000,
            role=role,
            environment={
                'S3_MODEL_URI': '<PLACE YOUR MODEL S3 URI HERE>'
            },
            timeout=core.Duration.seconds(300)
        )


app = core.App()
LambdaStack(app, "LambdaStack")
app.synth()

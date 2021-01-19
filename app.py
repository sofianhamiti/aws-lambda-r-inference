from aws_cdk import (
    aws_lambda,
    aws_iam,
    aws_apigatewayv2,
    core
)


class InferenceStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        project_name = 'r-inference'
        s3_model_uri = '<ADD YOUR S3 MODEL URI HERE>'
        # ==================================================
        # ================= IAM ROLES ======================
        # ==================================================
        lambda_role = aws_iam.Role(
            scope=self,
            id='lambda_role',
            assumed_by=aws_iam.ServicePrincipal(service='lambda.amazonaws.com'),
            managed_policies=[aws_iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambdaExecute')]
        )

        api_role = aws_iam.Role(
            scope=self,
            id='api_role',
            assumed_by=aws_iam.ServicePrincipal(service='apigateway.amazonaws.com'),
        )
        api_role.add_to_policy(aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=['lambda:InvokeFunction'],
            resources=['*']
        ))
        # ==================================================
        # =================== ECR IMAGE ====================
        # ==================================================
        ecr_image = aws_lambda.DockerImageCode.from_image_asset(
            repository_name=project_name,
            directory='lambda_image'
        )

        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        lambda_function = aws_lambda.DockerImageFunction(
            scope=self,
            id='lambda',
            function_name=project_name,
            code=ecr_image,
            memory_size=1024,
            role=lambda_role,
            environment={
                'S3_MODEL_URI': s3_model_uri
            },
            timeout=core.Duration.seconds(30)
        )

        # ==================================================
        # ================== API GATEWAY ===================
        # ==================================================
        api = aws_apigatewayv2.HttpApi(
            scope=self,
            id='api_gateway',
            api_name=project_name,
            cors_preflight={
                "allow_headers": ["Authorization"],
                "allow_methods": [aws_apigatewayv2.HttpMethod.POST],
                "allow_origins": ["*"],
                "max_age": core.Duration.days(10)
            }
        )

        integration = aws_apigatewayv2.CfnIntegration(
            scope=self,
            id='integration',
            api_id=api.http_api_id,
            credentials_arn=api_role.role_arn,
            integration_type='AWS_PROXY',
            integration_uri=lambda_function.function_arn,
            integration_method='POST',
            payload_format_version='2.0'
        )

        aws_apigatewayv2.CfnRoute(
            scope=self,
            id='route',
            api_id=api.http_api_id,
            route_key='POST /',
            target=f'integrations/{integration.ref}'
        )


app = core.App()
InferenceStack(app, "InferenceStack")
app.synth()

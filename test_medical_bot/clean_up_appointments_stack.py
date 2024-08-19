from aws_cdk import (
    core as cdk,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    aws_dynamodb as dynamodb
)

class CleanUpAppointmentsStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, appointments_table: dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the Lambda function
        clean_up_lambda = lambda_.Function(
            self, "CleanUpAppointmentsFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="clean_up_appointments.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                'TABLE_NAME': appointments_table.table_name,
            }
        )

        # Grant the Lambda function read/write permissions on the DynamoDB table
        appointments_table.grant_read_write_data(clean_up_lambda)

        # Create a CloudWatch Event Rule to trigger the Lambda function periodically
        rule = events.Rule(
            self, "CleanUpAppointmentsRule",
            schedule=events.Schedule.rate(cdk.Duration.hours(1))
        )
        rule.add_target(targets.LambdaFunction(clean_up_lambda))

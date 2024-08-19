# dynamodb_table.py

from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    Stack,
)
from constructs import Construct

class DynamoDBTableConstruct_appointments(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Créer une table DynamoDB
        self.table = dynamodb.Table(self, "AppointmentsWithCdk",
            table_name="AppointmentsWithCdk",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="sortKey",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
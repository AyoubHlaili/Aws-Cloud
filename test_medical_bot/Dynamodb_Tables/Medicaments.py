
from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    
)
from constructs import Construct

class DynamoDBTableConstruct_medicaments(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Créer une table DynamoDB
        self.table = dynamodb.Table(self, "Medicaments",
            table_name="Medicaments",
            partition_key=dynamodb.Attribute(
                name="Med",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SortKey",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
    def get_table(self):
        return self.table        
import aws_cdk as core
import aws_cdk.assertions as assertions

from test_medical_bot.test_medical_bot_stack import TestMedicalBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in test_medical_bot/test_medical_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TestMedicalBotStack(app, "test-medical-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

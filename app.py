import os
import aws_cdk as cdk
import aws_cdk as cdk
from test_medical_bot.test_medical_bot_stack import TestMedicalBotStack

app = cdk.App()
TestMedicalBotStack(app, "TestMedicalBotStack")


app.synth()

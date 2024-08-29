
from aws_cdk import (
    Duration,
    Stack,
    aws_lex as lex,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    RemovalPolicy,
)
import os 
from constructs import Construct
from test_medical_bot.Dynamodb_Tables.Appointments import DynamoDBTableConstruct_appointments
from test_medical_bot.Dynamodb_Tables.HomeHealthCare import DynamoDBTableConstruct_HomeHealthCare
from test_medical_bot.Dynamodb_Tables.MedicalAnalysis import DynamoDBTableConstruct_MedicalAnalysis
from test_medical_bot.Dynamodb_Tables.Medicaments import DynamoDBTableConstruct_medicaments
from test_medical_bot.Dynamodb_Tables.Symptoms import DynamoDBTableConstruct_symptoms
from test_medical_bot.Intents.Greeting import greeting
from test_medical_bot.Intents.BookAppointment import book_appointment
from test_medical_bot.Intents.Fallback import fallback
from test_medical_bot.Intents.BookAppointment import appointment_type_slot_type
from test_medical_bot.Intents.GetSymptomsAdvice import (severity,get_symptoms)
from test_medical_bot.Intents.Goodbye import goodbye
from test_medical_bot.Intents.GetMedicalInfo import get_medical_info
from test_medical_bot.Intents.Thankyou import thankyou
from test_medical_bot.Intents.NearbyPharmacies import find_nearest_pharmacy_intent
from test_medical_bot.Intents.check_med_avalibility import check_med_availability
from test_medical_bot.Intents.HomeHealthCare import (healthcare_service_slot_type,request_home_healthcare_intent)
from test_medical_bot.Intents.CancelHomeHealthCareAppointment import cancel_home_healthcare_intent
from test_medical_bot.Intents.UploadMedicalAnalysis import upload_medical_analysis
from test_medical_bot.Intents.GetSymptomsInfo import get_symptoms_info

class TestMedicalBotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
         # Définir la fonction Lambda
        fulfillment_lambda = _lambda.Function(
             self, 'MyLambdaFunction',
             runtime=_lambda.Runtime.PYTHON_3_12,
             handler='handler.handler',
             code=_lambda.Code.from_asset(os.path.join(os.getcwd(), 'test_medical_bot', 'lambda')),
             timeout=Duration.seconds(300)
        )
         # Grant the Lambda function permission to be invoked by Lex
        fulfillment_lambda.add_permission("LexInvokePermission",
            principal=iam.ServicePrincipal("lex.amazonaws.com"),
            action="lambda:InvokeFunction",
            #source_arn=f"arn:aws:lex:{self.region}:{self.account}:bot/*"
        )
        
        # Define the role for Lex
        lex_role = iam.Role(self, "LexRole",
            assumed_by=iam.ServicePrincipal("lex.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonLexRunBotsOnly")
            ]
        )
        
        # Create API Gateway
        api_lambda = _lambda.Function(
            self, 'MyApiGatewayLambdaFunction',
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler='api_handler.handler',  # Adjust the handler name based on your API Lambda function file
            code=_lambda.Code.from_asset(os.path.join(os.getcwd(), 'test_medical_bot', 'lambda')),
        )
        
        
        # Create API Gateway
        api = apigateway.LambdaRestApi(
            self, "MedicationCheckApi",
            handler=api_lambda,#The Lambda function that handles requests sent to this API Gateway.
            proxy=False
        )

        items = api.root.add_resource("items")
        items.add_method("PATCH")
        items.add_method("GET")
        items.add_method("POST")
        items.add_method("DELETE")
        

         # API Gateway
        api_model = apigateway.LambdaRestApi(
            self, "MedicalBotApi",
            handler = fulfillment_lambda,
            description="This service serves the medical bot.",
            proxy=False
        )

        
        path=api_model.root.add_resource("hello")  
        path.add_method("GET")
        # Define the bot locale including the built-in Fallback Intent
        bot_locale = lex.CfnBot.BotLocaleProperty(
            locale_id="en_US",
            nlu_confidence_threshold=0.4,
            intents=[
                fallback(),
                greeting(),
                get_symptoms(),
                book_appointment(),
                goodbye() ,
                get_medical_info()  ,
                thankyou(),    
                find_nearest_pharmacy_intent(),
                check_med_availability(),
                request_home_healthcare_intent(),
                cancel_home_healthcare_intent(),
                upload_medical_analysis(),
                #get_symptoms_info()

            ],
             slot_types=[
                 appointment_type_slot_type,
                 severity,
                 healthcare_service_slot_type,
                 
                 ],
            voice_settings=lex.CfnBot.VoiceSettingsProperty(
                voice_id="Joanna"
            )
        )
        
        data_privacy_property = {
            "ChildDirected": False
        }
        
        

        # Create the Lex bot
        lex_bot = lex.CfnBot(self, "AppointmentBotCDK",
            name="AyoubMedicalBotCDK",
            description="A medical chatbot ",
            role_arn=lex_role.role_arn,
            data_privacy=data_privacy_property, 
            idle_session_ttl_in_seconds=300,
            bot_locales=[bot_locale],
            
        )

        #  # Define the Lex bot alias
        # bot_alias = lex.CfnBotAlias(self, "TestBotAlias",
        #     bot_id=lex_bot.ref,
        #     bot_alias_name="TestBotAlias",
        #     bot_version="DRAFT"
        # )

        # # Add the Lambda function to the bot alias's locale settings
        # locale_settings = lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
        #     bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
        #         enabled=True,
        #         code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
        #             lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
        #                 code_hook_interface_version="1.0",
        #                 lambda_arn=fulfillment_lambda.function_arn
        #             )
        #         )
        #     ),
        #     locale_id="en_US"
        # )

        # bot_alias.bot_alias_locale_settings = [locale_settings]
        # Create the bot alias
        # bot_alias = lex.CfnBotAlias(self, "AppointmentBotAlias",
        #     bot_id=lex_bot.ref,
        #     bot_alias_name="TestBotAliasCDK",
        #     bot_alias_locale_settings=[lex.CfnBotAlias.BotAliasLocaleSettingsItemProperty(
        #         bot_alias_locale_setting=lex.CfnBotAlias.BotAliasLocaleSettingsProperty(
        #             enabled=True,
        #             code_hook_specification=lex.CfnBotAlias.CodeHookSpecificationProperty(
        #                 lambda_code_hook=lex.CfnBotAlias.LambdaCodeHookProperty(
        #                     code_hook_interface_version="1.0",
        #                     lambda_arn=fulfillment_lambda.function_arn
        #                 )
        #             )
        #         ),
        #         locale_id="en_US",
        #     )],
        # )
        
        
        # Dynamodb Tables
        Appointments_table = DynamoDBTableConstruct_appointments(self, "DynamoDBTableConstruct")
        symptoms_table = DynamoDBTableConstruct_symptoms(self, "DynamoDBTableConstruct2")
        medicaments_table = DynamoDBTableConstruct_medicaments(self,"DynamoDBTableConstruct3")
        # Grant the API Lambda function permissions to access DynamoDB
        medicaments_table = medicaments_table.get_table()  # Get the table instance
        medicaments_table.grant_read_write_data(api_lambda)  # Grant necessary permissions
        homehealthcare_table = DynamoDBTableConstruct_HomeHealthCare(self,"DynamoDBTableConstruct4")
        medicalanalysis_table = DynamoDBTableConstruct_MedicalAnalysis(self,"DynamoDBTableConstruct5")
        
        
        # S3 Bucket
        medicalanalysis_bucket = s3.Bucket(self,
                                            "MedicalAnalysisBucket",
                                            removal_policy = RemovalPolicy.DESTROY
                                           )
        models = s3.Bucket(self,
                           "ModelBucket",
                          removal_policy = RemovalPolicy.DESTROY # Destroys the bucket when the stack is deleted
        )
        models.grant_read(fulfillment_lambda)
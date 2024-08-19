

from datetime import time
from aiohttp import ClientError
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='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',
    region_name='us-east-1'  # Northern Virginia
)
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='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',
    region_name='us-east-1'  # Northern Virginia
)
table = dynamodb.Table('MedicalAnalysis')


def validate(slots):
    # Vérifier si le type de rendez-vous est fourni
    if not slots['Name']:
        print("Inside Empty Name")
        return {
            'isValid': False,
            'violatedSlot': 'Name'
        }
    if not slots['ImageFile']:
        print("Inside Empty ImageFile")
        return {
            'isValid': False,
            'violatedSlot': 'ImageFile'
        }
    return {'isValid': True}

def upload_medical_analysis_handler(event, slots, intent, invocation_source,context):
    validation_result = validate(slots)
    
    if invocation_source == 'DialogCodeHook':
        # Si la validation échoue, demander à l'utilisateur de fournir le slot manquant
        if not validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
            return response
        else:
            # Si tous les slots sont valides, déléguer le contrôle pour la suite du traitement
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
            return response
    
    
    
    if invocation_source == 'FulfillmentCodeHook':
        try:
            # Extract the slot value (image data)
            slots = event['sessionState']['intent']['slots']
            image_data = slots['ImageFile']['value']['interpretedValue']
            image_name = f"analysis_{context.aws_request_id}.png"  # Generate a unique file name

            # Upload to S3
            s3_client.put_object(
                Bucket='testmedicalbotstack-medicalanalysisbucket631caf53-seogqdjkslxp',
                Key=image_name,
                Body=image_data,
                ContentType='image/png'
            )
            name = event['sessionState']['sessionAttributes'].get('Name', slots['Name']['value']['interpretedValue'])
            upload_timestamp = event.get('requestAttributes', {}).get('requestTimestamp', time.strftime('%Y-%m-%dT%H:%M:%S'))
            # Store metadata in DynamoDB
            table.put_item(
                Item={
                    'FullName': name,
                    'ImageName': image_name,
                    'UploadTimestamp': upload_timestamp
                }
            )
            # Return success response
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": "UploadMedicalAnalysis",
                        "state": "Fulfilled"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Your medical analysis has been successfully uploaded."
                    }
                ]
            }
        
        except ClientError as e:
            print(e)
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": "UploadMedicalAnalysis",
                        "state": "Failed"
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Failed to upload your medical analysis. Please try again later."
                    }
                ]
            }

            
        


    
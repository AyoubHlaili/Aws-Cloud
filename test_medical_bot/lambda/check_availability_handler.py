import json
import boto3
from botocore.exceptions import ClientError
import requests

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Medicaments')
API_GATEWAY_URL = "https://tualfjiv9l.execute-api.us-east-1.amazonaws.com/prod/items"

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='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',
    region_name='us-east-1'  # Northern Virginia
)

def validate(slots):
    if not slots.get('Medication'):
        return {'isValid': False, 'violatedSlot': 'Medication'}
    if not slots.get('Quantity') or int(slots['Quantity']['value']['interpretedValue']) <= 0:
        return {'isValid': False, 'violatedSlot': 'Quantity'}
    return {'isValid': True}

def handle_check_medication_availability(event, slots, intent, invocation_source):
    validation_result = validate(slots)
    
    if invocation_source == 'DialogCodeHook':
        if not validation_result['isValid']:
            return {
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
        else:
            return {
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
    
    if invocation_source == 'FulfillmentCodeHook':
        # Parse the medication and quantity from the event
        medication = slots['Medication']['value']['interpretedValue']
        quantity_requested =int(slots['Quantity']['value']['interpretedValue'])
        items=requests.get(API_GATEWAY_URL)
        payload = {
            "Med": medication,
            "SortKey":medication +"#",
            "Quantity": quantity_requested
        }
        print(payload)
        response = requests.post(API_GATEWAY_URL, json=payload)
        # Log the response for debugging
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        if response.status_code == 200:
            return build_lex_response(f"The quantity of {medication} has been updated by {quantity_requested} units.", intent, slots)
        else:
            return build_lex_response(f"Failed to update the quantity of {medication}.", intent, slots)

def build_lex_response(message, intent, slots):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent,
                "slots": slots,
                "state": "Fulfilled"  # or "Failed" based on the outcome
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

from twilio.rest import Client
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='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',
    region_name='us-east-1'  # Northern Virginia
)
table = dynamodb.Table('HomeHealthCare')

def validate(slots):
    if not slots.get('FullName'):
        return {'isValid': False, 'violatedSlot': 'FullName'}
    return {'isValid': True}

def handle_cancel_home_health_care_appointment(event, slots, intent, invocation_source):
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
                    "dialogAction": {"type": "Delegate"},
                    "intent": {'name': intent, 'slots': slots}
                }
            }
    
    if invocation_source == 'FulfillmentCodeHook':
            return fulfill_cancel_home_health_care_appointment(event, slots)
        


def fulfill_cancel_home_health_care_appointment(event, slots):
    FullName = slots['FullName']['value']['interpretedValue']
    user_id = FullName  # Assuming FullName is unique

    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('FullName').eq(user_id)
        )
        if response['Items']:
            for item in response['Items']:
                # Extract fields from the item
                PhoneNumber = item.get('PhoneNumber')
                healthcare_service_type = item.get('HealthcareServiceType')
                Home_Location = item.get('HomeLocation')
                table.delete_item(
                    Key={'FullName': user_id, 'sortKey': item['sortKey']}
                )
            message_content = "Your appointments have been canceled."
        else:
            message_content = "No matching appointments found to cancel."
    except Exception as e:
        message_content = f"Sorry, there was an error canceling your appointment: {str(e)}"
    sms_not(FullName,PhoneNumber,healthcare_service_type,Home_Location)
    return close_session(event, slots, message_content)

def close_session(event, slots, message_content):
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                'name': event['sessionState']['intent']['name'],
                'slots': slots,
                'state': 'Fulfilled'
            }
        },
        "messages": [
            {"contentType": "PlainText", "content": message_content}
        ]
    }
def sms_not(full_name,PhoneNumber,healthcare_service_type,Home_Location):
    try:
        account_sid = 'AC94859835bca445d23f2f8336e895b0d3'
        auth_token = '37d8ab7fbbb21e6ed2c7db54f54bf1ca'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Hello {full_name}, Your {healthcare_service_type} Service to {Home_Location} has been canceled.",
            from_='+13605583340',
            to=PhoneNumber,
        )

        print(f"Message sent with SID: {message.sid}")
        if message.error_code is not None:
            print(f"Twilio Error: {message.error_message}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")

import datetime
import re
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='gL05qNdMLS4O7vD0OAhx0S4oqcAQu2OL5cnBQpsu',
    region_name='us-east-1'  # Northern Virginia
)
# Replace 'YourDynamoDBTableName' with the actual name of your DynamoDB table
table = dynamodb.Table('AppointmentsWithCdk')

def validate(slots):
    # Vérifier si le type de rendez-vous est fourni
    if not slots['AppointmentType']:
        print("Inside Empty AppointmentType")
        return {
            'isValid': False,
            'violatedSlot': 'AppointmentType'
        }
        
    # Vérifier si la date du rendez-vous est fournie
    if not slots['Date']:
        return {
            'isValid': False,
            'violatedSlot': 'Date'
        }
        
    # Vérifier si l'heure du rendez-vous est fournie
    if not slots['Time']:
        return {
            'isValid': False,
            'violatedSlot': 'Time'
        }
    # Check if the provided time is either on the hour or half-hour
    time_pattern = re.compile(r'^(0[8-9]|1[0-7]):(00|30)$')
    appointment_time = slots['Time']['value']['interpretedValue']
    
    if not time_pattern.match(appointment_time):
        return {
            'isValid': False,
            'violatedSlot': 'Time'
        }
    return {'isValid': True}

def handle_book_appointment(event, slots, intent, invocation_source):
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
        # Extract slot values
        user_id = event['sessionId']
        appointment_type = slots['AppointmentType']['value']['interpretedValue']
        appointment_date = slots['Date']['value']['interpretedValue']
        appointment_time = slots['Time']['value']['interpretedValue']
        

         # Construct the sort key for the DynamoDB item
        sort_key = f"{appointment_date}#{appointment_time}"
        
        # Add order to database
        try:
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id) & 
                                       boto3.dynamodb.conditions.Key('sortKey').eq(sort_key)
            )
            if response['Items']:
                for item in response['Items']:
                    if item['AppointmentType'] == appointment_type:
                        message_content = f"An appointment for {appointment_type} at {appointment_date} {appointment_time} already exists."
                        return {
                            'sessionState': {
                                'dialogAction': {
                                    'type': 'Close',
                                },
                                'intent': {
                                    'name': event['sessionState']['intent']['name'],
                                    'state': 'Fulfilled',
                                },
                            },
                            'messages': [{
                                'contentType': 'PlainText',
                                'content': message_content,
                            }],
                        }
            table.put_item(
                Item={
                    'user_id': user_id,
                    'AppointmentType': appointment_type,
                    'sortKey': sort_key, 
                    'Date': appointment_date,
                    'Time': appointment_time,
                    'CreatedAt': str(datetime.datetime.now())
                }
            )
            message_content = "Thanks, I have placed your appointment."
        except Exception as e:
            message_content = f"Sorry, there was an error placing your appointment: {str(e)}"
        
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    'name': intent,
                    'slots': slots,
                    'state': 'Fulfilled'
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": message_content
                }
            ]
        }
        return response

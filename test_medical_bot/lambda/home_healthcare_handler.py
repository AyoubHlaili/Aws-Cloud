import datetime
from twilio.rest import Client
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='gL05qNdMLS4O7vD0OAhx0S4oqcAQu2OL5cnBQpsu',
    region_name='us-east-1'  # Northern Virginia
)
# Replace 'YourDynamoDBTableName' with the actual name of your DynamoDB table
table = dynamodb.Table('HomeHealthCare')

def validate(slots):
    # Vérifier si le type de rendez-vous est fourni
    if not slots['FullName']:
        print("Inside Empty FullName")
        return {
            'isValid': False,
            'violatedSlot': 'FullName'
        }
        
    # Vérifier si la date du rendez-vous est fournie
    if not slots['PhoneNumber']:
        return {
            'isValid': False,
            'violatedSlot': 'PhoneNumber'
        }
        
    # Vérifier si l'heure du rendez-vous est fournie
    if not slots['Home_Location']:
        return {
            'isValid': False,
            'violatedSlot': 'Home_Location'
        }
    if not slots['HealthcareServiceType']:
        return {
            'isValid': False,
            'violatedSlot': 'HealthcareServiceType'
        }
    # if not slots['SpecialRequirements']:
    #     return {
    #         'isValid': False,
    #         'violatedSlot': 'SpecialRequirements'
    #     }
    return {'isValid': True}

def handle_home_health_care_appointment(event, slots, intent, invocation_source):
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
        full_name = slots['FullName']['value']['interpretedValue']
        PhoneNumber = slots['PhoneNumber']['value']['interpretedValue']
        Home_Location = slots['Home_Location']['value']['interpretedValue']
        healthcare_service_type = slots['HealthcareServiceType']['value']['interpretedValue']

        # Construct the sort key for the DynamoDB item
        sort_key = f"{full_name}#{PhoneNumber}#{Home_Location}"
        
        # Add order to database
        try:
            table.put_item(
                Item={
                    'FullName': full_name,
                    'sortKey': sort_key,
                    'PhoneNumber': PhoneNumber,
                    'Home_Location': Home_Location,
                    'HealthcareServiceType': healthcare_service_type,
                    'CreatedAt': str(datetime.datetime.now())
                }
            )
            print("hey")
            
            sms_not(full_name,healthcare_service_type,Home_Location,PhoneNumber)
            print("hi")
            message_content = "Thanks, I have placed your HomeHealthCare Service."    
        except Exception as e:
            message_content = f"Sorry, there was an error placing your HomeHealthCare Service: {str(e)}"
        print("hello")
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
    
def sms_not(full_name, healthcare_service_type, Home_Location,PhoneNumber):
    try:
        account_sid = 'AC94859835bca445d23f2f8336e895b0d3'
        auth_token = '37d8ab7fbbb21e6ed2c7db54f54bf1ca'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Hello {full_name}, Your {healthcare_service_type} Service to {Home_Location} is on its way.",
            from_='+13605583340',
            to=PhoneNumber,
        )

        print(f"Message sent with SID: {message.sid}")
        if message.error_code is not None:
            print(f"Twilio Error: {message.error_message}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")


            


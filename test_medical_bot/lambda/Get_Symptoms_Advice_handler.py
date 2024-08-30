import datetime
import boto3

# Initialize DynamoDB resource
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id='AKIA57LEVK6QRETBTEJY',
    aws_secret_access_key='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',
    region_name='us-east-1'
)
table = dynamodb.Table('Symptoms')

def validate(slots):
    if not slots['SymptomType']:
        return {
            'isValid': False,
            'violatedSlot': 'SymptomType'
        }
    if not slots['Duration']:
        return {
            'isValid': False,
            'violatedSlot': 'Duration'
        }
    if not slots['Severity']:
        return {
            'isValid': False,
            'violatedSlot': 'Severity'
        }
    return {'isValid': True}

def handle_get_symptoms_advice(event, slots, intent, invocation_source):
    print("hi")
    validation_result = validate(slots)
    print("hello")
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
        return delegate(slots, intent)
    
    if invocation_source == 'FulfillmentCodeHook':
        print("hey")
        user_id = event['sessionId']
        symptom_type = slots['SymptomType']['value']['interpretedValue']
        duration = slots['Duration']['value']['interpretedValue']
        severity = slots['Severity']['value']['interpretedValue']
        sort_key = f"{user_id}#{datetime.datetime.now().isoformat()}"

        # Personalized response based on history
        try:
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
            )
            history = response.get('Items', [])
            advice = get_advice(symptom_type, duration, severity, history)
            
            # Save current symptoms to history
            table.put_item(
                Item={
                    'user_id': user_id,
                    'sortKey': sort_key,
                    'SymptomType': symptom_type,
                    'Duration': duration,
                    'Severity': severity,
                    'Timestamp': str(datetime.datetime.now())
                }
            )
        except Exception as e:
            advice = f"Sorry, there was an error retrieving your history: {str(e)}"

        message_content = f"Thanks for providing me with theses information . {advice} Please note that these tips are not a substitute for a medical consultation. For severe or persistent symptoms, consult a healthcare professional."

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

def get_advice(symptom_type, duration, severity, history):
    if severity == 'mild':
        advice = f"It seems like your {symptom_type} is mild. Make sure to stay hydrated and rest. If symptoms persist, consult a healthcare professional."
    elif severity == 'moderate':
        advice = f"Your {symptom_type} is moderate. You may want to consider taking over-the-counter medications to relieve symptoms. If symptoms worsen or persist, please seek medical attention."
    elif severity == 'severe':
        advice = f"Your {symptom_type} is severe . It is recommended that you consult a healthcare professional immediately for further evaluation."

    # Check history for similar symptoms
    for record in history:
        if record['SymptomType'] == symptom_type and record['Severity'] == severity:
            advice += " It looks like you've had this symptom before. If it is recurrent, it is even more important to consult a health professional."
            break
    
    advice += " For more information, please visit [This link](https://www.healthline.com)."
    return advice

def delegate(slots, intent):
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

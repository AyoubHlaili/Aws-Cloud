import json
import requests

def validate(slots):
    # Check if MedicationName slot is provided
    if not slots['MedicationName'] or not slots['MedicationName']['value']:
        print("Inside Empty MedicationName")
        return {
            'isValid': False,
            'violatedSlot': 'MedicationName'
        }
    return {'isValid': True}

def get_medical_info(event, slots, intent_name, invocation_source):
    print(slots)
    validation_result = validate(slots)
    
    if invocation_source == 'DialogCodeHook':
        # If validation fails, ask the user to provide the missing slot
        if not validation_result['isValid']:
            return {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent_name,
                        'slots': slots
                    }
                }
            }
        else:
            # If all slots are valid, delegate control for further processing
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent_name,
                        'slots': slots
                    }
                }
            }
    
    if invocation_source == 'FulfillmentCodeHook':
        medication_name = slots['MedicationName']['value']['interpretedValue']
    
        # Fetch information from Wikipedia API
        wikipedia_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{medication_name}"

        try:
            response = requests.get(wikipedia_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            if 'extract' in data:
                summary = data['extract']
            else:
                summary = 'I did not find any information on this medication.'
        except requests.exceptions.RequestException as e:
            summary = f'I was unable to obtain information on this medication at the moment. Error: {e}'
        
        return close_intent(event, summary)

def close_intent(event, message):
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
            'content': message,
        }],
    }

def delegate(event):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'Delegate',
            },
            'intent': event['sessionState']['intent'],
        },
    }
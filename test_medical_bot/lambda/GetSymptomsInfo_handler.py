import boto3
import pickle
import logging
# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# S3 client
s3_client = boto3.client('s3')
bucket_name = 'testmedicalbotstack-modelbucketb33d855b-hrfj6he2b0vs'
model_key = 'decision_tree_model.pkl'
models = {}

def validate(slots):
    """Validates that the necessary slot (Symptoms) is filled."""
    if not slots.get('Symptoms'):
        return {
            'isValid': False,
            'violatedSlot': 'Symptoms'
        }
    return {'isValid': True}

def handle_get_symptoms_info(event, slots, intent, invocation_source, context):
    """Handles the Lex bot request based on the invocation source."""
    validation_result = validate(slots)
    
    if invocation_source == 'DialogCodeHook':
        if not validation_result['isValid']:
            return elicit_slot(slots, intent, validation_result['violatedSlot'])
        return delegate(slots, intent)
    
    if invocation_source == 'FulfillmentCodeHook':
        symptoms = slots['Symptoms']['value']['interpretedValue']
        message_content = result(symptoms)
        return close(slots, intent, message_content)

def elicit_slot(slots, intent, slot_to_elicit):
    """Elicits a slot value from the user."""
    return {
        "sessionState": {
            "dialogAction": {
                'slotToElicit': slot_to_elicit,
                "type": "ElicitSlot"
            },
            "intent": {
                'name': intent,
                'slots': slots
            }
        }
    }

def delegate(slots, intent):
    """Delegates the next action to Lex."""
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

def close(slots, intent, message_content):
    """Closes the Lex conversation with the user."""
    return {
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

def download_model():
    """Downloads the model from S3 if it hasn't been loaded yet."""
    try:
        s3_response = s3_client.get_object(Bucket=bucket_name, Key=model_key)
        file = s3_response["Body"].read()
        models['decision_tree'] = pickle.loads(file)
        logger.info("Model downloaded and loaded successfully.")
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        raise

def predict(symptoms_list):
    """Predicts the disease based on symptoms using the downloaded model."""
    print("hi")
    if not models.get('decision_tree'):
        download_model()
        print("success")
    model = models['decision_tree']
    print(model)
    # Encode symptoms (ensure this matches the model's training setup)
    symptoms_encoded = encode_symptoms(symptoms_list)

    # Predict the disease
    prediction = model.predict([symptoms_encoded])
    diseases = ['Disease1', 'Disease2', 'Disease3']  # Replace with actual diseases
    predicted_disease = diseases[prediction[0]]

    return predicted_disease

def encode_symptoms(symptoms_list):
    """Encodes symptoms into a binary vector for the model."""
    symptoms_master_list = ['symptom1', 'symptom2', 'symptom3']  # List of all possible symptoms
    encoded_vector = [1 if symptom in symptoms_list else 0 for symptom in symptoms_master_list]
    return encoded_vector

def result(symptoms):
    """Generates a result message based on the predicted disease."""
    try:
        symptoms_list = [symptom.strip() for symptom in symptoms.split(',')]
        logger.info(f"Received symptoms: {symptoms_list}")

        predicted_disease = predict(symptoms_list)

        return f"The predicted disease based on your symptoms '{symptoms}' is: {predicted_disease}"
    except Exception as e:
        logger.error(f"Error in processing symptoms: {e}")
        return "Sorry, I couldn't process your symptoms. Please try again."

import json
import requests

def find_nearest_pharmacy(location):
    headers = {
        'User-Agent': 'MedicalChatbot/1.0 (your.email@example.com)'
    }
    
    try:
        # OpenStreetMap Nominatim API URL for geocoding
        nominatim_url = f"https://nominatim.openstreetmap.org/search?city={location}&country=US&format=json&limit=1"
        response = requests.get(nominatim_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        if data:
            # Extract the coordinates of the location
            lat = data[0]['lat']
            lon = data[0]['lon']
            
            # Use the coordinates to find nearby pharmacies
            pharmacy_url = f"https://nominatim.openstreetmap.org/search?format=json&q=pharmacy&lat={lat}&lon={lon}&limit=5"
            pharmacy_response = requests.get(pharmacy_url, headers=headers)
            pharmacy_response.raise_for_status()  # Raise an exception for HTTP errors
            pharmacy_data = pharmacy_response.json()

            # Log pharmacy data for debugging
            print("Pharmacy Data:", pharmacy_data)
            
            if pharmacy_data:
                # Filter for actual pharmacies
                actual_pharmacies = [p for p in pharmacy_data if p['class'] == 'amenity' and p['type'] == 'pharmacy']
                if actual_pharmacies:
                    nearest_pharmacy = actual_pharmacies[0]
                    name = nearest_pharmacy.get('display_name', 'Unknown')
                    address = nearest_pharmacy.get('address', {}).get('road', 'No address available')
                    return f"The nearest pharmacy is {name}, located at {address}."
                else:
                    return "No actual pharmacies found nearby."
            else:
                return "No pharmacies found nearby."
        else:
            return "Unable to find location. Please try again."
    
    except requests.exceptions.RequestException as e:
        return f"Request Error: {str(e)}"
    except json.JSONDecodeError:
        return "Error decoding the response from the location or pharmacy service."
    except Exception as e:
        return f"Error: {str(e)}"

def handle_find_nearest_pharmacy(event, slots, intent, invocation_source):
    if invocation_source == 'DialogCodeHook':
        # Validate if the location slot is filled
        if not slots.get('Location') or not slots['Location'].get('value'):
            response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': 'Location',
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
            return response

        # All slots are filled, delegate control to the fulfillment hook
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
        # Retrieve the location slot value
        location = slots['Location']['value']['interpretedValue']
        pharmacy_info = find_nearest_pharmacy(location)
        
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
                    "content": pharmacy_info
                }
            ]
        }
        return response

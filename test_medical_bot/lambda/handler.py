import json
from book_appointment_handler import handle_book_appointment
from Get_medical_info_handler import get_medical_info
from Get_Symptoms_Advice_handler import handle_get_symptoms_advice
from nearby_pharmacies_handler import handle_find_nearest_pharmacy
from check_availability_handler import handle_check_medication_availability
from cancel_home_healthcare_handler import handle_cancel_home_health_care_appointment
from home_healthcare_handler import  handle_home_health_care_appointment
from upload_medical_analysis_handler import upload_medical_analysis_handler

def handler(event, context):
    # Extract slots and intent name
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    invocation_source = event['invocationSource']
    
    # Route the request to the appropriate handler function
    if intent == "BookAppointment":
        return handle_book_appointment(event, slots, intent, invocation_source)
    elif intent == "ProvideMedicationInfo" :
        return get_medical_info(event,slots,intent,invocation_source)
    elif intent == "GetSymptomsAdvice":
        return handle_get_symptoms_advice(event, slots, intent, invocation_source)
    elif intent =="FindNearestPharmacy":
        return handle_find_nearest_pharmacy(event, slots, intent, invocation_source)
    elif intent =="RequestHomeHealthcare":
        return handle_home_health_care_appointment(event, slots, intent, invocation_source)
    elif intent =="CancelHomeHealthcare":
        return handle_cancel_home_health_care_appointment(event, slots, intent, invocation_source)
    elif intent == "CheckMedicationAvailability":
        return handle_check_medication_availability(event, slots, intent, invocation_source) 
    elif intent == "UploadMedicalAnalysis":
        return upload_medical_analysis_handler(event, slots, intent, invocation_source,context)
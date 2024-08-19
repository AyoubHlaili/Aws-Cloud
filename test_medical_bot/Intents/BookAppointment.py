from aws_cdk import (
    aws_lex as lex,
)
# Define the custom slot type
appointment_type_slot_type = lex.CfnBot.SlotTypeProperty(
            name="AppointmentType",
            slot_type_values=[
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="General Consultation")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Physical Therapy")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Psychologist")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Nutritionist")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Vaccination"))
            ],
            value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                resolution_strategy="ORIGINAL_VALUE"
            )
        )

def book_appointment():
    return lex.CfnBot.IntentProperty(
            name="BookAppointment",
            description="This intent is for booking a doctor appointment",
            sample_utterances=[
                lex.CfnBot.SampleUtteranceProperty(utterance="I want to book an appointment"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Schedule a consultation"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book an appointment with a doctor"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book {AppointmentType} appointment ."),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book {AppointmentType} appointment {Date} at {Time} ."),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book {AppointmentType} appointment {Date} ."),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book {AppointmentType} appointment at {Time} ."),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book an appointment at {Time} ."),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book an appointment {Date} at {Time} .")
            ],
            slots=[
                lex.CfnBot.SlotProperty(
                    name="AppointmentType",
                    slot_type_name="AppointmentType",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="What type of appointment would you like to book?"
                                        )
                                    )
                                ),
                                lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="Healthcare_Service_Type",
                                        subtitle="Choose the type of service:",
                                        buttons=[
                                            lex.CfnBot.ButtonProperty(
                                                text="General Consultation",
                                                value="General Consultation"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Physical Therapy",
                                                value="Physical Therapy"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Psychologist",
                                                value="Psychologist"
                                            ),
                                            
                                            lex.CfnBot.ButtonProperty(
                                                text="Nutritionist",
                                                value="Nutritionist"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Vaccination",
                                                value="Vaccination"
                                            ),
                                            
                                        ]
                                    )
                                )
                            ) 
                            ],
                            max_retries=3,
                            allow_interrupt=False
                        )
                    )
                ),
                lex.CfnBot.SlotProperty(
                    name="Date",
                    slot_type_name="AMAZON.Date",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="On what date would you like to book the appointment?"
                                        )
                                    )
                                )
                            ],
                            max_retries=3,
                            allow_interrupt=False
                        )
                    )
                ),
                lex.CfnBot.SlotProperty(
                    name="Time",
                    slot_type_name="AMAZON.Time",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="At what time would you like to book the appointment ? (Time should be either on the hour (00) or half-hour (30))"
                                        )
                                    )
                                )
                            ],
                            max_retries=3,
                            allow_interrupt=False
                        )
                    )
                )
            ],
            slot_priorities=[
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="AppointmentType",
                    priority=1
                ),
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="Date",
                    priority=2
                ),
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="Time",
                    priority=3
                )
            ],
            dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                enabled=True
            ),
            
            fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                enabled=True,
                # is_active=True,
                # fulfillment_updates_specification=lex.CfnBot.FulfillmentUpdatesSpecificationProperty(active=False),
            ),
            
        )
         
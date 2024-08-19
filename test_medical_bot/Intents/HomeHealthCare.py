from aws_cdk import (
    aws_lex as lex,
)
# Define custom slot type for HealthcareServiceType
healthcare_service_slot_type = lex.CfnBot.SlotTypeProperty(
            name="HealthcareServiceType",
            slot_type_values=[
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Nursing Care")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Physical Therapy")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Occupational Therapy")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Medical Social Services")),
                lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="Nutritional Support"))
            ],
            value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
                resolution_strategy="ORIGINAL_VALUE"
            )
        )

def request_home_healthcare_intent():
    return lex.CfnBot.IntentProperty(
            name="RequestHomeHealthcare",
            description="Intent to request home healthcare services with advanced options",
            sample_utterances=[
                lex.CfnBot.SampleUtteranceProperty(utterance="I need {HealthcareServiceType} at home"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Request home healthcare service"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Book {HealthcareServiceType} at my home."),
                lex.CfnBot.SampleUtteranceProperty(utterance="Schedule a home visit for {HealthcareServiceType} "),
                lex.CfnBot.SampleUtteranceProperty(utterance="Home healthcare appointment ."),
                lex.CfnBot.SampleUtteranceProperty(utterance="I want a healthcare appointment .")
            ],
            slots=[
                lex.CfnBot.SlotProperty(
                    name="FullName",
                    slot_type_name="AMAZON.AlphaNumeric",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="Can you please provide your full name?"
                                        )
                                    )
                                )
                            ],
                            max_retries=3,
                            allow_interrupt=True
                        )
                    )
                ),
                lex.CfnBot.SlotProperty(
                    name="PhoneNumber",
                    slot_type_name="AMAZON.AlphaNumeric",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="Can you please provide your Phone Number?"
                                        )
                                    )
                                )
                            ],
                            max_retries=3,
                            allow_interrupt=True
                        )
                    )
                ),
                lex.CfnBot.SlotProperty(
                    name="Home_Location",
                    slot_type_name="AMAZON.AlphaNumeric",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="Where do you want the HomeHealthCare service ?"
                                        )
                                    )
                                )
                            ],
                            max_retries=3,
                            allow_interrupt=True
                        )
                    )
                ),
                lex.CfnBot.SlotProperty(
                    name="HealthcareServiceType",
                    slot_type_name="HealthcareServiceType",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="What type of healthcare service do you need?"
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
                                                text="Nursing Care",
                                                value="Nursing Care"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Physical Therapy",
                                                value="Physical Therapy"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Occupational Therapy",
                                                value="Occupational Therapy"
                                            ),
                                            
                                            lex.CfnBot.ButtonProperty(
                                                text="Nutritional Support",
                                                value="Nutritional Support"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Medical Social Services",
                                                value="Medical Social Services"
                                            ),
                                            
                                        ]
                                    )
                                )
                            ) 
                            ],
                            max_retries=3,
                            allow_interrupt=True
                        )
                    )
                ),
                
                # lex.CfnBot.SlotProperty(
                #     name="SpecialRequirements",
                #     slot_type_name="AMAZON.AlphaNumeric",
                #     value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                #         slot_constraint="Optional",
                #         prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                #             message_groups_list=[
                #                 lex.CfnBot.MessageGroupProperty(
                #                     message=lex.CfnBot.MessageProperty(
                #                         plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                #                             value="Do you have any special requirements?"
                #                         )
                #                     )
                #                 )
                #             ],
                #             max_retries=3,
                #             allow_interrupt=True
                #         )
                #     )
                # )
            ],
            slot_priorities=[
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="FullName",
                    priority=1
                ),
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="PhoneNumber",
                    priority=2
                ),
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="Home_Location",
                    priority=3
                ),
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="HealthcareServiceType",
                    priority=4
                ),
                # lex.CfnBot.SlotPriorityProperty(
                #     slot_name="SpecialRequirements",
                #     priority=5
                # )
            ],
            dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                enabled=True
            ),
            fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                enabled=True,
            ),
        )

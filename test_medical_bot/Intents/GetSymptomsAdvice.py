from aws_cdk import (
    aws_lex as lex,
)

# Define the custom slot type
severity = lex.CfnBot.SlotTypeProperty(
    name="Severity",
    slot_type_values=[
        lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="mild")),
        lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="moderate")),
        lex.CfnBot.SlotTypeValueProperty(sample_value=lex.CfnBot.SampleValueProperty(value="severe"))
    ],
    value_selection_setting=lex.CfnBot.SlotValueSelectionSettingProperty(
        resolution_strategy="ORIGINAL_VALUE"
    )
)

def get_symptoms():
    return lex.CfnBot.IntentProperty(
        name="GetSymptomsAdvice",
        description="Provide medical advice based on the user's symptoms",
        sample_utterances=[
            lex.CfnBot.SampleUtteranceProperty(utterance="I have had a {SymptomType} for {Duration} days"),
            lex.CfnBot.SampleUtteranceProperty(utterance="I have been feeling a {SymptomType} for {Duration} "),
            lex.CfnBot.SampleUtteranceProperty(utterance="My {SymptomType} has been {Severity} for {Duration} "),
            lex.CfnBot.SampleUtteranceProperty(utterance="I have had severe {SymptomType} for {Duration} "),
            lex.CfnBot.SampleUtteranceProperty(utterance="Can you give me advice for a {SymptomType} ?"),
            lex.CfnBot.SampleUtteranceProperty(utterance="I have {SymptomType} "),
            lex.CfnBot.SampleUtteranceProperty(utterance="I am {SymptomType} "),
            lex.CfnBot.SampleUtteranceProperty(utterance=" {SymptomType} is killing me ")
        ],
        slots=[
            lex.CfnBot.SlotProperty(
                name="SymptomType",
                slot_type_name="AMAZON.AlphaNumeric",
                value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="Required",
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        message_groups_list=[
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="What symptom are you experiencing?"
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
                name="Duration",
                slot_type_name="AMAZON.Number",
                value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="Required",
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        message_groups_list=[
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="How long have you been experiencing this symptom?"
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
                name="Severity",
                slot_type_name="Severity",
                value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="Required",
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        message_groups_list=[
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="How severe is the symptom? Please choose one of the options below:"
                                    )
                                )
                            ),
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    image_response_card=lex.CfnBot.ImageResponseCardProperty(
                                        title="Severity",
                                        subtitle="Choose the severity of your symptom:",
                                        buttons=[
                                            lex.CfnBot.ButtonProperty(
                                                text="Mild",
                                                value="mild"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Moderate",
                                                value="moderate"
                                            ),
                                            lex.CfnBot.ButtonProperty(
                                                text="Severe",
                                                value="severe"
                                            )
                                        ]
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
                slot_name="SymptomType",
                priority=1
            ),
            lex.CfnBot.SlotPriorityProperty(
                slot_name="Duration",
                priority=2
            ),
            lex.CfnBot.SlotPriorityProperty(
                slot_name="Severity",
                priority=3
            )
        ],
        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
            enabled=True
        ),
        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
            enabled=True,
        ),
    )

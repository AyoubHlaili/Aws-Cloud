from aws_cdk import (
    aws_lex as lex,
)


def upload_medical_analysis():
    return lex.CfnBot.IntentProperty(
        name="UploadMedicalAnalysis",
        description="Storing the Medical Analysis in S3 bucket",
        sample_utterances=[
            lex.CfnBot.SampleUtteranceProperty(utterance="I want to store my medical analysis"),
            lex.CfnBot.SampleUtteranceProperty(utterance="I want to upload my medical analysis"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Upload my medical analysis "),
            lex.CfnBot.SampleUtteranceProperty(utterance="Can I upload a medical report? "),
         
        ],
        slots=[
            lex.CfnBot.SlotProperty(
                name="ImageFile",
                slot_type_name="AMAZON.AlphaNumeric",
                value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="Required",
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        message_groups_list=[
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="Please upload your medical analysis image."
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
                name="Name",
                slot_type_name="AMAZON.AlphaNumeric",
                value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="Required",
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        message_groups_list=[
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="Please Provide me with your full name "
                                    )
                                )
                            )
                        ],
                        max_retries=3,
                        allow_interrupt=False
                    )
                )
            ),
        ],
        slot_priorities=[
            lex.CfnBot.SlotPriorityProperty(
                slot_name="Name",
                priority=1
            ),
            lex.CfnBot.SlotPriorityProperty(
                slot_name="ImageFile",
                priority=2
            ),
        ],
        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
            enabled=True
        ),
        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
            enabled=True,
        ),
    )

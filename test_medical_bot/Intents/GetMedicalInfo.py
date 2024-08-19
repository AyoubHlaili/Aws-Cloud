from aws_cdk import (
    aws_lex as lex,
)

def get_medical_info():

    return lex.CfnBot.IntentProperty(
            name="ProvideMedicationInfo",
            description="Provide a description for a given medicament ",
            sample_utterances=[
                lex.CfnBot.SampleUtteranceProperty(utterance="Give me informations about {MedicationName} "),
                lex.CfnBot.SampleUtteranceProperty(utterance="could you give me informations about medicaments "),
                lex.CfnBot.SampleUtteranceProperty(utterance="What are the second effects of {MedicationName} ?"),
                lex.CfnBot.SampleUtteranceProperty(utterance="How to use {MedicationName} ?"),
                lex.CfnBot.SampleUtteranceProperty(utterance="what's a {MedicationName} ?"),
                lex.CfnBot.SampleUtteranceProperty(utterance="what's an {MedicationName} ?"),
                
            ],
            slots=[
                lex.CfnBot.SlotProperty(
                    name="MedicationName",
                    slot_type_name="AMAZON.AlphaNumeric",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="Sure , what's the name of the medicament you want to ask about?"
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
                    slot_name="MedicationName",
                    priority=1
                ),
                
            ],
            dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                enabled=True
            ),
            fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                enabled=True
            )
        )

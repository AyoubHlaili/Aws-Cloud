from aws_cdk import (
    aws_lex as lex,
)



def get_symptoms_info():
    return lex.CfnBot.IntentProperty(
        name="GetSymptomsInfo",
        description="Provide medical advice based on the user's symptoms",
        sample_utterances=[
            lex.CfnBot.SampleUtteranceProperty(utterance="I have been sick lately"),
            lex.CfnBot.SampleUtteranceProperty(utterance="I am sick "),
            lex.CfnBot.SampleUtteranceProperty(utterance="i don't feel good "),
            lex.CfnBot.SampleUtteranceProperty(utterance="I have some trouble lately "),
            lex.CfnBot.SampleUtteranceProperty(utterance="i'm sick "),
            lex.CfnBot.SampleUtteranceProperty(utterance="i need symptoms advice "),
            lex.CfnBot.SampleUtteranceProperty(utterance="I am not feeling well "),
            lex.CfnBot.SampleUtteranceProperty(utterance="i'm tired ")
        ],
        slots=[
            lex.CfnBot.SlotProperty(
                name="Symptoms",
                slot_type_name="AMAZON.AlphaNumeric",
                value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="Required",
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        message_groups_list=[
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="Please describe the symptom you're experiencing."
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
                slot_name="Symptoms",
                priority=1
            )
            
        ],
        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
            enabled=True
        ),
        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
            enabled=True,
        ),
    )

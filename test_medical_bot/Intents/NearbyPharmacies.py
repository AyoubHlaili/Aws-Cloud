from aws_cdk import (
    aws_lex as lex,
)

def find_nearest_pharmacy_intent():
    return lex.CfnBot.IntentProperty(
        name="FindNearestPharmacy",
        description="Find the nearest pharmacy based on user location",
        sample_utterances=[
            lex.CfnBot.SampleUtteranceProperty(utterance="Find the nearest pharmacy near me"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Where is the closest pharmacy?"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Show me the nearest pharmacy"),
            lex.CfnBot.SampleUtteranceProperty(utterance="I need to find a pharmacy close by")
        ],
        slots=[
            lex.CfnBot.SlotProperty(
                name="Location",
                slot_type_name="AMAZON.City",  # Or another appropriate slot type
                value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                    slot_constraint="Required",
                    prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                        message_groups_list=[
                            lex.CfnBot.MessageGroupProperty(
                                message=lex.CfnBot.MessageProperty(
                                    plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                        value="Please provide your location or city."
                                    )
                                )
                            )
                        ],
                        max_retries=2,
                        allow_interrupt=False
                    )
                )
            )
        ],
        slot_priorities=[
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="Location",
                    priority=1
                ),
        ],
        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
            enabled=True
        ),
        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
            enabled=True
        ),
    )

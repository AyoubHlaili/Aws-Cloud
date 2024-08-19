from aws_cdk import aws_lex as lex

def cancel_home_healthcare_intent():
    return lex.CfnBot.IntentProperty(
        name="CancelHomeHealthcare",
        description="Intent to cancel a home healthcare appointment",
        sample_utterances=[
            lex.CfnBot.SampleUtteranceProperty(utterance="I want to cancel my appointment"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Cancel my healthcare appointment"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Cancel the home healthcare service")
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
            )
        ],
        slot_priorities=[
            lex.CfnBot.SlotPriorityProperty(slot_name="FullName", priority=1)
        ],
        dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(enabled=True),
        fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(enabled=True)
    )

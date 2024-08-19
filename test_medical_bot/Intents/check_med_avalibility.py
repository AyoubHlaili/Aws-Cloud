from aws_cdk import (
    aws_lex as lex,
)
# Define the custom slot type
def check_med_availability():
    return lex.CfnBot.IntentProperty(
            name="CheckMedicationAvailability",
            description="Check if a specific medication is available",
            sample_utterances=[
                lex.CfnBot.SampleUtteranceProperty(utterance="Is {Medication} available?"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Do you have {Medication} in stock?"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Can I get {Medication} ?"),
                lex.CfnBot.SampleUtteranceProperty(utterance="I am looking for a medication ")
            ],
            slots=[
                lex.CfnBot.SlotProperty(
                    name="Medication",
                    slot_type_name="AMAZON.AlphaNumeric",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="Which medication are you looking for?"
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
                    name="Quantity",
                    slot_type_name="AMAZON.Number",
                    value_elicitation_setting=lex.CfnBot.SlotValueElicitationSettingProperty(
                        slot_constraint="Required",
                        prompt_specification=lex.CfnBot.PromptSpecificationProperty(
                            message_groups_list=[
                                lex.CfnBot.MessageGroupProperty(
                                    message=lex.CfnBot.MessageProperty(
                                        plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                            value="How many units do you need?"
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
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="Medication",
                    priority=1
                ),
                lex.CfnBot.SlotPriorityProperty(
                    slot_name="Quantity",
                    priority=2
                ),
            ],
            dialog_code_hook=lex.CfnBot.DialogCodeHookSettingProperty(
                enabled=True
            ),
            fulfillment_code_hook=lex.CfnBot.FulfillmentCodeHookSettingProperty(
                enabled=True
            )
        )

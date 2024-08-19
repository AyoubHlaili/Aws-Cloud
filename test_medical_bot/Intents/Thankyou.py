from aws_cdk import (
    aws_lex as lex,
)
import random

def thankyou():
    # Randomly select one of the messages
    selected_message = random.choice([
        "You're welcome !",
        
    ])

    return lex.CfnBot.IntentProperty(
        name="ThankYou",
        description="Thank you message",
        sample_utterances=[
            lex.CfnBot.SampleUtteranceProperty(utterance="Thank you"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Thanks"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Thank you very much"),
            lex.CfnBot.SampleUtteranceProperty(utterance="I appreciate that !"),
        ],
        intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
            closing_response=lex.CfnBot.ResponseSpecificationProperty(
                message_groups_list=[
                    lex.CfnBot.MessageGroupProperty(
                        message=lex.CfnBot.MessageProperty(
                            plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                value=selected_message
                            )
                        )
                    )
                ],
                allow_interrupt=False
            )
        )
    )

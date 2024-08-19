from aws_cdk import (
    aws_lex as lex,
)
import random

def greeting():
    # Randomly select one of the messages
    selected_message = random.choice([
        "Hi, How can I help you today?",
        "Hi! I am your medical assistant. What symptoms are you experiencing?"
    ])

    return lex.CfnBot.IntentProperty(
        name="Greeting",
        description="Greeting intent",
        sample_utterances=[
            lex.CfnBot.SampleUtteranceProperty(utterance="Hey"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Hi"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Hello"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Hey MedicalBot"),
            lex.CfnBot.SampleUtteranceProperty(utterance="Good morning")
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

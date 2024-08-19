from aws_cdk import (
    aws_lex as lex,
)
import random

def goodbye():
    # Randomly select one of the messages
    selected_message = random.choice([
        "Goodbye! Take care.",
        "See you soon! Stay safe.",
        "Goodbye! Have a nice day."
    ])

    return lex.CfnBot.IntentProperty(
            name="Goodbye",
            description="Say goodbye to the user",
            sample_utterances=[
                lex.CfnBot.SampleUtteranceProperty(utterance="Goodbye"),
                lex.CfnBot.SampleUtteranceProperty(utterance="See you soon"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Have a nice day"),
                lex.CfnBot.SampleUtteranceProperty(utterance="Bye ")
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

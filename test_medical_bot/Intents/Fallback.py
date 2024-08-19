from aws_cdk import (
    aws_lex as lex,
)

def fallback():
    return lex.CfnBot.IntentProperty(
            name="FallbackIntent",
            description="Default intent when no other intent matches",
            parent_intent_signature="AMAZON.FallbackIntent",
            intent_closing_setting=lex.CfnBot.IntentClosingSettingProperty(
                closing_response=lex.CfnBot.ResponseSpecificationProperty(
                    message_groups_list=[
                        lex.CfnBot.MessageGroupProperty(
                            message=lex.CfnBot.MessageProperty(
                                plain_text_message=lex.CfnBot.PlainTextMessageProperty(
                                    value="I'm sorry, I didn't understand that. Can you please rephrase?"
                                )
                            )
                        )
                    ],
                    allow_interrupt=False
                )
            )
        )


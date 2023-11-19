import os
import sys

from openai import OpenAI
import config

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def translate_to_chinese(text):
    text = check_input(text)
    if text:
        user_content = f"Please translate the following text in the triple backtick and only response with the translated content." \
                       f"You can alter the translated word order to make the translation more comprehensive." \
                       f"```{text}```" \
            # f"If there is no text in the previous triple backtick, please respond with only" \
        # f"'Please provide the text to be translated into Chinese.'."

        response = client.chat.completions.create(
            model=config.MODEL_SELECTION,
            messages=[
                {
                    "role": "system",
                    "content": config.TRAN_SYSTEM_MSG
                },
                {
                    "role": "user",
                    "content": user_content,
                },

            ],
            max_tokens=config.MAX_TOKEN,

            # What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
            temperature=config.TEMPERATURE,

            # Number between -2.0 and 2.0.
            # Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
            presence_penalty=0.03,

            # Number between -2.0 and 2.0.
            # Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
            frequency_penalty=0.02,
            # stream=True,

        )

        response_content = response.choices[0].message.content
        return remove_backtick(response_content)

    return ""


def remove_backtick(text):
    # remove all the backtick
    text = text.replace("`", "")
    return text


def check_input(text):
    # check if the user's input is valid:
    # 1. the input should be a string

    if not isinstance(text, str):
        print("Please provide the text to be translated into Chinese.")
        return None

    if (text is None) or (text == ""):
        print("Please provide the text to be translated into Chinese.")
        return None

    # remove all the backtick

    return remove_backtick(text)


if __name__ == '__main__':
    # Figure of the day: One-third, the share of American women of reproductive age that would have to drive more than
    # an hour to get an abortion. Read the full story.

    # read input from the cli arguments
    english_text = sys.argv[1].strip()
    if isinstance(english_text, str):
        translated_chinese = translate_to_chinese(english_text)
        print(translated_chinese)
    else:
        print("Please provide the text to be translated into Chinese.")

"""
The `max_tokens` is altered to adapt to the specific scenario in Alfred
And there is no need to remove backtick.
"""
import os
import sys

import openai
import requests
from openai import OpenAI

import config

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TERMINAL = os.getenv('GPT_IN_TERMINAL', default=False)
if TERMINAL == "1":
    TERMINAL = True


def chat(text):
    text = check_input(text)

    system_msg = config.CHAT_SYSTEM_MSG

    if text:
        user_content = f"{text}"

        try:
            response = client.chat.completions.create(
                model=config.MODEL_SELECTION,
                messages=[
                    {
                        "role": "system",
                        "content": system_msg,
                    },
                    {
                        "role": "user",
                        "content": user_content,
                    },

                ],

                max_tokens=config.MAX_TOKEN,

                # What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random
                # while lower values like 0.2 will make it more focused and deterministic.
                temperature=config.TEMPERATURE,

                # Number between -2.0 and 2.0.
                # Positive values penalize new tokens based on whether they appear in the text so far
                # increasing the model's likelihood to talk about new topics.
                presence_penalty=0.05,

                # Number between -2.0 and 2.0.
                # Positive values penalize new tokens based on their existing frequency in the text so far
                # decreasing the model's likelihood to repeat the same line verbatim.
                frequency_penalty=0.05,

                # why not? because in alfred, the output is only obtained by after executing current one.
                # if it is in the terminal mode, the output will be printed out immediately simulating the ChatGPT.
                stream=TERMINAL,

            )
        except (requests.exceptions.ConnectionError, openai.APIConnectionError) as e:
            return "[ERROR] Please check your network proxy settings."

        if TERMINAL:
            response_content = ""
            print("GPT:", end=" ")
            try:
                for chunk in response:
                    if (chunk.choices[0].finish_reason != "stop") and \
                            (chunk.choices[0].finish_reason != "length"):

                        chunk_message = chunk.choices[0].delta.content  # extract the message
                        response_content += chunk_message
                        print(chunk_message, end="")
                        sys.stdout.flush()
                    else:
                        response_content += "\n"
                        print()
                        sys.stdout.flush()
            except KeyboardInterrupt:
                return ""  # return nothing because the content has already generated or not satisfied by the user

            return ""

        response_content = response.choices[0].message.content
        return response_content

    return ""


def remove_backtick(text):
    # remove all the backtick
    text = text.replace("`", "")
    return text


def check_input(text):
    # check if the user's input is valid:
    # 1. the input should be a string

    if (not isinstance(text, str)) or (text == ""):
        print("Please provide the text to ask GPT.")
        return None

    # if (text is None) or (text == ""):
    #     print("Please provide the text to ask GPT.")
    #     return None

    # remove all the backtick

    # No need to remove backtick for now
    # return remove_backtick(text)
    return text


if __name__ == '__main__':
    openai.api_key = os.environ['OPENAI_API_KEY']
    user_input = ""

    # read input from the cli arguments
    try:
        user_input = sys.argv[1].strip()
    except IndexError:
        user_input = ""

    if isinstance(user_input, str):
        output = chat(user_input)
        if not TERMINAL:
            print(output)
    else:
        print("Please provide the text to be asked to GPT.")

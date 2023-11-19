# write the base64 to files:
import base64
import os.path
import sys
from datetime import datetime

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# TODO: extract the path to alfred environmental variable
path = "/tmp/openai/dalle/"
if not os.path.exists(path):
    os.makedirs(path)
abs_path = os.path.abspath(path)


def image_generation(prompt):
    """
    prompt: string Required
    A text description of the desired image(s). The maximum length is 1000 characters.

    n: integer Optional, Defaults to 1
    The number of images to generate. Must be between 1 and 10.

    size: string Optional, Defaults to 1024x1024
    The size of the generated images. Must be one of 256x256, 512x512, or 1024x1024.

    response_format: string Optional, Defaults to url
    The format in which the generated images are returned. Must be one of url or b64_json.

    user: string Optional
    A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Learn more.
    :return: image base64
    """

    response = client.images.generate(prompt=prompt,
    n=1,
    size="1024x1024",
    response_format="b64_json")

    image_base_64 = response.data[0].b64_json

    return image_base_64


def get_filename(prompt):
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = "_".join(prompt.lower().split()[:8]) + "_" + current_time + ".png"
    return filename


def save_file(image_b64, filename):
    filepath = os.path.join(abs_path, filename)
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(image_b64))
    return filepath


# with open("/tmp/openai/dalle/", "wb") as fh:
#     fh.write(img_data.decode('base64'))

if __name__ == '__main__':
    

    # prompt = "a close-up photographic white Siamese cat with blue eyes with detailed fur and whiskers"
    prompt = sys.argv[1]
    image_b64 = image_generation(prompt)
    filepath = save_file(image_b64, get_filename(prompt))
    print(filepath)

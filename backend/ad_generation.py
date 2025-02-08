from openai import OpenAI
import json
from typing import List
# from dotenv import load_dotenv
# from models import *
import os

from google import genai



def generate_image(prompt):
    client = OpenAI()

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    print(response.data[0].url)

def generate_prompt(audience_info, brand_info):

    prompt = f"Generate a prompt for an image generation model to generate personal \
            and specialized ads based on some general characteristics of the consumers. \
            Add a phrase that reflects the selling point of the product. The product: {brand_info['Product description']} \
            should be at the spotlight in the ad. The ad design should have both the target audience and company characters in \
            mind. These characteristics are {audience_info} and {brand_info}. THE OUTPUT SHOULD JUST BE THE PROMPT"
    
    client = genai.Client(api_key="AIzaSyA892rZ2Eqj4okrBGqH2gKHZRAsdZJNyz4")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    print(response.text)

    # client = OpenAI(
    #     api_key=os.getenv("OPENAI_API_KEY"),
    # )

    
    
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are an AI that generate non-generic prompts for image generation."},
    #         {"role": "user", "content": prompt}
    #     ]
    # )

    # result = response.choices[0].message.content

    # print(result)


def main():
    audience_info = {
        "Interest & Behaviors": "Fashion",
        "Age Range": "20-30",
        "Income Range": "N/A",
        "Gender": "Male",
        "Marital Status": "unmarried",
        "Employment status": "unemployed",
        "Occupation type": "N/A",
        "Personality type" "ENFJ"
        "Demographic detail": "teacher",
        "Country": "China"
    }

    brand_info = {
        "Company Logo": "N/A",
        "Company Color": "Yellow and Purple",
        "Company Description": "N/A",
        "Company Tagline": "N/A",
        "Product image": "N/A",
        "Product description": "blackhead remover vacuum",
        "Price range": "12000",
        "Produce category": "N/A",
        "Target emotions": "Anger"
    }
    
    prompt = generate_prompt(audience_info, brand_info)


if __name__ == "__main__":
    main()

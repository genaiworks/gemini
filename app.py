from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os 
from PIL import Image 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def get_gemini_response(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0],prompt],safety_settings=safety_settings)
    for candidate in response.candidates:
        return [part.text for part in candidate.content.parts]

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Multi Language Invoice Extractor")
st.header("Gemini Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice... ", type=["jpg", "jpeg", "png", "img"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image. ", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt ="""
You are an expert in understanding invoices.  We will upload an image as invoices
and you will have to answer any question based on the uploaded invoice image.
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data,input)
    st.subheader("The response is")
    st.write(response)


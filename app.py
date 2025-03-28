from dotenv import load_dotenv
load_dotenv()  # Load all environment variables

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini pro vision
model = genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(prompt, image, user_input):
    response = model.generate_content([prompt, image[0], user_input])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type of uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit setup
st.set_page_config(page_title="MultiLanguage Invoice Extractor")

user_input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image ....", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as an invoice,
and you will have to answer any question based on the uploaded invoice image.
"""

# If submit button is clicked
if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, user_input)
    st.subheader("The response is:")
    st.write(response)

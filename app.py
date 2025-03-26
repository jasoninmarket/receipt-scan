import streamlit as st
import google.generativeai as genai
import json
from PIL import Image

# Configure Gemini API (Replace with your API key)
genai.configure(api_key="AIzaSyBmKp3dKS0Q-Wz8epZfpLvm3d1np_DJTJs")
model = genai.GenerativeModel('gemini-2.0-flash')  # Updated to latest model

# Streamlit UI
st.title("Clarity Rewards - Receipt Scanner")

uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    if st.button("Extract Receipt Data"):

        try:
            # Gemini prompt for receipt data extraction
            prompt = """
            Extract the following information from this receipt:
            - Store Name
            - Date
            - List of items (name, quantity, price)
            - Total Amount
            Return the result as a json object.
            """

            # Gemini API call, directly sending the image object.
            response = model.generate_content([prompt, image])

            # Parse Gemini's JSON response
            extracted_data = response.text

            try:
                extracted_json = json.loads(extracted_data) # Use json.loads for safety
                st.success("Receipt data extracted successfully!")
                st.json(extracted_json)

            except json.JSONDecodeError:
                st.error("Gemini returned non-json data. Displaying raw text.")
                st.write(extracted_data)

        except Exception as e:
            st.error(f"Error processing receipt: {e}")
import streamlit as st
import requests
import base64
import io
from PIL import Image
import google.generativeai as genai

# Configure Gemini API (Replace with your API key)
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro-vision')

# Streamlit UI
st.title("Clarity Rewards - Receipt Scanner")

uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    if st.button("Extract Receipt Data"):
        # Convert image to base64 for Gemini
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")  # Or PNG, depending on your needs
        img_bytes = buffered.getvalue()

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

            # Gemini API call
            response = model.generate_content([prompt, img_bytes])
            response.raise_for_block_filter() # Ensure no unsafe content

            # Parse Gemini's JSON response
            extracted_data = response.text

            try:
                extracted_json = eval(extracted_data) #eval is unsafe for production, use json.loads.
                st.success("Receipt data extracted successfully!")
                st.json(extracted_json)

            except:
                st.error("Gemini returned non-json data. Displaying raw text.")
                st.write(extracted_data)

        except Exception as e:
            st.error(f"Error processing receipt: {e}")

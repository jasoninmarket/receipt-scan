import streamlit as st
import requests
import base64
import io
from PIL import Image

# Streamlit UI
st.title("Clarity Rewards - Receipt Scanner")

uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    if st.button("Scan Receipt"):
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")  # Or PNG, depending on your needs
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Backend API call (replace with your server URL)
        api_url = "YOUR_NODE_SERVER_URL/scan-receipt"
        payload = {"imageBase64": img_str, "userId": "user123"}  # Replace user123

        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            result = response.json()
            if result["success"]:
                st.success("Receipt scanned successfully!")
                st.json(result["data"])
            else:
                st.error(f"Error: {result['error']}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")

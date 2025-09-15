import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

# Load the CSV file
df = pd.read_csv("data.csv")

# Function to get the closest color name from CSV
def get_closest_color_name(R, G, B):
    minimum = float('inf')
    cname = None
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, "name"]   # ✅ fixed column name
    return cname

# Streamlit app
st.title("🎨 Color Detection App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Open image with PIL
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to OpenCV format
    img = np.array(image)
    if img.shape[-1] == 4:  # handle RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # Click position input
    x = st.number_input("Enter X coordinate", min_value=0, max_value=img.shape[1]-1, value=0)
    y = st.number_input("Enter Y coordinate", min_value=0, max_value=img.shape[0]-1, value=0)

    if st.button("Detect Color"):
        B, G, R = img[int(y), int(x)]
        color_name = get_closest_color_name(R, G, B)
        st.write(f"**Detected Color:** {color_name}")
        st.write(f"RGB: ({R}, {G}, {B})")

        # Show color preview
        st.markdown(
            f"<div style='width:100px;height:100px;background-color:rgb({R},{G},{B});'></div>",
            unsafe_allow_html=True
        )


import streamlit as st
import numpy as np
from PIL import Image
import requests

st.set_page_config(layout="centered")  # keeps the layout tight

# --- Enhancement functions ---
def enhance_red_areas(img_rgb, strength=1.5, red_threshold=0.2):
    img_float = img_rgb.astype(np.float32) / 255.0
    red_channel = img_float[:, :, 0]
    green_channel = img_float[:, :, 1]
    blue_channel = img_float[:, :, 2]

    red_mask = (red_channel > red_threshold) & (red_channel > green_channel) & (red_channel > blue_channel)
    enhanced = img_float.copy()
    enhanced[:, :, 0][red_mask] *= strength
    enhanced = np.clip(enhanced, 0, 1)
    return (enhanced * 255).astype(np.uint8)

def enhance_red_green_areas(img_rgb, red_strength=1.6, green_strength=1.2, threshold=0.15):
    img_float = img_rgb.astype(np.float32) / 255.0
    red, green, blue = img_float[:, :, 0], img_float[:, :, 1], img_float[:, :, 2]

    red_mask = (red > threshold) & (red > green) & (red > blue)
    green_mask = (green > threshold) & (green > red) & (green > blue)

    enhanced = img_float.copy()
    enhanced[:, :, 0][red_mask] *= red_strength
    enhanced[:, :, 1][green_mask] *= green_strength

    enhanced = np.clip(enhanced, 0, 1)
    return (enhanced * 255).astype(np.uint8)

def enhance_rgb_areas(img_rgb, red_strength=1.7, green_strength=1.3, blue_strength=1.1, threshold=0.1):
    img_float = img_rgb.astype(np.float32) / 255.0
    red, green, blue = img_float[:, :, 0], img_float[:, :, 1], img_float[:, :, 2]

    red_mask = (red > threshold) & (red > green) & (red > blue)
    green_mask = (green > threshold) & (green > red) & (green > blue)
    blue_mask = (blue > threshold) & (blue > red) & (blue > green)

    enhanced = img_float.copy()
    enhanced[:, :, 0][red_mask] *= red_strength
    enhanced[:, :, 1][green_mask] *= green_strength
    enhanced[:, :, 2][blue_mask] *= blue_strength

    enhanced = np.clip(enhanced, 0, 1)
    return (enhanced * 255).astype(np.uint8)

# --- UI ---
st.markdown("""
    <div style='text-align: center; max-width: 800px; margin: auto;'>
        <h1>🤿 Underwater Color Correction Tool</h1>
        <p>Upload your underwater photo, then choose the approximate depth.  
        The app will intelligently enhance red, green, and blue tones lost due to underwater color absorption.</p>
    </div>
""", unsafe_allow_html=True)

# Upload image
uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
else:
    st.info("No image uploaded. Using a sample image.")
    image = Image.open(requests.get(
        "https://i.kym-cdn.com/entries/icons/facebook/000/022/747/Do_Something_meme_banner_imag.jpg", 
        stream=True).raw).convert("RGB")

# Convert to array
img_rgb = np.array(image)

depth_choice = st.selectbox("🌊 Approximate Depth (meters)", [5, 10, 15, 20, 25, 30])

st.markdown("### 🎛️ Adjust enhancement strength")

if depth_choice <= 10:
    red_strength = st.slider("🔴 Red Strength", 0.5, 2.0, 1.5, 0.1)
    enhanced_img = enhance_red_areas(img_rgb, strength=red_strength, red_threshold=0.15)

elif depth_choice <= 20:
    red_strength = st.slider("🔴 Red Strength", 0.5, 2.0, 1.6, 0.1)
    green_strength = st.slider("🟢 Green Strength", 0.5, 2.0, 1.2, 0.1)
    enhanced_img = enhance_red_green_areas(img_rgb, red_strength=red_strength, green_strength=green_strength, threshold=0.12)

else:
    red_strength = st.slider("🔴 Red Strength", 0.5, 2.0, 1.7, 0.1)
    green_strength = st.slider("🟢 Green Strength", 0.5, 2.0, 1.3, 0.1)
    blue_strength = st.slider("🔵 Blue Strength", 0.5, 2.0, 1.1, 0.1)
    enhanced_img = enhance_rgb_areas(
        img_rgb,
        red_strength=red_strength,
        green_strength=green_strength,
        blue_strength=blue_strength,
        threshold=0.1
    )
# Display both images
tab1, tab2 = st.tabs(["🎨 Color Corrected", "📷 Original"])
tab1.image(enhanced_img, caption="Corrected image (~{}m)".format(depth_choice))
tab2.image(img_rgb, caption="Original image")
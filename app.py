import streamlit as st
import pandas as pd

from model.image_captioning import generate_from_image
from model.caption_generator import generate_caption
from model.hashtag_generator import suggest_hashtags

st.set_page_config(page_title="InfluenceBuddy", layout="wide")

st.sidebar.title("📂 InfluenceBuddy")
section = st.sidebar.radio("Navigate", [
    "Home", 
    "Upload CSV", 
    "Dashboard", 
    "Caption Generator", 
    "Hashtag Tool", 
    "Image Caption & Hashtag"
])

# 🔁 Initialize df globally in session state
if "df" not in st.session_state:
    st.session_state.df = None

# 🏠 Home Section
if section == "Home":
    st.title("🏆 Welcome to InfluenceBuddy")
    st.write("Helping beginner influencers grow smarter with AI-powered insights, captions, and strategies.")

# 📁 Upload CSV Section
elif section == "Upload CSV":
    st.title("📁 Upload Your Instagram Data")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success("✅ File uploaded successfully.")
            st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# 📊 Dashboard Section
elif section == "Dashboard":
    st.title("📊 Performance Dashboard")
    df = st.session_state.df
    
    if df is not None:
        try:
            st.line_chart(df[["Likes", "Comments", "Reach", "Saves"]])
        except KeyError:
            st.warning("⚠️ Please make sure your CSV has columns: Likes, Comments, Reach, Saves")
    else:
        st.warning("❗ Please upload a CSV first from the 'Upload CSV' section.")

# ✍️ Caption Generator
elif section == "Caption Generator":
    st.title("✍️ Caption Generator")
    topic = st.text_input("Enter a topic")
    tone = st.selectbox("Select a tone", ["Friendly", "Professional", "Funny", "Inspirational"])
    platform = st.selectbox("Select your platform", ["Instagram", "LinkedIn"])
    category = st.selectbox("Select content category", ["Lifestyle", "Food", "Tech", "Fashion"])

    if st.button("Generate Captions"):
        if topic:
            caption = generate_caption(topic, tone, platform, category)
            st.subheader("Generated Caption")
            st.write(caption)
        else:
            st.warning("⚠️ Please enter a topic.")

# 📌 Hashtag Recommender
elif section == "Hashtag Tool":
    st.title("📌 Hashtag Recommender")
    topic = st.text_input("Enter your post topic")
    category = st.selectbox("Select content category", ["Lifestyle", "Food", "Tech", "Fashion"])

    if st.button("Suggest Hashtags"):
        if topic:
            hashtags = suggest_hashtags(topic, category)
            st.success("✅ Suggested Hashtags:")
            st.write(", ".join(hashtags))
        else:
            st.warning("⚠️ Please enter a topic.")

# 🖼️ Image Caption & Hashtag
elif section == "Image Caption & Hashtag":
    st.title("🖼️ Image Caption & Hashtag")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

        if st.button("Generate from Image"):
            caption, hashtags = generate_from_image(uploaded_image)
            st.subheader("Generated Caption")
            st.write(caption)

            st.subheader("Suggested Hashtags")
            st.write(", ".join(hashtags))

import streamlit as st
import pandas as pd
from datetime import datetime


from model.image_captioning import generate_from_image
from model.caption_generator import generate_caption
from model.hashtag_generator import suggest_hashtags

st.set_page_config(page_title="InfluenceBuddy", layout="wide")

st.sidebar.title("InfluenceBuddy")
section = st.sidebar.radio("Navigate", [
    "Home",
    "Upload CSV",
    "Dashboard",
    "Caption Generator",
    "Hashtag Tool",
    "Image Caption & Hashtag"
])

# Initialize df globally in session state
if "df" not in st.session_state:
    st.session_state.df = None

# Home Section
if section == "Home":
    st.title("🏆 Welcome to InfluencerBuddy")
    st.markdown("""
    ## Welcome to InfluenceBuddy 💡

    **InfluenceBuddy** is an AI-powered platform designed to help **influencers, content creators, and marketers** grow smarter and faster by understanding their audience better.

    ### 🔍 What does this app do?

    - 📈 Analyze your social media performance using uploaded CSV data  
    - 🧠 Generate smart, engaging **captions** for your posts based on tone and category  
    - 🏷️ Suggest high-performing **hashtags** that suit your content  
    - 🖼️ Create **image-based captions & hashtags** using AI  
    - 📅 Discover the **best days & times to post** to maximize reach and engagement  
    - 📊 View personalized **visual dashboards** to track likes, comments, and shares over time  

    ### 📁 How to Get Started:

    1. Upload your **social media CSV file** from the sidebar under 'Upload CSV'  
    2. Navigate to the **Dashboard** to analyze your performance  
    3. Use the **Caption Generator**, **Hashtag Tool**, and **Image Captioning** tools to enhance your content  
    4. Optimize your strategy using data insights  

    ---
    ### 📥 Supported Platforms:

    - **Instagram**  
    - **YouTube**  
    - **Facebook**  
    - **Twitter (X)**  
    - **LinkedIn**

    ### 📤 How to Get Your CSV File:

    - **Instagram**: Go to *Settings → Your Activity → Download Your Information*  
    - **Facebook**: Go to *Settings → Your Facebook Information → Download Your Information*  
    - **Twitter (X)**: Go to *Settings → Account → Download an archive of your data*  
    - **YouTube**: Visit Google Takeout and select YouTube  
    - **LinkedIn**: *Settings & Privacy → Get a copy of your data*

    ---

    Whether you're just starting your influencer journey or want to boost your growth,  
    **InfluenceBuddy is here to support you every step of the way. 💫**
    """)

# Upload CSV Section
elif section == "Upload CSV":
    st.title("📁 Upload Your Instagram Data")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.success("✅ File uploaded successfully.")
            st.dataframe(df)
            st.write("📄 Columns detected in CSV:", df.columns.tolist())
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

# Dashboard Section
elif section == "Dashboard":
    st.title("📊 Performance Dashboard")
    df = st.session_state.df  # Use uploaded file

    if df is None:
        st.warning("⚠️ Please upload your CSV first from the 'Upload CSV' section.")
        st.stop()

    try:
        # Overall engagement chart
        st.subheader("📈 Engagement Overview")
        engagement_cols = [col for col in ["likes", "comments", "shares"] if col in df.columns]
        if engagement_cols:
            st.line_chart(df[engagement_cols])
        else:
            st.info("ℹ️ No 'likes', 'comments', or 'shares' columns found in your data.")

        # Average Likes by Day
        if 'post_day' in df.columns:
            st.subheader("🗓️ Average Likes by Day")
            day_avg = df.groupby('post_day')['likes'].mean().sort_values(ascending=False)
            st.bar_chart(day_avg)
        else:
            st.info("ℹ️ 'post_day' column not found for day-wise analysis.")

        # Average Likes by Hour
        if 'post_time' in df.columns:
            df['hour'] = pd.to_datetime(df['post_time'], errors='coerce').dt.hour
            st.subheader("⏰ Average Likes by Hour")
            hour_avg = df.groupby('hour')['likes'].mean().sort_index()
            st.line_chart(hour_avg)
        else:
            st.info("ℹ️ 'post_time' column not found for hour-wise analysis.")

        # Likes by Post Type
        if 'post_type' in df.columns:
            st.subheader("📌 Average Likes by Post Type")
            type_avg = df.groupby('post_type')['likes'].mean().sort_values(ascending=False)
            st.bar_chart(type_avg)
        else:
            st.info("ℹ️ 'post_type' column not found for post type analysis.")

    except KeyError as e:
        st.warning(f"⚠️ Missing expected columns: {e}")

# Caption Generator
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

# Hashtag Recommender
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

# Image Caption & Hashtag
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

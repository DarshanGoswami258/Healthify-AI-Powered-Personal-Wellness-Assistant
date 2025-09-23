import streamlit as st
import google.generativeai as genai
import pandas as pd
import os

# Configure API
api = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# App Title
st.title("🧑‍⚕️ :orange[Healthify] – :blue[AI Powered Personal Health Assistant]")
st.markdown(
    """
    ### 🌱 Your AI partner for a healthier lifestyle  
    This application helps you understand your health better and provides **personalized guidance**.  
    """
)

# Sidebar for user details
st.sidebar.header("📝 Enter Your Details")
Name = st.sidebar.text_input("👤 Name")
gender = st.sidebar.selectbox("⚧ Gender", ["Male", "Female", "Other"])
age = st.sidebar.number_input("🎂 Age (Years)", min_value=1, max_value=120, step=1)
height = st.sidebar.number_input("📏 Height (cm)", min_value=50, max_value=250, step=1)
weight = st.sidebar.number_input("⚖️ Weight (kg)", min_value=10, max_value=250, step=1)
fitness = st.sidebar.slider("💪 Fitness Level (0-5)", 0, 5, 3)

# BMI Calculation
if height > 0 and weight > 0:
    bmi = weight / ((height / 100) ** 2)
    st.sidebar.success(f"📊 {Name}, your BMI is **{round(bmi,2)} kg/m²**")

    # BMI category message
    if bmi < 18.5:
        st.sidebar.info("⚠️ You are underweight")
    elif 18.5 <= bmi < 24.9:
        st.sidebar.success("✅ You have a healthy weight")
    elif 25 <= bmi < 29.9:
        st.sidebar.warning("⚠️ You are overweight")
    else:
        st.sidebar.error("🚨 You fall in the obese range")

# Tips section
with st.expander("📌 How to use this assistant"):
    st.markdown(
        """
        1. Fill in your **personal details** in the sidebar.  
        2. Enter your **health-related question** below.  
        3. Get **personalized, AI-powered advice** in seconds.  
        """
    )

# User query
user_query = st.text_input("💬 Enter your health question:")

# Prompt to GenAI
prompt = f"""
Assume you are a Health Expert. Answer the question asked by the user using these details:

- Name: {Name}
- Gender: {gender}
- Age: {age}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {round(bmi,2) if height > 0 else 'N/A'} kg/m²
- Fitness Rating: {fitness}/5

Format the response as:
- A short personalized comment on the details provided.
- Explain the core issue based on the query.
- Possible reasons for the problem.
- Suggested lifestyle/health solutions.
- Which doctor (specialization) to see, if needed.
- Strictly do not recommend any medicines.
- Use bullet points and tables wherever required.
- End with a 5–7 line summary.

User query: {user_query}
"""

# Generate response
if user_query:
    response = model.generate_content(prompt)
    st.subheader("🤖 Your Healthify Assistant’s Advice")
    st.markdown(
        f"""
        <div style="background-color:#f9f9f9; padding:15px; border-radius:12px; border:1px solid #ddd;">
        {response.text}
        </div>
        """,
        unsafe_allow_html=True,
    )

import streamlit as st
import google.generativeai as genai
import os

# ─────────────────────────────────────────────
# CONFIGURE API
# ─────────────────────────────────────────────
api = os.getenv("GOOGLE_API_KEY")

if not api:
    st.error("❌ API Key not found. Please set GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api)

# Use stable model
model = genai.GenerativeModel("gemini-1.5-flash")

# ─────────────────────────────────────────────
# APP TITLE
# ─────────────────────────────────────────────
st.title("🧑‍⚕️ :orange[Healthify] – :blue[AI Powered Personal Health Assistant]")
st.markdown(
    """
    ### 🌱 Your AI partner for a healthier lifestyle  
    Get simple, personalized health guidance based on your details.
    """
)

# ─────────────────────────────────────────────
# SIDEBAR INPUTS
# ─────────────────────────────────────────────
st.sidebar.header("📝 Enter Your Details")

Name = st.sidebar.text_input("👤 Name")
display_name = Name if Name else "User"

gender = st.sidebar.selectbox("⚧ Gender", ["Male", "Female", "Other"])
age = st.sidebar.number_input("🎂 Age (Years)", min_value=1, max_value=120, step=1)
height = st.sidebar.number_input("📏 Height (cm)", min_value=50, max_value=250, step=1)
weight = st.sidebar.number_input("⚖️ Weight (kg)", min_value=10, max_value=250, step=1)
fitness = st.sidebar.slider("💪 Fitness Level (0-5)", 0, 5, 3)

# ─────────────────────────────────────────────
# BMI CALCULATION
# ─────────────────────────────────────────────
bmi = None

if height > 0 and weight > 0:
    bmi = weight / ((height / 100) ** 2)
    bmi_value = round(bmi, 2)

    st.sidebar.success(f"📊 {display_name}, your BMI is **{bmi_value} kg/m²**")

    if bmi < 18.5:
        st.sidebar.info("⚠️ You are underweight")
    elif 18.5 <= bmi < 24.9:
        st.sidebar.success("✅ You have a healthy weight")
    elif 25 <= bmi < 29.9:
        st.sidebar.warning("⚠️ You are overweight")
    else:
        st.sidebar.error("🚨 You fall in the obese range")

# ─────────────────────────────────────────────
# HOW TO USE
# ─────────────────────────────────────────────
with st.expander("📌 How to use this assistant"):
    st.markdown(
        """
        1. Fill in your **personal details** in the sidebar  
        2. Ask a **health-related question**  
        3. Get **AI-powered guidance instantly**
        """
    )

# ─────────────────────────────────────────────
# USER INPUT
# ─────────────────────────────────────────────
user_query = st.text_input("💬 Enter your health question:")

# ─────────────────────────────────────────────
# GENERATE RESPONSE
# ─────────────────────────────────────────────
if st.button("🔍 Get Advice"):

    if not user_query:
        st.warning("⚠️ Please enter a health question.")
        st.stop()

    prompt = f"""
    You are a professional health expert.

    User details:
    - Name: {display_name}
    - Gender: {gender}
    - Age: {age}
    - Height: {height} cm
    - Weight: {weight} kg
    - BMI: {round(bmi,2) if bmi else 'N/A'} kg/m²
    - Fitness Rating: {fitness}/5

    Instructions:
    - Start with a short personalized comment
    - Explain the issue clearly
    - List possible reasons
    - Suggest lifestyle improvements
    - Recommend doctor type if needed
    - DO NOT suggest medicines
    - Use bullet points
    - End with a short 5–7 line summary

    User question: {user_query}
    """

    try:
        with st.spinner("🤖 Thinking..."):
            response = model.generate_content(prompt)

        st.subheader("🤖 Healthify Assistant")

        st.markdown(
            f"""
            <div style="background-color:#f9f9f9; padding:15px; border-radius:12px; border:1px solid #ddd;">
            {response.text}
            </div>
            """,
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")

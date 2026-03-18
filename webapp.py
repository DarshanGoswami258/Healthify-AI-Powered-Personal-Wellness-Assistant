import streamlit as st
import google.generativeai as genai
import os
import pandas as pd

api=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=api)

model=genai.GenerativeModel('gemini-2.5-flash-lite')

# lets create the UI
st.title(':orange[HEALTHIFY] :blue[AI Powered Personal Heath Assistant]')
st.markdown('''##### This application will assist you to have a better ans healthy life. You can ask your health related questions and get personalised guidance.''')
tips=''':orange[Follow the steps]
* Enter your details in the side bar.
* Enter your gender, age, height (cms), weight (kgs).
* Select the number on the fitness sacle (0-5). 5-Fittest and 0-Not Fit
* After filling the details write your  here and get customised response.'''
st.write(tips)

st.sidebar.header(':orange[ENTER YOUR DETAILS]')
name=st.sidebar.text_input('Enter your name')
gender=st.sidebar.selectbox('Gender',['Male','Female'])
age=st.sidebar.text_input('Age (Years)')
weight=st.sidebar.number_input('Weight (kgs)',min_value=0.0,value=70.0,step=0.1,format="%.1f")
height=st.sidebar.number_input('Height (cms)',min_value=0.0,value=140.0,step=0.1,format="%.1f")
bmi=pd.to_numeric(weight)/(pd.to_numeric(height)/100)**2
fitness=st.sidebar.slider('Rate your fitness between 0-5',0,5,step=1)
st.sidebar.write(f':orange[{name} BMI is {round(bmi,2)} kg/m^2]')

# lets use genai model to get the output
user_query=st.text_input('Enter your question here')
prompt=f''' Assume you are health expert. you are required to answer the question asked by the user. Use the following details provided by the user.
Gender of {name} is {gender}
Age of {name} is {age}
Weight of {name} is {weight} kgs
Height of {name} is {height} cms
BMI of {name} is {bmi} kg/m^2
ans {name} rates his/her fitness as {fitness} out of 5

Your output shall be in follwoing format:
* it should start by giving one two line comment on the details that have been given
* it should explain what the real problem is based on the query asked by user
* what could be the possible reason for the problem.
* What are the possible solutions for the problem.
* You can also mention what doctor to see (specialization) if required
* Strictily do not recommend any medicine even if asked
* Output should be in bullet points and use tables wherever required.
* try to add relevant images

here is the query from the user {user_query}'''

if user_query:
    response=model.generate_content(prompt)
    st.write(response.text)
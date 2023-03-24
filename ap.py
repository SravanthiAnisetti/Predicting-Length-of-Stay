import streamlit as st
import pandas as pd
import numpy as np
import pickle
from passlib.hash import pbkdf2_sha256

st.set_page_config(page_title='Predicting LOS',layout="wide")

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create a table for users if it does not already exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password_hash TEXT)''')
conn.commit()

# Function to add a new user to the database
def add_user(username, password):
    password_hash = pbkdf2_sha256.hash(password)
    c.execute(f"INSERT INTO users VALUES ('{username}', '{password_hash}')")
    conn.commit()
    

# Function to check if a username already exists in the database
def username_exists(username):
    c.execute(f"SELECT * FROM users WHERE username='{username}'")
    return c.fetchone() is not None

# Function to validate a password
def validate_password(password):
    if len(password) < 8:
        return False
    has_digit = False
    has_uppercase = False
    for char in password:
        if char.isdigit():
            has_digit = True
        elif char.isupper():
            has_uppercase = True
    return has_digit and has_uppercase


def main():
  st.title(" ")

pickle_in = open('rf.pkl', 'rb')
classifier = pickle.load(pickle_in)


def prediction(input_data):  
  input = np.asarray(input_data)
  sh = input.reshape(1,3)
  prediction = classifier.predict(sh)[0]
  print(prediction)
  return prediction

st.sidebar.subheader("Login Section")
    
form_container = st.sidebar.container()

def submitted():
    st.session_state.submitted = True
def reset():
    st.session_state.submitted = False

with form_container:
      with st.form("add user"):
            st.subheader('Enter your Credentials')
            username = st.text_input("User Name")
            password = st.text_input("Password",type='password')
            st.form_submit_button(label="Login", on_click=submitted)
        
st.sidebar.write("Don't have an account? ")

def logout():
    st.info('Thanks for visiting !!!!')
    st.stop()

if 'submitted' in st.session_state:
    if st.session_state.submitted == True:
     c.execute(f"SELECT * FROM users WHERE username='{username}'")
     user = c.fetchone()
     if not username:
            st.error("Please enter a username")
     elif not password:
            st.error("Please enter a password")

    if user is not None:
         if pbkdf2_sha256.verify(password, user[1]):
      
            st.success("Logged In as {}".format(username))
            col1, col2 = st.columns([9, 1])
            with col1:
              st.write("")
            with col2:
              if st.button('Logout', on_click=logout):
                pass
            st.title("Predicting Length of Stay for Hospital Inpatients")
          
            res = pd.read_csv("csv.csv",encoding='latin1')
            res["disease"] = res["disease"].str.lower().str.strip().str.replace(r'[^\w\s]+', '').str.replace(r'\s+', ' ')
            unique_diseases = res["disease"].unique()

            disease_precautions = res.set_index('disease')['Precautions'].to_dict()
            disease_tests = res.set_index('disease')['Medical Tests'].to_dict()

# Create selectbox for disease names
            selected_disease = st.selectbox('Select a Disease:',["None"] + [i for i in unique_diseases], index=0)
            if selected_disease != "None":
      
             st.write("You Selected:",selected_disease)
             selected_code = res.loc[res["disease"] == selected_disease, "code"].iloc[0]
          
            option2 = st.radio("Select Gender",('Male', 'Female'))
            if option2 == 'Male':
              option2 = 0
            else:
              option2 = 1 

            data2 = ('0-17 years', '18-29 years', '30-49 years','50-69 years','70 and above years')
            option3 = st.selectbox('Select Age Group',["None"] + [j for j in data2])
            for j in range(0,5):
                  if(option3 == data2[j]):
                        option3 = data2[j]
                        st.write("You Selected:",option3)
                        break
        
            if option3 == '0-17 years':
              option3 = 0
            elif option3 == '18-29 years':
              option3 = 1 
            elif option3 == '30-49 years':
              option3 = 2
            elif option3 == '50-69 years':
              option3 = 3
            else:
              option3 = 4
        
            result =''
            m = st.markdown("""
<style>
div.stButton >button:first-child {
  background-color: rgb(220,220,220);
}
</style>""",unsafe_allow_html=True)
    
            if st.button("PREDICT"):
              result = prediction([selected_code,option2,option3])
              st.write("Length of Stay: ",result,"days")
              
              if selected_disease in disease_tests:
               med = disease_tests[selected_disease]
               st.write(f"Recommended Medical Tests : {med}")
         
              if selected_disease in disease_precautions:
               precautions = disease_precautions[selected_disease]
               st.write(f"Precautions : {precautions}")
         else:
          st.warning("User not found. Please sign up.")

if st.sidebar.checkbox("Sign up", key="signup"):

      st.subheader("Create New Account")
      new_user = st.text_input("Username",key='1')
      new_password = st.text_input("Password",type='password',key='2')

      if st.button("Submit"):
            if username_exists(new_user):
                st.error("Username already exists. Please choose a different one.")
            elif not validate_password(new_password):
                st.error("Password must be at least 8 characters long and contain at least one digit and one uppercase letter.")
            else:
                add_user(new_user, new_password)
                st.success("You have successfully created an Account.Please Login !!")

if __name__ == '__main__':
   main()
import streamlit as st
import pandas as pd
import numpy as np
import pickle



import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def main():
  st.title(" ")

menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

pickle_in = open('rf.pkl', 'rb')
classifier = pickle.load(pickle_in)


def prediction(input_data):  
  input = np.asarray(input_data)
  sh = input.reshape(1,3)
  prediction = classifier.predict(sh)[0]
  print(prediction)
  return prediction

if choice == "Home":
    st.subheader("Home")

elif choice == "Login":
    st.subheader("Login Section")

username = st.sidebar.text_input("User Name")
password = st.sidebar.text_input("Password",type='password')

if st.sidebar.checkbox("Login"):
    # if password == '12345':
    create_usertable()
    hashed_pswd = make_hashes(password)

    result = login_user(username,check_hashes(password,hashed_pswd))
    if result:

        st.success("Logged In as {}".format(username))
        st.title("Predicting Length of Stay for Hospital Inpatients")

        res = pd.read_csv("csv.csv",sep=',', encoding='utf8')
       
        data = res.loc[:,'CCS Diagnosis Description']
        data1 = res.loc[:,'code']
        data2 = res.loc[:,'Precautions']
        option1 = st.selectbox("Select Disease",["None"] + [i for i in data])
        
        for i in range(0,1343):
          if(option1 == data[i]):
            res_code = data1[i]
            st.write("You Selected:",option1,"with disease code :",res_code)
            break
          
        op = st.text_input("Enter Disease Code")
        option2 = st.number_input("Enter Gender(Type 0 for male and 1 for female)",min_value=0, max_value=1)
        option3 = st.number_input("Enter Age Group(Type 0 for (0-17 years),1 for (18-29 years),2 for (30-49 years),3 for (50-69 years),4 for (70 and above years)",min_value=0, max_value=4)
        
        result =''
        if st.button("PREDICT"):
          result = prediction([op,option2,option3])
          st.write("Length of Stay: ",result)
          st.write("Precautions: ",data2[i])
 
    else:
        st.warning("Incorrect Username/Password")

elif choice == "SignUp":
    st.subheader("Create New Account")
    new_user = st.text_input("Username",key='1')
    new_password = st.text_input("Password",type='password',key='2')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

if __name__ == '__main__':
	main()
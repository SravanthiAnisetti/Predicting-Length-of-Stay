## Title : Predicting Length of Stay of Patients in Hospital using Machine Learning

## Objectives 
This project focuses more on the logistical metric of healthcare,hospital length-of-stay (LOS). 

A web page is designed in such a way that it is easy to use and predicts the length of stay information, along with some precautions, for the selected disease.

Prolonged LOS may result in high use of hospital resources. As a result, accurate prediction of patient LOS may aid healthcare professionals in making medical decisions and allocating medical teams and resources.


## Dataset 
https://health.data.ny.gov/Health/Hospital-Inpatient-Discharges-SPARCS-De-Identified/82xm-y6g8

“NewYork Hospital Inpatient Discharges in 2015” is the dataset used, which can be downloaded from the Kaggle. 
 
This dataset contains 1+ million rows of patient data, including information such as patient general details, diagnoses, treatments,costs, and charges.

### Tool 
Visual Studio Code
### Programming Language
Python
### Framework
Streamlit
## Steps to execute the project
1. Install the latest version of Visual Studio Code and Python interpreter.

2. Create a folder in your system with above mentioned files and open that folder in visual studio code.

(Folder must contain : kaggle dataset(rename it as Health Care),ipynb notebook,ap.py(python file),csv.csv(intermediate csv file),rf.pkl)

3. Click the ap.py file.

4. In the terminal of VS Code, install the necessary python libraries and required modules through pip command.

(For example: pip install streamlit,
              pip install -U jupyter etc)
              
    5.Then run ap.py through the command : streamlit run ap.py
 
   6. Hence the page will be redirected to a browser and you can be able to view the output page.
                   

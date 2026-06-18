import streamlit as st
from PIL import Image
import pandas as pd
import time
import requests
import json


# defining the function which will get the prediction 
# using the data with the user inputs 
def get_prediction(chemicals):
    
    # define the url of the API exposing the trained model
    url = 'http://kevinwineapi.azurewebsites.net/predict'

    # List containing the features
    X_columns = ['volatile_acidity', 'alcohol']
    
    # zip the two lists together to create a list of key-value pairs
    key_value_pairs = zip(X_columns, chemicals)
    data = dict(key_value_pairs)

    headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
    }

    resp = requests.post(url, headers=headers, json=data)
    
    return json.loads(resp.json())


# when 'Predict' is clicked, make the prediction and store it 
def predict(chemicals):
    
    st.markdown("***")
    if st.button("Predict"): 
        result = get_prediction(chemicals)

        #st.text(result)
        
        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)
        time.sleep(1)
        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'Iteration {i+1}')
            bar.progress(i + 1)
            time.sleep(0.01)
        
        time.sleep(0.5)
        if result.get('prediction') == 1:
            #st.text(result.get('prediction'))
            st.success(f'This is a Good wine, probability: {result.get("probability")[1]:.2f}')
        else:
            #st.text(result.get('prediction'))
            st.error(f'This is a Bad wine, probability: {result.get("probability")[0]:.2f}')

# Get features using input widgets
def inputversion():
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # fixed_acidity = st.number_input("Fixed Acidity", min_value=0.0, max_value=15.0, value=7.4)
        volatile_acidity = st.number_input("Volatile Acidity", min_value=0.0, max_value=2.0, value=0.7)
        # citric_acid = st.number_input("Citric Acid", min_value=0.0, max_value=1.0, value=0.0)
        # residual_sugar = st.number_input("Residual Sugar", min_value=0.0, max_value=15.0, value=1.9)
        # free_sulfur_dioxide = st.number_input("Free Sulfur Dioxide", min_value=0, max_value=100, value=11)
        # total_sulfur_dioxide = st.number_input("Total Sulfur Dioxide", min_value=0, max_value=300, value=34)
    
    with col2:
        st.write('')

    with col3:
        # chlorides = st.number_input("Chlorides", min_value=0.0, max_value=0.2, value=0.076)
        # density = st.number_input("Density", min_value=0.0, max_value=2.0, value=0.9978)
        # sulphates = st.number_input("Sulphates", min_value=0.0, max_value=2.0, value=0.56)
        # pH = st.number_input("pH", min_value=0.0, max_value=14.0, value=3.51)
        alcohol = st.number_input("Alcohol", min_value=0.0, max_value=20.0, value=9.4)
    
    # chemicals = [[fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
    #               chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density,
    #               pH, sulphates, alcohol]]

    chemicals = [volatile_acidity, alcohol]
    
    predict(chemicals)

# Get features using slider widgets
def sliderversion():
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # fixed_acidity = st.slider('Fixed Acidity', 4.0, 16.0, 6.695, 0.01) 
        volatile_acidity = st.slider('Volatile Acidity', 0.0, 2.0, 0.319, 0.001) 
        # citric_acid = st.slider('Citric Acidity', 0.0, 1.0, 0.442, 0.01)
        # residual_sugar = st.slider('Residual Sugar', 0.0, 16.0, 2.391, 0.01) 
        # free_sulfur_dioxide = st.slider('free sulfur dioxide', 1.0, 80.0, 23.68, 0.1) 
        # total_sulfur_dioxide = st.slider('total sulfur dioxide', 1.0, 300.0, 33.77, 0.1) 

    with col2:
        st.write('')

    with col3:
        # chlorides = st.slider('chlorides', 0.0, 1.0, 0.061, 0.001) 
        # density = st.slider('density', 0.9, 1.1, 0.9948, 0.001) 
        # sulphates = st.slider('sulphates', 0.1, 2.0, 0.802, 0.001) 
        # pH = st.slider('pH', 2.0, 5.0, 3.29, 0.01) 
        alcohol = st.slider('Alcohol', 0.0, 16.0, 11.634, 0.01) 
        
    
    # chemicals = [[fixed_acidity, volatile_acidity, citric_acid, residual_sugar,
    #               chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density,
    #               pH, sulphates, alcohol]]
    
    chemicals = [volatile_acidity, alcohol]

    predict(chemicals)


# this is the main function in which we define our webpage  
def main():
    st.markdown("# Wine Quality Prediction App 🍷🍇")
    st.markdown("### This app is meant to predict red wine quality " +
            "according to different chemical")

    # display the image of the app
    col1, col2 = st.columns(2)
    with col1:
        init_image = Image.open("../img/wine6.jpeg")
        st.image(init_image, width=250)

    with col2:
        st.text("")
        st.markdown("### **Select Mode:**")
        select_mode = []

        modes_df = pd.DataFrame(['Choose', 'Input version', 'Slider version'])
        select_mode.append(st.selectbox('Mode selection', modes_df, label_visibility='collapsed'))
    
    if select_mode[0] == 'Input version':
        inputversion()
    elif select_mode[0] == 'Slider version':
        sliderversion()
    else:
        st.text("")

# Init code
if __name__=='__main__': 
    main()
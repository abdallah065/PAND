#create a streamlit app to display the results of plant disease detection
import streamlit as st
import time
import numpy as np
from PIL import Image           # for checking images
import modelClass as mc
import json
import requests


def predict(image):
    #show the progress bar
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.003)
        my_bar.progress(percent_complete + 1)
        
    st.write("")
    data = mc.predict_image(image, model)

    #display the top 3 predictions beside each other if confidance 1 is less than 0.98
    if data[0]['confidance'] < 99:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Plant: ", data[0]['plant'])
            if data[0]['status'] == "healthy":
                st.write("Status: ", data[0]['status'], ":smile:")
            else:
                st.write("Status: ", data[0]['status'], ":broken_heart:")
                st.write("Disease: ", data[0]['disease'])
            st.write("Confidance: ", data[0]['confidance'])
        with col2:
            st.write("Plant: ", data[1]['plant'])
            if data[1]['status'] == "healthy":
                st.write("Status: ", data[1]['status'], ":smile:")
            else:
                st.write("Status: ", data[1]['status'], ":broken_heart:")
                st.write("Disease: ", data[1]['disease'])
            st.write("Confidance: ", data[1]['confidance'])
        with col3:
            st.write("Plant: ", data[2]['plant'])
            if data[2]['status'] == "healthy":
                st.write("Status: ", data[2]['status'], ":smile:")
            else:
                st.write("Status: ", data[2]['status'], ":broken_heart:")
                st.write("Disease: ", data[2]['disease'])
            st.write("Confidance: ", data[2]['confidance'])
    else:
        #display the first prediction in center
        st.write("Plant: ", data[0]['plant'])
        if data[0]['status'] == "healthy":
            st.write("Status: ", data[0]['status'], ":smile:")
        else:
            st.write("Status: ", data[0]['status'], ":broken_heart:")
            st.write("Disease: ", data[0]['disease'])
        st.write("Confidance: ", data[0]['confidance'])
    #set the footer of the app

    #cuase and treatment of the disease html 
    with open("result_html.json", 'r') as f:
        result_html = json.load(f)

    #show a horizontal line in center
    st.write("--------------Cause and Treatment of the Disease--------------  (" + data[0]['disease'] + ")")
    
    #display the cuase and treatment of the disease html
    st.markdown(result_html[data[0]['class_name']], unsafe_allow_html=True)


#load the model
model = mc.get_model()

st.set_page_config(page_title="P.A.N.D System", page_icon=":seedling:", layout="wide", initial_sidebar_state="auto")

#set the title of the app
st.title("P.A.N.D System")

#supported plants
with open("classes_out.json", "r") as f:
    classes = json.load(f)


#set the sidebar of the app
st.sidebar.title("Supported Plants")
st.sidebar.write("This app can detect the following plants:")
for i in range(len(classes)):
    st.sidebar.write(classes[str(i)]["plant"]+": "+classes[str(i)]["disease"],":seedling:")

#set the subtitle of the app
st.subheader("Plant Analysis and Disease Detection System")

#set the description of the app
st.write("This is a web app that can detect plant diseases and give you the best treatment for the disease. It can also detect the status of the plant (healthy, unhealthy, or dead).")

uploaded = False

#switch botton to choose between automatic detection and manual detection
option = st.selectbox("Choose the detection method", ["Automatic Detection", "Manual Detection"])

def php_request():
    #make a request to the php server to get the image link
    try:
        url = "https://anubis4bug.000webhostapp.com/img_upload/get_file_name.php"
        response = requests.get(url)
        #response is json
        response = response.json()
        #get the image link
        if len(response["link"]) == 0:
            image = Exception("No image found in database")
        else:
            image = "https://anubis4bug.000webhostapp.com/uploads/" + response["link"]
        
    except Exception as e:
        image = e
    return image

#choose the detection method **************************************
#automatic detection
if option == "Automatic Detection":
    image = php_request()
    image_url = php_request()
    if isinstance(image, Exception):
        st.write(Exception("Error loading image from database"))
        st.write(image)
        #set the option to manual detection
        uploaded = False
    else:
        image = mc.get_image(url=image,local=False)
        uploaded = True
    
    if uploaded:
        #show the small image
        st.image(str(image_url), caption="Uploaded Image.", width=300)
        predict(image)
        
    else:
        option = "Manual Detection"
    #wait 20 seconds
    time.sleep(60)
    #reload the page
    st.experimental_rerun()
    
#manual detection
else:
    #load the image by upload or url
    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg","JPJ", "PNG", "JPEG"])
    if image is None:
        image_url = st.text_input("Enter an image URL")
        if image_url != "":
            image = mc.get_image(url=image_url,local=False)
            #if image belongs to Exiption, then it is not a valid url
            if isinstance(image, Exception):
                st.write(image)
            else:
                uploaded = True
        else:
            st.write(Exception("Please enter an image URL or upload an image"))
    else:
        uploaded = True 
        #transform the image to numpy array
        image = np.array(Image.open(image))
        
        image = mc.prepare_image(image)
        

if uploaded:
    predict(image)
    st.markdown("Developed with :heart: by [Abdallah Saber](https://www.linkedin.com/in/abdallah-saber-530a5b213/)", unsafe_allow_html=True)
#create a streamlit app to display the results of plant disease detection
import streamlit as st
import time
import numpy as np
from PIL import Image           # for checking images
import modelClass as mc

#load the model
model = mc.get_model()

st.set_page_config(page_title="P.A.N.D System", page_icon=":seedling:", layout="wide", initial_sidebar_state="expanded")

#set the title of the app
st.title("P.A.N.D System")

#set the subtitle of the app
st.subheader("Plant Analysis and Disease Detection System")

#set the description of the app
st.write("This is a web app that can detect plant diseases and give you the best treatment for the disease. It can also detect the status of the plant (healthy, unhealthy, or dead).")

#load the image by upload or url
image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg","JPJ", "PNG", "JPEG"])
if image is None:
    image = st.text_input("Enter an image URL")
    if image is not None:
        try:
            image = mc.get_image(url=image,local=False)
        except Exception as e:
            st.write("Invalid URL")
            image = None
else: 
    #transform the image to numpy array
    image = np.array(Image.open(image))
    
    image = mc.prepare_image(image)
#show the progress bar
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.005)
    my_bar.progress(percent_complete + 1)
    
st.write("")
data = mc.predict_image(image, model)

#display the top 3 predictions beside each other if confidance 1 is less than 0.98
if data[0]['confidance'] < 99:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Plant: ", data[0]['plant'])
        st.write("Status: ", data[0]['status'])
        st.write("Disease: ", data[0]['disease'])
        st.write("Confidance: ", data[0]['confidance'])
    with col2:
        st.write("Plant: ", data[1]['plant'])
        st.write("Status: ", data[1]['status'])
        st.write("Disease: ", data[1]['disease'])
        st.write("Confidance: ", data[1]['confidance'])
    with col3:
        st.write("Plant: ", data[2]['plant'])
        st.write("Status: ", data[2]['status'])
        st.write("Disease: ", data[2]['disease'])
        st.write("Confidance: ", data[2]['confidance'])
else:
    #display the first prediction in center
    st.write("Plant: ", data[0]['plant'])
    st.write("Status: ", data[0]['status'])
    st.write("Disease: ", data[0]['disease'])
    st.write("Confidance: ", data[0]['confidance'])
#set the footer of the app



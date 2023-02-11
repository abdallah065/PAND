#create a streamlit app to display the results of plant disease detection
import streamlit as st
import time
import numpy as np
from PIL import Image           # for checking images
import modelClass as mc
import json
import requests


#load the model
model = mc.get_model()

st.set_page_config(page_title="P.A.N.D System", page_icon=":seedling:", layout="wide", initial_sidebar_state="auto")

#set the title of the app
st.title("P.A.N.D System")


#option to choose between english and arabic
lang = st.selectbox("Choose the language", ["English", "عربي"])

#note: if detection method choosed as "Automatic Detection" any changes in the language will take effect after the next image is uploaded
if lang == "English":
    #write this 'note: if detection method choosed as "Automatic Detection" any changes in the language will take effect after the next image is uploaded'
    st.write("Note: if detection method choosed as \"Automatic Detection\" any changes in the language will take effect after the next image is uploaded")
else:
    #write this 'ملاحظة: إذا تم اختيار طريقة الكشف عن "الكشف التلقائي" فإن أي تغييرات في اللغة ستؤثر بعد تحميل الصورة التالية'
    st.write("ملاحظة: إذا تم اختيار طريقة الكشف عن \"الكشف التلقائي\" فإن أي تغييرات في اللغة ستؤثر بعد تحميل الصورة التالية")
#set the app text direction rtl for arabic and ltr for english
if lang == "English":
    st.markdown("<style>body{direction: ltr;}</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>body{direction: rtl;}</style>", unsafe_allow_html=True)

#predct function
def predict(image):
    #show the progress bar
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.003)
        my_bar.progress(percent_complete + 1)
        
    st.write("")
    if lang == "English":
        data = mc.predict_image(image, model, lang="en")
    else:
        data = mc.predict_image(image, model, lang="ar")

    #display the top 3 predictions beside each other if confidance 1 is less than 0.98
    if lang == "English":
        confidance_str="Confidance: "
        plant_str="Plant: "
        status_str="Status: "
        disease_str="Disease: "
    else:
        confidance_str="الثقة: "
        plant_str="النبات: "
        status_str="الحالة: "
        disease_str="المرض: "
    if data[0]['confidance'] < 99:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(plant_str, data[0]['plant'])
            if data[0]['status'] == "healthy":
                st.write(status_str, data[0]['status'], ":smile:")
            else:
                st.write(status_str, data[0]['status'], ":broken_heart:")
                st.write(disease_str, data[0]['disease'])
            st.write(confidance_str, data[0]['confidance'])
        with col2:
            st.write(plant_str, data[1]['plant'])
            if data[1]['status'] == "healthy":
                st.write(status_str, data[1]['status'], ":smile:")
            else:
                st.write(status_str, data[1]['status'], ":broken_heart:")
                st.write(disease_str, data[1]['disease'])
            st.write(confidance_str, data[1]['confidance'])
        with col3:
            st.write(plant_str, data[2]['plant'])
            if data[2]['status'] == "healthy":
                st.write(status_str, data[2]['status'], ":smile:")
            else:
                st.write(status_str, data[2]['status'], ":broken_heart:")
                st.write(disease_str, data[2]['disease'])
            st.write(confidance_str, data[2]['confidance'])
    else:
        #display the first prediction in center
        st.write(plant_str, data[0]['plant'])
        if data[0]['status'] == "healthy":
            st.write(status_str, data[0]['status'], ":smile:")
        else:
            st.write(status_str, data[0]['status'], ":broken_heart:")
            st.write(disease_str, data[0]['disease'])
        st.write(confidance_str, data[0]['confidance'])

    #cuase and treatment of the disease html 
    if lang == "English":
        with open("result_html.json", 'r') as f:
            result_html = json.load(f)
    else:
        with open("result_html_ar.json", 'r') as f:
            result_html = json.load(f)

    #show a horizontal line in center
    st.write("--------------Cause and Treatment of the Disease--------------  (" + data[0]['disease'] + ")")
    
    #display the cuase and treatment of the disease html
    st.markdown(result_html[data[0]['class_name']], unsafe_allow_html=True)



#supported plants
if lang == "English":
    with open("classes_out.json", "r") as f:
        classes = json.load(f)
else:
    with open("classes_out_ar.json", "r") as f:
        classes = json.load(f)

#set the sidebar of the app
if lang == "English":
    st.sidebar.title("Supported Plants")
    st.sidebar.write("This app can detect the following plants:")
else:
    st.sidebar.title("النباتات المدعومة")
    st.sidebar.write("يمكن لهذا التطبيق اكتشاف النباتات التالية:")
    
for i in range(len(classes)):
    st.sidebar.write(classes[str(i)]["plant"]+": "+classes[str(i)]["disease"],":seedling:")

#set the subtitle of the app
if lang == "English":
    st.subheader("Plant Disease Detection")
else:
    st.subheader("تشخيص أمراض النباتات")

#set the description of the app
if lang == "English":
    st.write("This is a web app that can detect plant diseases and give you the best treatment for the disease. It can also detect the status of the plant (healthy, unhealthy, or dead).")
else:
    st.write("هذا تطبيق ويب يمكنه اكتشاف أمراض النباتات وإعطائك أفضل علاج للمرض. يمكنه أيضًا اكتشاف حالة النبات (صحي، غير صحي أو ميت).")
    
uploaded = False

#switch botton to choose between automatic detection and manual detection
if lang == "English":
    option = st.selectbox("Choose the detection method", ["Automatic Detection", "Manual Detection"])
else:
    option = st.selectbox("اختر طريقة الكشف", ["كشف تلقائي", "كشف يدوي"])
    

def php_request():
    #make a request to the php server to get the image link
    try:
        url = "https://anubis4bug.000webhostapp.com/img_upload/get_file_name.php"
        response = requests.get(url)
        #response is json
        response = response.json()
        #get the image link
        if len(response["link"]) == 0:
            if lang == "English":
                image = Exception("No image found in database")
                date = None
            else:
                image = Exception("لم يتم العثور على صورة في قاعدة البيانات")
                date = None
        else:
            image = "https://anubis4bug.000webhostapp.com/uploads/" + response["link"]
            date = response["date"]
        
    except Exception as e:
        image = e
        date = None
    return [image, date]

#choose the detection method **************************************
#automatic detection
if option == "Automatic Detection" or option == "كشف تلقائي":
    php = php_request()
    image = php[0]
    date = php[1]
    image_url = image
    if isinstance(image, Exception):
        if lang == "English":
            st.write(Exception("Error loading image from database"))
        else:
            st.write(Exception("خطأ في تحميل الصورة من قاعدة البيانات"))
        st.write(image)
        #set the option to manual detection
        uploaded = False
    else:
        image = mc.get_image(url=image,local=False)
        uploaded = True
    
    if uploaded:
        #show the small image
        if lang == "English":
            caption = "Uploaded Image."
        else:
            caption = "الصورة المحملة."
        st.image(str(image_url), caption=caption, width=300)
        #show the date of the image
        if lang == "English":
            st.write("Date: ", date)
        else:
            st.write("التاريخ: ", date)
        predict(image)
        
    else:
        if lang == "English":
            option = "Manual Detection"
        else:
            option = "كشف يدوي"
    #wait 60 seconds
    time.sleep(60)
    #reload the page
    st.experimental_rerun()
    
#manual detection
else:
    #load the image by upload or url
    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg","JPJ", "PNG", "JPEG"])
    if image is None:
        if lang == "English":
            image_url = st.text_input("Enter an image URL")
        else:
            image_url = st.text_input("أدخل عنوان URL للصورة")
        if image_url != "":
            image = mc.get_image(url=image_url,local=False)
            #if image belongs to Exiption, then it is not a valid url
            if isinstance(image, Exception):
                st.write(image)
            else:
                uploaded = True
        else:
            if lang == "English":
                st.write(Exception("Please enter an image URL or upload an image"))
            else:
                st.write(Exception("يرجى إدخال عنوان URL للصورة أو تحميل صورة"))
    else:
        uploaded = True 
        #transform the image to numpy array
        image = np.array(Image.open(image))
        
        image = mc.prepare_image(image)
        

if uploaded:
    predict(image)
    if lang == "English":
        caption = "Uploaded Image."
    else:
        caption = "الصورة المحملة."
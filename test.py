import modelClass

model = modelClass.get_model()

url = "D:\\Abdallah\\Pictures\\444.jpg"
 
 
data = modelClass.predict_image(url, model)

for i in range(len(data)):
    print(data[i])

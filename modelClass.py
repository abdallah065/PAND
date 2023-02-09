import torch                    # Pytorch module 
import torch.nn as nn           # for creating  neural networks
import torch.nn.functional as F # for functions for calculating loss
# import numpy as np              # for numerical computationss
import torch                    # Pytorch module 
import torch.nn as nn           # for creating  neural networks
from PIL import Image           # for checking images
import torch.nn.functional as F # for functions for calculating loss
import torchvision.transforms as transforms   # for transforming images into tensors 
# import seaborn as sns                         # for plotting confusion matrix
import json 
# import matplotlib.pyplot as plt # for plotting informations on graph and images using tensors
import io                      # for reading and writing bytes
import requests               # for making HTTP requests
import time                   # for time operations
import os                       # for working with files
import pandas as pd             # for working with dataframes
# from torch.utils.data import DataLoader # for dataloaders 
# from torchvision.utils import make_grid       # for data checking
# from torchvision.datasets import ImageFolder  # for working with classes and images
# from torchsummary import summary              # for getting the summary of our model
# from sklearn.metrics import confusion_matrix  # for confusion matrix
#extracting the rar file



class __SimpleResidualBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=1)
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=1)
        self.relu2 = nn.ReLU()
        
    def forward(self, x):
        out = self.conv1(x)
        out = self.relu1(out)
        out = self.conv2(out)
        return self.relu2(out) + x # ReLU can be applied before or after adding the input

# for calculating the __accuracy
def __accuracy(outputs, labels):
    _, preds = torch.max(outputs, dim=1)
    return torch.tensor(torch.sum(preds == labels).item() / len(preds))


# base class for the model
class __ImageClassificationBase(nn.Module):
    
    def training_step(self, batch):
        images, labels = batch
        out = self(images)                  # Generate predictions
        loss = F.cross_entropy(out, labels) # Calculate loss
        return loss
    
    def validation_step(self, batch):
        images, labels = batch
        out = self(images)                   # Generate prediction
        loss = F.cross_entropy(out, labels)  # Calculate loss
        acc = __accuracy(out, labels)          # Calculate __accuracy
        return {"val_loss": loss.detach(), "val___accuracy": acc}
    
    def validation_epoch_end(self, outputs):
        batch_losses = [x["val_loss"] for x in outputs]
        batch___accuracy = [x["val___accuracy"] for x in outputs]
        epoch_loss = torch.stack(batch_losses).mean()       # Combine loss  
        epoch___accuracy = torch.stack(batch___accuracy).mean()
        return {"val_loss": epoch_loss, "val___accuracy": epoch___accuracy} # Combine accuracies
    
    def epoch_end(self, epoch, result):
        print("Epoch [{}], last_lr: {:.5f}, train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
            epoch, result['lrs'][-1], result['train_loss'], result['val_loss'], result['val___accuracy']))
        

## 👷 Defining the final architecture of our model 👷

# Architecture for training

# convolution block with BatchNormalization
def _ConvBlock(in_channels, out_channels, pool=False):
    layers = [nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
             nn.BatchNorm2d(out_channels),
             nn.ReLU(inplace=True)]
    if pool:
        layers.append(nn.MaxPool2d(4))
    return nn.Sequential(*layers)

# resnet architecture 
class __ResNet9(__ImageClassificationBase):
    def __init__(self, in_channels, num_diseases):
        super().__init__()
        
        self.conv1 = _ConvBlock(in_channels, 64)
        self.conv2 = _ConvBlock(64, 128, pool=True) # out_dim : 128 x 64 x 64 
        self.res1 = nn.Sequential(_ConvBlock(128, 128), _ConvBlock(128, 128))
        
        self.conv3 = _ConvBlock(128, 256, pool=True) # out_dim : 256 x 16 x 16
        self.conv4 = _ConvBlock(256, 512, pool=True) # out_dim : 512 x 4 x 44
        self.res2 = nn.Sequential(_ConvBlock(512, 512), _ConvBlock(512, 512))
        
        self.classifier = nn.Sequential(nn.MaxPool2d(4),
                                       nn.Flatten(),
                                       nn.Linear(512, num_diseases))
        
    def forward(self, xb): # xb is the loaded batch
        out = self.conv1(xb)
        out = self.conv2(out)
        out = self.res1(out) + out
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.res2(out) + out
        out = self.classifier(out)
        return out    

#transformer
transform = transforms.Compose([
    transforms.ToTensor()
]) 


classes = []
class_path = os.path.join(os.path.dirname(__file__),'classes.json')
with open(class_path, 'r') as f:
    classes = json.load(f)


#load the model
def get_model():   
    #load the __ResNet9 model from plant-disease-model-complete.pth
    device = torch.device('cpu')
    model = __ResNet9(3,38)
    #get the relative path of the model
    model_path = os.path.join(os.path.dirname(__file__),'plant-disease-model1.pth')
    #check if the model is exist
    model.load_state_dict(torch.load(model_path, map_location=device))
    return model

def prepare_image(image):
    #transform numpy array to PIL image
    image = Image.fromarray(image)
    #reshape image to (256, 256, 3)
    if image.size != (256, 256):
        image = image.resize((256, 256))
    image = image.convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)
    return image

#load the image from the url
def get_image(url,darw=False,local=True,time_out=20):
    if local:
        image = Image.open(url)
    else:
        try:
            start = time.time()
            response = requests.get(url,timeout=time_out)
            image = Image.open(io.BytesIO(response.content))
        except Exception as e:
            raise Exception("Error loading image from server: {}".format(e.__cause__))
    #reshape image to (256, 256, 3)
    if image.size != (256, 256):
        image = image.resize((256, 256))
    image = image.convert('RGB')
    if darw:
        image.show(title=url)
    image = transform(image)
    image = image.unsqueeze(0)
    return image
    
#convert the index to the disease name
def get_label(index):
     if index != None:
         return classes[index]
     else:
        raise Exception("Index is None")

#convert the classes_out.json to int
def __keystoint(x):
    new = {}
    for k,v in x:
        try:
            new[int(k)] = v
        except ValueError:
            new[k] = v
    return new

#load the classes_out.json
def get_classes_out():
    classes_out_path = os.path.join(os.path.dirname(__file__),'classes_out.json')
    with open(classes_out_path, 'r') as f:
        jsontxt = json.load(f)
    r = json.dumps(jsontxt)
    classes_out = json.loads(r,object_pairs_hook=__keystoint)
    return classes_out
classes_out = get_classes_out()

#predict the test data
def predict_image(image ,model , darw=False, local=True):
    #check if the image is url or image
    if type(image) == str:
        img = get_image(url=image ,darw=darw,local=local)
    else:
        img = image
    yb = model(img)
    #the confidance of all classes
    confidance = torch.nn.functional.softmax(yb, dim=1)
    #return the max 3 confidances and the labeles
    confidance , preds = torch.topk(confidance,3)
    confidance = confidance[0].tolist()
    preds = preds[0].tolist()
    data = [] 
    for i in range(len(preds)):
        data.append(classes_out[preds[i]])
        data[i]["confidance"] = round(confidance[i]*100,2)
        data[i]["class_name"] = get_label(preds[i])
    return data
    
#make image folder for the test data from the url
def make_image_folder(url,local=True):
    #write function docstring for parameters and return values
    """the function return the image folder and the image folder names
        parameters:
            url: the url of the folder
            local: if the folder is local or not
        return:
            Images_folder: the image folder
            pathes_folder: the image folder names
    """
    try:
        Image_pathes = os.listdir(url)
        
        #check if the folder is empty
        if len(Image_pathes) == 0:
            raise Exception("Folder is empty")
        else:
            #check if the folder contains images and make the image folder
            pathes_folder=[]
            Images_folder = []
            for i in range(len(Image_pathes)):
                if Image_pathes[i].split(".")[1] in ["jpg","png","jpeg","JPG","PNG","JPEG"]:
                    pathes_folder.append(Image_pathes[i])
            if len(pathes_folder) == 0:
                raise Exception("Folder does not contain images")
            else:
                #make the image folder
                for i in range(len(pathes_folder)):
                    Images_folder.append(get_image(url+pathes_folder[i],local=local))
                return Images_folder , pathes_folder
    except Exception as e:
        raise Exception("Error loading image from server: {}".format(e.__cause__))
                    
                
        
#         data_names = os.listdir(url)
#         return data , data_names
#     except Exception as e:
#         raise Exception("Error loading image from server: {}".format(e.__cause__))
# make_image_folder("test/")

#predict the images from the folder
def predict_image_folder(url, model, darw=False, local=True):
    data , data_names = make_image_folder(url)
    for i in range(len(data)):
        img = data[i][0].unsqueeze(0)
        yb = model(img)
        _, preds = torch.max(yb, dim=1)
        print(data_names[i] + " : " + get_label(preds[0].item()))
from django.shortcuts import render,redirect
from .forms import ImageUploadForm
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from PIL import Image
import dlib
import cv2
import numpy as np
import os
image_path = open(os.path.join(settings.MEDIA_ROOT,"uploads/1.jpg"),"rb")
im= Image.open(image_path)
image_array= np.asarray(im)
array2=image_array.copy()

face_detector= dlib.get_frontal_face_detector()
face_recognition_model=dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1 (1).dat")
predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
def extract_face_features(image):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=face_detector(gray)
    features=[]
    for face in faces:
        cv2.rectangle(image,(face.left(),face.top()),(face.right(),face.bottom()),(0,255,0),3)
        landmarks= predictor(gray,face)
        face_descriptor=face_recognition_model.compute_face_descriptor(image,landmarks)
        for n in range(0,68):
            x=landmarks.part(n).x
            y=landmarks.part(n).y
            cv2.circle(image,(x,y),4,(0,0,255),-1)
        features.append(face_descriptor)
    cv2.imshow('image',image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return features

def compare(f1,f2):
    descriptor1=np.array(f1[0])
    descriptor2=np.array(f2[0])
    distance=np.linalg.norm(descriptor1-descriptor2)
    if distance<=0.6:
        s1="Same face"
        return s1
    else :
        s2="Different faces"
        return s2 

    
def auth(request):
    template=loader.get_template("detect/auth.html")
    return HttpResponse(template.render({},request))
 
def recognise(request):
    load_features=extract_face_features(array2)
    vid =cv2.VideoCapture(0)
    while(True):
        ret,frame=vid.read()
    #cv2.imshow('frame',frame)
        features=extract_face_features(frame)
        if cv2.waitKey(1)==ord('q'):
            break
#cv2.imshow('frame',frame)
#cv2.waitKey(0)
    
    vid.release()
    cv2.destroyAllWindows()
    rv=compare(features,load_features)
    template=loader.get_template("detect/result.html")
    return HttpResponse(template.render({"rv":rv},request))

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('auth.html')
    else:
        form = ImageUploadForm()
    return render(request,'detect/upload_image.html',{'form': form})


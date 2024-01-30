from django.urls import path
from .views import upload_image,auth,recognise
urlpatterns=[path("",upload_image,name='upload_image'),path("run_model",recognise,name="run_model"),
path("auth.html",auth,name="auth.html"),path("upload/",upload_image,name='upload_image'),
]

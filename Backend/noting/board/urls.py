from django.urls import path, include  
from .views import *

urlpatterns = [
    path('' , index, name='index'),
    path('allMemo/' , allMemo, name='allMemo'),
    path('uploadPost/' , uploadPost, name='allMemo'),
    path('lunch/', donong_lunch, name='lunch'),
    path('comments/<int:post_id>/', getComments, name='getComments'),
    path('uploadComment/', uploadComment, name='uploadComment'),
    path('log_in/', log_in, name='login'),
    path('sign_up/', sign_up, name='signup'),
]
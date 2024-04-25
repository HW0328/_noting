from django.urls import path, include  
from .views import *

urlpatterns = [
    path('' , index, name='index'),
    path('allMemo/' , allMemo, name='allMemo'),
    path('uploadPost/' , uploadPost, name='allMemo'),
    path('logggin/' , Login, name='login'),
    path('pro/' , pf, name='pro'),

]
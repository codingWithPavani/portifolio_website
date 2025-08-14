from django.contrib import admin
from django.urls import path
from message import views  # replace myapp with your app name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', views.contact_view, name='contact'),
    path('', views.index, name='index'),
]

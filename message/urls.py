from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_view, name='contact'),
    path('', views.index, name='index'),
    path('test-email/', views.test_email, name='test_email'),
    

]

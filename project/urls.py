
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello_to_my_project, name='Say Hello'),
    path('goodbye/', views.say_goodbye_to_my_project, name='Say Goodbye'),
    path('aggregate/', views.aggregate_example, name='Aggregate Example'),
]
from django.shortcuts import render, HttpResponse   

# Create your views here.


def say_hello_to_my_project(request):
    return HttpResponse("Hola from Project app!")

def say_goodbye_to_my_project(request):
    goodbye_message = "Goodbye from Project app! See you again!"
    return render(request, 'bye.html', {'goodbye_message': goodbye_message})
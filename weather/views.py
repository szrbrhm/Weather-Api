from django.shortcuts import render,redirect,get_object_or_404
import requests
from decouple import config
from pprint import pprint
from .models import City
from django.contrib import messages

# Create your views here.

def index(request):
    cities = City.objects.all()
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    # city = "istanbul"
    # response = requests.get(url.format(city, config('API_KEY')))
    # content = response.json()
    # print(content)
    # print(type(content))
    
    g_city = request.GET.get('name')
    print("g_city:", g_city)
    if g_city:
        
        response = requests.get(url.format(g_city, config('API_KEY')))
        print(response.status_code)
        if response.status_code == 200:
            content = response.json()
            a_city = content['name']
            print(a_city)
            if City.objects.filter(name=a_city):
                messages.warning(request, 'City already exists')
            else:
                City.objects.create(name=a_city)
                messages.success(request, 'City successfully added')
        else:
            messages.warning(request, 'City does not exist')
        return redirect('index')
           
        
        
        
    city_data = []
    for city in cities:
        print(city)
        response = requests.get(url.format(city, config('API_KEY')))
        content = response.json()
        pprint(content)
        data = {
            "city" : city,
            "temp" : content['main']["temp"],
            "desc" : content['weather'][0]["description"],
            "icon" : content['weather'][0]["icon"],
        }
        
        city_data.append(data)
    pprint(city_data)
    context = {
        "city_data" : city_data,
    }

    return render(request, "weather/index.html",context)

def delete_city(request,id):
    city = get_object_or_404(City, id=id)
    city.delete()
    return redirect('index')


    


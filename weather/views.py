import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=a8e40e23f81508dac1055201e717b938'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)
        # prevent duplicates
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                #print(r)
                if r['cod'] == 200:    
                    form.save()
                else:
                    err_msg = 'City does not exist!'
            else:
                err_msg = 'City is already added in the List!'
    #print(err_msg)
    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        #print(r.text)
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    #print(weather_data)
    #print(city_weather)
    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)

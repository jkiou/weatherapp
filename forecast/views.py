from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime
import pytz

API_KEY = '8a98d140172d0d3c5d9e7d50a36d3863'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('weather')
    else:
        form = UserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('weather')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('weather')

def about_view(request):
    return render(request, 'about.html')

def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    print("API Response:", data)
    
    # Clean up the description by removing spaces
    description = data['weather'][0]['description'].replace(' ', '')
    
    weather_data = {
        'city': data['name'],
        'current_temperature': round(data['main']['temp']),
        'feels_like_temperature': round(data['main']['feels_like']),
        'temp_min': round(data['main']['temp_min']),
        'temp_max': round(data['main']['temp_max']),
        'humidity': data['main']['humidity'],
        'wind_speed': round(data['wind']['speed']),
        'description': description,
        'country': data['sys']['country'],
        'clouds': data['clouds']['all'],
        'pressure': data['main']['pressure'],
        'visibility': data.get('visibility', 'N/A'),
    }
    return weather_data

def get_forecast(city):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric&cnt=5"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    
    forecasts = []
    for item in data['list']:
        time = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
        temp = round(item['main']['temp'])
        humidity = item['main']['humidity']
        clouds = item['clouds']['all']
        forecasts.append({
            'time': time,
            'temp': temp,
            'humidity': humidity,
            'clouds': clouds
        })
    return forecasts

@login_required(login_url='login')
def weather_view(request):
    context = {}
    
    if request.method == 'POST':
        city = request.POST.get('city')
        if not city:
            messages.error(request, 'Please enter a city name')
            return render(request, 'forecast/weather.html', context)
        
        current_weather = get_current_weather(city)
        if not current_weather:
            messages.error(request, 'City not found')
            return render(request, 'forecast/weather.html', context)
        
        forecasts = get_forecast(city)
        if not forecasts:
            messages.error(request, 'Unable to get forecast data')
            return render(request, 'forecast/weather.html', context)

        timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(timezone)
        
        context = {
            'city': current_weather['city'],
            'country': current_weather['country'],
            'current_temperature': current_weather['current_temperature'],
            'feels_like_temperature': current_weather['feels_like_temperature'],
            'temp_min': current_weather['temp_min'],
            'temp_max': current_weather['temp_max'],
            'humidity': current_weather['humidity'],
            'clouds': current_weather.get('clouds', '--'),
            'description': current_weather['description'],
            'wind_speed': current_weather['wind_speed'],
            'pressure': current_weather['pressure'],
            'visibility': current_weather['visibility'],
            'date': current_time.strftime('%b %d, %Y'),
            'time': current_time.strftime('%I:%M %p'),
            'forecasts': forecasts
        }
        
    return render(request, 'forecast/weather.html', context)
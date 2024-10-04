from django.shortcuts import render
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Thiruvananthapuram'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=5f15092a1e89d6be467da698a046c12f'
    PARAMS = {'units': 'metric'}
    error_message = None  # Variable to store error message if any

    try:
        response = requests.get(url, params=PARAMS)
        response.raise_for_status()  # Raise HTTPError if the response status is 4xx or 5xx
        data = response.json()

        # Extract required information
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapps/index.html', {
            'description': description,
            'icon': icon,
            'day': day,
            'temp': temp,
            'city': city,
            'error_message': error_message
        })

    except requests.exceptions.HTTPError:
        # If the API response indicates an error, set an error message
        error_message = f"Weather data for '{city}' is not available. Please try a different city."
    
    except requests.exceptions.RequestException:
        # Handle other network-related errors
        error_message = "There was a problem retrieving the data. Please try again later."
    
    # Render the template with default data and error message
    return render(request, 'weatherapps/index.html', {
        'description': 'N/A',
        'icon': '01d',  # Default icon
        'day': datetime.date.today(),
        'temp': 'N/A',
        'city': city,
        'error_message': error_message
    })

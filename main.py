from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import redis
# weather
from geopy import geocoders
import requests

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
except:
    print("Redis isn't started on your local machine.")


async def get_weather_forecast(city: str):
    gn = geocoders.GeoNames(username="markdevel0per")  # free feature
    key = "fa43a522e02a4aab983115541242007"  # free key
    try:
        latitude, longitude = gn.geocode(city)[1]
    except TypeError:
        return {}
    try:
        weather_url = f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={latitude},{longitude}&days=4"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
    except:
        print("Api key is invalid.")
        return {}

    current_weather = weather_data['current']
    forecast_days = weather_data['forecast']['forecastday']

    response = {
        "current": {
            "temp": current_weather['temp_c'],
            "wind": current_weather['wind_kph'],
            "condition": current_weather['condition']['text'],
            "icon": current_weather['condition']['icon']
        },
        "forecast": [
            {
                "date": forecast_days[i]['date'],
                "temp_avg": forecast_days[i]['day']['avgtemp_c'],
                "wind": forecast_days[i]['day']['maxwind_kph'],
                "condition": forecast_days[i]['day']['condition']['text'],
                "icon": forecast_days[i]['day']['condition']['icon']
            }
            for i in range(1, 4)
        ]
    }

    return response


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    index_page = 1
    cached_cities = r.lrange("searched_cities", 0, 8)
    return templates.TemplateResponse("home.html", request=request,
                                      context={"request": request, "index_page": index_page,
                                               "cached_cities": cached_cities})


@app.post('/submit', response_class=HTMLResponse)
async def submit_city(user_input: Annotated[str, Form()], request: Request):
    return RedirectResponse(url=f"/weather/{user_input}", status_code=303)


@app.get('/weather/{city}', response_class=HTMLResponse)
async def weather(city: str, request: Request):
    weather = await get_weather_forecast(city=city)
    r.lpush("searched_cities", city)
    r.ltrim("searched_cities", 0, 8)
    cached_cities = r.lrange("searched_cities", 0, -1)
    return templates.TemplateResponse("home.html", request=request,
                                      context={"request": request, "weather": weather, "city": city,
                                               "cached_cities": cached_cities})


@app.get('/history', response_class=HTMLResponse)
async def get_my_history(request: Request):
    user_ip = request.client.host
    cached_cities = r.lrange("searched_cities", 0, -1)
    return templates.TemplateResponse("history.html", {"request": request, "cached_cities": cached_cities})

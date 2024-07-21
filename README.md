# fastapi-project

This is a website that gives a weather forecast for your city 
Few words about the project: It is written on the clean fast api. Cache is stored by Redis. Tests are written on Pytest and Unittest. API by weatherapi.com. Added autocomplete for the most popular cities in the world and CIS. When the user searches for another city, he can see his history of 10 last visited cities. Forecast is 4 day. 

Done all except the API.



How to run it:
1. Clone the repository or just download it
2. Make sure you installed python3.12
3. type: docker build -t asd .
4. type: docker run -d --name fastapi-docker-container -p 80:80 fastapi-docker
5. go to localhost on your browser and that's all


Thanks for reading

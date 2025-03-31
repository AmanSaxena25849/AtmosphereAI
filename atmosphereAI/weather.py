import requests
from datetime import datetime
from django.core.cache import cache

# wather code refrence dictionary.......
WEATHER_CODE_REF = {
    "0": {
        "day": {
            "description": "Sunny",
            "image": "http://openweathermap.org/img/wn/01d@2x.png"
        },
        "night": {
            "description": "Clear",
            "image": "http://openweathermap.org/img/wn/01n@2x.png"
        }
    },
    "1": {
        "day": {
            "description": "Mainly Sunny",
            "image": "http://openweathermap.org/img/wn/01d@2x.png"
        },
        "night": {
            "description": "Mainly Clear",
            "image": "http://openweathermap.org/img/wn/01n@2x.png"
        }
    },
    "2": {
        "day": {
            "description": "Partly Cloudy",
            "image": "http://openweathermap.org/img/wn/02d@2x.png"
        },
        "night": {
            "description": "Partly Cloudy",
            "image": "http://openweathermap.org/img/wn/02n@2x.png"
        }
    },
    "3": {
        "day": {
            "description": "Cloudy",
            "image": "http://openweathermap.org/img/wn/03d@2x.png"
        },
        "night": {
            "description": "Cloudy",
            "image": "http://openweathermap.org/img/wn/03n@2x.png"
        }
    },
    "45": {
        "day": {
            "description": "Foggy",
            "image": "http://openweathermap.org/img/wn/50d@2x.png"
        },
        "night": {
            "description": "Foggy",
            "image": "http://openweathermap.org/img/wn/50n@2x.png"
        }
    },
    "48": {
        "day": {
            "description": "Rime Fog",
            "image": "http://openweathermap.org/img/wn/50d@2x.png"
        },
        "night": {
            "description": "Rime Fog",
            "image": "http://openweathermap.org/img/wn/50n@2x.png"
        }
    },
    "51": {
        "day": {
            "description": "Light Drizzle",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Light Drizzle",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "53": {
        "day": {
            "description": "Drizzle",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Drizzle",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "55": {
        "day": {
            "description": "Heavy Drizzle",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Heavy Drizzle",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "56": {
        "day": {
            "description": "Light Freezing Drizzle",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Light Freezing Drizzle",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "57": {
        "day": {
            "description": "Freezing Drizzle",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Freezing Drizzle",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "61": {
        "day": {
            "description": "Light Rain",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night": {
            "description": "Light Rain",
            "image": "http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "63": {
        "day": {
            "description": "Rain",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night": {
            "description": "Rain",
            "image": "http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "65": {
        "day": {
            "description": "Heavy Rain",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night": {
            "description": "Heavy Rain",
            "image": "http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "66": {
        "day": {
            "description": "Light Freezing Rain",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night": {
            "description": "Light Freezing Rain",
            "image": "http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "67": {
        "day": {
            "description": "Freezing Rain",
            "image": "http://openweathermap.org/img/wn/10d@2x.png"
        },
        "night": {
            "description": "Freezing Rain",
            "image": "http://openweathermap.org/img/wn/10n@2x.png"
        }
    },
    "71": {
        "day": {
            "description": "Light Snow",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night": {
            "description": "Light Snow",
            "image": "http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "73": {
        "day": {
            "description": "Snow",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night": {
            "description": "Snow",
            "image": "http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "75": {
        "day": {
            "description": "Heavy Snow",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night": {
            "description": "Heavy Snow",
            "image": "http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "77": {
        "day": {
            "description": "Snow Grains",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night": {
            "description": "Snow Grains",
            "image": "http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "80": {
        "day": {
            "description": "Light Showers",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Light Showers",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "81": {
        "day": {
            "description": "Showers",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Showers",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "82": {
        "day": {
            "description": "Heavy Showers",
            "image": "http://openweathermap.org/img/wn/09d@2x.png"
        },
        "night": {
            "description": "Heavy Showers",
            "image": "http://openweathermap.org/img/wn/09n@2x.png"
        }
    },
    "85": {
        "day": {
            "description": "Light Snow Showers",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night": {
            "description": "Light Snow Showers",
            "image": "http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "86": {
        "day": {
            "description": "Snow Showers",
            "image": "http://openweathermap.org/img/wn/13d@2x.png"
        },
        "night": {
            "description": "Snow Showers",
            "image": "http://openweathermap.org/img/wn/13n@2x.png"
        }
    },
    "95": {
        "day": {
            "description": "Thunderstorm",
            "image": "http://openweathermap.org/img/wn/11d@2x.png"
        },
        "night": {
            "description": "Thunderstorm",
            "image": "http://openweathermap.org/img/wn/11n@2x.png"
        }
    },
    "96": {
        "day": {
            "description": "Light Thunderstorms With Hail",
            "image": "http://openweathermap.org/img/wn/11d@2x.png"
        },
        "night": {
            "description": "Light Thunderstorms With Hail",
            "image": "http://openweathermap.org/img/wn/11n@2x.png"
        }
    },
    "99": {
        "day": {
            "description": "Thunderstorm With Hail",
            "image": "http://openweathermap.org/img/wn/11d@2x.png"
        },
        "night": {
            "description": "Thunderstorm With Hail",
            "image": "http://openweathermap.org/img/wn/11n@2x.png"
        }
    }
}


def get_weather(latitude: float, longitude: float)->dict:
    """get weather data from Redis cache or OPEN METEO API using coordinates. separates and saves data into separate variables and returns it.  
       

    Args:
        latitude (float): latitude of the city
        longitude (float): longitude of the city

    Raises:
        RequestException: Raises if not data is found on both cache or API.

    Returns:
        Dictionary: dictionary of all the currunt data and zipped hourly and daily data. 
    """
    
    
    cache_key = f"Weather_data_latitude:{latitude}_longitude:{longitude}"
    cache_data = cache.get(cache_key) #try to get cached data from redis server.
    
    
    if cache_data:
        print("Data fetched from redis cache")
        return cache_data # returns data if its in the Redis cache.
    else:
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "hourly": "temperature_2m,weather_code",
            "current": ["apparent_temperature", "is_day", "snowfall", "surface_pressure", "wind_gusts_10m",
                        "pressure_msl", "showers", "wind_direction_10m", "cloud_cover", "rain", "relative_humidity_2m",
                        "wind_speed_10m", "weather_code", "precipitation", "temperature_2m"],
            "timezone": "auto"
        }
        
    



        try:
            #making request to api.......
            pre_response = requests.get(base_url, params)
            
            if pre_response.status_code == 200:
                response = pre_response.json()

                # separating data into variables.
 
                # variables for currunt weather conditions.
                date_time = response["current"]["time"]
                date_part = date_time[:10]
                today_date =  datetime.strptime(date_part, "%Y-%m-%d").strftime("%B %d, %Y")
                current_time = datetime.strptime(date_time[11:], "%H:%M").strftime("%I:%M %p")
                current_temp = response["current"]["temperature_2m"]
                wind_speed = response["current"]["wind_speed_10m"]
                relative_humidity = response["current"]["relative_humidity_2m"]
                precipitation = response["current"]["precipitation"]
                surface_pressure = response["current"]["surface_pressure"]
                max_temp = response["daily"]["temperature_2m_max"][0]
                min_temp = response["daily"]["temperature_2m_min"][0]
                
                
                # variables for hourly weather conditions.
                hour = []
                hour_temp = []
                hour_weather = []
                hour_weather_icon = []
                
                for i in range(11):
                    hour.append(response["hourly"]["time"][i][11:])
                    hour_temp.append(response["hourly"]["temperature_2m"][i])
                    code = str(response["hourly"]["weather_code"][i])
                    hour_weather.append(WEATHER_CODE_REF[code]["day"]["description"])
                    hour_weather_icon.append(WEATHER_CODE_REF[code]["day"]["image"])
                
                
                
                 # variables for daily weather conditions.
                day_name = []
                day_temperature = []
                day_weather = []
                day_weather_icon = []

                for i in range(7):
                    day = response["daily"]["time"][i]
                    day_name.append( datetime.strptime(day, "%Y-%m-%d").strftime("%A"))
                    day_temperature.append(response["daily"]["temperature_2m_max"][i])
                    code = str(response["daily"]["weather_code"][i])
                    day_weather.append(WEATHER_CODE_REF[code]["day"]["description"])
                    day_weather_icon.append(WEATHER_CODE_REF[code]["day"]["image"])
                
                
               
                #zipping only hourly and daily data for easy accessibility in html file.   
                hour_data = zip(hour, hour_temp, hour_weather, hour_weather_icon)
                day_data = zip(day_name, day_temperature, day_weather,day_weather_icon)
                
                
                weather_data = {"today_date":today_date,
                                "current_time": current_time,
                                "current_temp": current_temp,
                                "wind_speed": wind_speed,
                                "relative_humidity": relative_humidity,
                                "precipitation": precipitation,
                                "surface_pressure": surface_pressure,
                                "max_temp": max_temp,
                                "min_temp": min_temp,
                                "hour": hour,
                                "hour_temp": hour_temp,
                                "hour_weather": hour_weather,
                                "hour_weather_icon": hour_weather_icon,
                                "hour_data":hour_data,
                                "day_name": day_name,
                                "day_temperature": day_temperature,
                                "day_weather": day_weather,
                                "day_weather_icon": day_weather_icon,
                                "day_data":day_data}
                
                #set cache in redis for 15min.....
                cache.set(cache_key, weather_data , timeout=300)
                print("Data set in redis cache")
                
                
                return weather_data


        except requests.RequestException as e:
            raise Exception(f"Failed to get weather data: {e}")
        





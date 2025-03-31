from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .weather import get_weather
from .geocoding import get_location,search_locations
from ipware import get_client_ip
from .chatbot import chat_reply
from django.core.cache import caches


# setting up cache for rate limmiting in all views
cache = caches['default']


def home(request):
    """View for home screen."""
    
    # default latitude and longitude of New Delhi 
    latitude = 28.7041
    longitude = 77.1025
    
    try:    
        weather_data = get_weather(latitude=latitude, longitude=longitude)  #gets weather data 
        address = get_location(latitude=latitude, longitude=longitude) #gets address of that coordinates

        return render(request, "atmoSphereAI.html", {**weather_data, "address": address, "latitude":latitude,  "longitude":longitude})
    except:
        return JsonResponse({'error': "failed to get weather data"}, status=400)
    

 
    
def city_weather(request):
    """View for city weather"""
    
    #takes users coordinate from frontend.
    latitude = request.GET.get("lat")
    longitude = request.GET.get("lon")
    
    
    if latitude and longitude:
        try:
            weather_data = get_weather(latitude=latitude, longitude=longitude)#gets weather data 
            address = get_location(latitude=latitude, longitude=longitude)#gets address of that coordinates
            return render(request, "atmoSphereAI.html", {**weather_data, "address": address, "weather_data":str(weather_data)})
        
        except:
            return JsonResponse({'error': "failed to get weather data"}, status=400)
    else:
        latitude = 28.7041
        longitude = 77.1025
        weather_data = get_weather(latitude=latitude, longitude=longitude)#gets weather data 
        address = get_location(latitude=latitude, longitude=longitude)#gets address of that coordinates
        return render(request, "atmoSphereAI.html", {**weather_data, "address": address, "weather_data":str(weather_data)})
    
       

def search_results(request):
    """view for quick search using HTMX."""    
    
    #takes the query and remove space and make it lower case.
    search_query = request.GET.get("search_query", "").strip().lower()
    
    if not search_query:
        #returns empty list so html logic can show no city found.
        return render(request, "search_list.html", {"city_data":[]}) 
    
    else:
        city_data = search_locations(query=search_query) #searches the city and returns list of cities
        return render(request, "partials/search_list.html", {"city_data":city_data})
    


def chatbot(request):
    """view for getting chat results from llama using HTMX"""
    
    if request.method == "POST":
        user_chat = request.POST.get("user_chat")
        weather_data = request.POST.get("weather_data")
        
        # useing ipware to get user IP
        ip, is_routable = get_client_ip(request) 
        
        #seting cache key, limit and time window in seconds.
        cache_key = f"rate_limit:{ip}"
        limit = 3  
        window = 60  
        
        #initializing the request counter.
        request_count = cache.get(cache_key, 0)

        if request_count == 0:
            cache.set(cache_key, 1, timeout=window) # seting the timout on first request.
            remaining_time = window # get remaining time to show in the html.
            
        else:
            request_count = cache.incr(cache_key) # incrementing the timeout with every request.
            remaining_time = cache.ttl(cache_key) # get live remaining time to show in the html.

        if request_count > limit:
            return render(request, "partials/chatbot.html", {"remaining_time":remaining_time, "limit":limit})

        elif user_chat and request_count <= limit:
            helping_data = f"You are a helpful weather AI assistant with this data: {weather_data}. Keep responses under 150 words, short and precise."
            reply = chat_reply(helping_data=helping_data, question=user_chat)
            return render(request, "partials/chatbot.html", {"user_chat": user_chat, "reply": reply})

        else:
            #if request was empty then an empty response to avoid errors.
            return HttpResponse() 
    
    else:
        #handaling other type of request and logging it. 
        print("Request was not a POST request.")
        return JsonResponse({"error":"Request was not a POST request."},status=400)
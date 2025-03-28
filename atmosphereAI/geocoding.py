from geopy.geocoders import Nominatim
from django.core.cache import cache


geolocator = Nominatim(user_agent="AtomsphereAI")


def get_location(latitude: float, longitude: float)->str:
    
    """Gets address using coordinates data using GEOpy.

     Args:
        latitude (float): latitude of the city
        longitude (float): longitude of the city
    
    Returns:
        String: string containing address.
    """
    
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}", language="en")
        address = location.raw['address']
        loc = str(location).split(", ")
        
    
        # Extract the city name and country
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        
        
        if city and country:
            city_country = f"{city}, {country}"
        elif state and country:
            city_country = f"{loc[0]}, {state}, {country}"
        else:
            city_country = "Unknown"

        return city_country
    
    except Exception as e:
        print(f"Unexpected error by geopy(get_location): {e}")





def search_locations(query:str)->list:
    
    """ Get city address and coordinates using name or pin-code from GEOpy or Redis cache.

    Args:
        query (string):Searched query(city name or pin-code)
        
    Raises:
        Exception: Raises exception and prints it if any error occours.
    
    Returns:
        List: Zipped list of city name, city full address, city latitude and city longitude.
    """
    
    cache_key = f"scity_search_{query}"   
    
    #trying to data form redis cache 
    cache_results = cache.get(cache_key)
    
    if cache_results:
        return cache_results 
    
    else:
        try:
            cities = geolocator.geocode(query=query, exactly_one=False, limit=4)
        
            city_list = []
            city_titles = []
            city_latitude = []
            city_longitude = []
            
            #saving data into seperate variables.
            for city in cities:
                p = city.address.split(', ')
                city_titles.append(p[0])
                city_list.append(city.address)
                city_latitude.append(city.latitude)
                city_longitude.append(city.longitude)
                
            
            city_data = list(zip(city_titles, city_list, city_latitude, city_longitude))
            
            cache.set(cache_key, city_data, timeout=60*60*2)  #saving data into redis cache.
            
            return  city_data
        
        except Exception as e:
            print(f"Unexpected error by geopy(search_loaction): {e}")
            return [] #returns emplty list so no city found can be showed by the logic in search_list html template.
     



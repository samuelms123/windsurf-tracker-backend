from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="windsurf_tracker")

async def get_location(latitude, longitude):
        
    geolocator = Nominatim(user_agent="windsurf_tracker")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    
    if not location:
        return None
    
    address = location.address
    address_list = [part.strip() for part in address.split(",")]
    

    return {
        "street": address_list[0],
        "neighborhood": address_list[1],
        "district": address_list[2],
        "subdistrict": address_list[3],
        "city": address_list[4],
        "metropolitan_area": address_list[5],
        "region": address_list[6],
        "mainland": address_list[7],
        "postal_code": address_list[8],
        "country": address_list[9], 
    }

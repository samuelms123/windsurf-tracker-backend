from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="windsurf_tracker")

def get_location(latitude: float, longitude: float) -> dict:
        
    geolocator = Nominatim(user_agent="windsurf_tracker")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)

    if not location:
        return None
    
    ad: dict = location.raw['address']

    return {
        "street": ad.get("road"),
        "neighborhood": ad.get("quarter"),
        "suburb": ad.get("suburb"),
        "city_district": ad.get("city_district"),
        "city": ad.get("city"),
        "municipality": ad.get("municipality"),
        "region": ad.get("state"),
        "area": ad.get("region"),
        "postal_code": ad.get("postcode"),
        "country": ad.get("country"),
    }

#            60.187712,
#            25.13872

if __name__ == "__main__":

    #print(get_location(61.211385, 25.716855))
    print(get_location(60.187712,25.13872))
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2

    return 2 * R * math.asin(math.sqrt(a))


def nearby_places(user_lat, user_lon, donations, max_km=5):
    result = []
    for item in donations:
        if item["latitude"] and item["longitude"]:
            dist = haversine(user_lat, user_lon, item["latitude"], item["longitude"])
            if dist <= max_km:
                result.append((item, dist))
    return result

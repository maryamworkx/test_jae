from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from geopy.distance import geodesic

app = FastAPI()

class Location(BaseModel):
    lat: float
    lng: float

station_data = {
    'admiralty':     {'code': 'NS10',      'coords': (1.4406, 103.8000)},
    'aljunied':      {'code': 'EW9',       'coords': (1.3167, 103.8820)},
    'ang mo kio':    {'code': 'NS16',      'coords': (1.3691, 103.8488)},
    'vation park':   {'code': 'CR2',       'coords': (1.3382, 103.7803)},
    'bahar junction':{'code': 'JS7',       'coords': (1.3398, 103.7056)},
    'bartley':       {'code': 'CC12',      'coords': (1.3424, 103.8803)},
    'bayfront':      {'code': 'DT16 CE1',  'coords': (1.2820, 103.8595)},
    'bayshore':      {'code': 'TE29',      'coords': (1.3019, 103.9214)}
}

def get_nearest_station(lat: float, lng: float) -> Dict:
    input_coords = (lat, lng)
    min_distance = float('inf')
    nearest_station = None

    for name, info in station_data.items():
        dist = geodesic(input_coords, info['coords']).kilometers
        if dist < min_distance:
            min_distance = dist
            nearest_station = {
                "station_name": name,
                "station_code": info['code'],
                "distance_km": round(dist, 3)
            }

    return nearest_station

@app.post("/nearest-station")
def nearest_station(location: Location):
    result = get_nearest_station(location.lat, location.lng)
    if not result:
        raise HTTPException(status_code=404, detail="No station found")

    return {
        "input_location": {"lat": location.lat, "lng": location.lng},
        **result
    }

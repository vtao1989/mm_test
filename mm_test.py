## Package
import pandas as pd
from valhalla import Actor, get_config

## map matching config
config = get_config(tile_extract='custom_files/valhalla_tiles.tar', verbose=False)
actor = Actor(config)

selected_points = pd.read_csv('trips.csv')

for trip_id in selected_points['trip_id'].unique():
    print(trip_id)
    trip_points = selected_points[selected_points['trip_id']==trip_id]
    ## create query
    coords = trip_points[['lat', 'lon', 'new_time']].to_json(orient='records')
    query_head = '{"shape":'
    query_tail = ""","search_radius": 50, "shape_match":"map_snap", "costing":"auto", "format":"osrm"}"""
    query_body = query_head + coords + query_tail
    try:
        response = actor.trace_attributes(query_body)
    except RuntimeError as e:
        print(e)
        continue
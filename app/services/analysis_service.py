import pandas as pd
import json
### Data analysis logic

def load_stream_data(filepath):
    with open(filepath, 'r') as f:
        stream = json.load(f)
    return stream

def analyze_data(data_stream):
    ## split into many steps
    # top speed during 5 sec intervals
    # top speed during 10 sec intervals
    # acceleration from small speed to 10 knots
    # acceleration from smaal speed to 20 knots
    # gybes amount
    pass 

def parse_stream(stream):
    data_dict = {}
    for stream in stream:
        stream_type = stream['type']
        stream_data = stream['data']
        if stream_type == 'latlng':
            lats, lngs = zip(*stream_data)
            data_dict['lat'] = lats
            data_dict['lng'] = lngs
        else:
            data_dict[stream_type] = stream_data
    return pd.DataFrame(data_dict)
    

def top_speed_rolling_avg(data):
    print(data)
    pass


if __name__ == "__main__":
    data = load_stream_data('C:\Projects\Windsurf-Tracker\windsurf-tracker-backend\stream_example_response.json')
    df = parse_stream(data)
    print(df.head(50))
    
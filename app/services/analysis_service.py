import pandas as pd
import numpy as np
import json

class DataAnalysis:
    
    
    def __init__(self):
        self.results = {}
        
        # Speed zones
        self.idle_max_speed = 1.5
        self.low_max_speed = 3.5
        self.planing_entry_max_speed = 4.5
        self.planing_max_speed = 8.0
        
    
    def save_to_results(self, result_name: str, value):
        self.results[result_name] = value
    
    # testing data
    def load_stream_data(self, filepath):
        with open(filepath, 'r') as f:
            stream = json.load(f)
        return stream

    def analyze_data(self, data_stream):
        print("Started to analyze data")
        # Convert to pandas DataFrame
        df = self.parse_stream(data_stream)
        
        # Calculate rolling top speed averages
        self.top_speed_rolling_avg(df)
        
        # Calculate time spend in each speed zone 
        self.time_spend_in_time_zones(df)
        
        # Calculate fastest x meters
        self.fastest_meters(df, 100)
        self.fastest_meters(df, 500)
        self.fastest_meters(df, 1000)
        self.fastest_meters(df, 1852)  # 1 nautical mile in meters
        
        return self.results

    def parse_stream(self, stream):
        print("Parse stream started")
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
    
    def time_spend_in_time_zones(self, df: pd.DataFrame):
        print("calculation: time_spend_in_time_zones")
        bins = [
            0,
            self.idle_max_speed,
            self.low_max_speed,
            self.planing_entry_max_speed,
            self.planing_max_speed,
            np.inf
        ]
        
        labels = ['idle', 'low', 'planing_entry', 'planing', 'blasting']
        zones = pd.cut(df['velocity_smooth'], bins=bins, labels=labels, include_lowest=True)
        self.results['speed_zones'] = zones.value_counts().to_dict()

        

    def top_speed_rolling_avg(self, df):
        print("Started to calculate top speed")
        df['rolling_avg_5rows'] = df['velocity_smooth'].rolling(window=5).mean()
        df['rolling_avg_10rows'] = df['velocity_smooth'].rolling(window=10).mean()

        max_5 = df['rolling_avg_5rows'].max()
        max_10 = df['rolling_avg_10rows'].max()
        
        avg_5_sec = float(round(max_5, 2)) if not pd.isna(max_5) else 0.0
        avg_10_sec = float(round(max_10, 2)) if not pd.isna(max_10) else 0.0
        
        self.save_to_results('max_speed_avg_5_s', avg_5_sec)
        self.save_to_results('max_speed_avg_10_s', avg_10_sec)
        
    
    def fastest_meters(self, df, target_distance):
        print("calculation: fastest meters")
        distances = df['distance'].values
        n = len(distances)
        start_index = 0
        best_time = None
        
        for end_index in range(n):
            while start_index < end_index and distances[end_index] - distances[start_index] >= target_distance:
                duration = end_index - start_index
                if best_time is None or duration < best_time:
                    best_time = duration
                
                start_index += 1
                
        self.results[f'fastest_{target_distance}'] = best_time

        
        
        
    # not used, atleast yet
    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        d_lon = np.radians(lon2 - lon1)
        lat1 = np.radians(lat1)
        lat2 = np.radians(lat2)

        x = np.sin(d_lon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(d_lon)

        bearing = np.degrees(np.arctan2(x, y))
        bearing = (bearing + 360) % 360  # Normalize to 0-360
        return bearing
 

            

if __name__ == "__main__":
    da = DataAnalysis()
    data = da.load_stream_data('/home/samuel/windsurf/windsurf-tracker-backend/stream_18997912984.json')
    result = da.analyze_data(data)
    print(result)
   # print(df.head(50))

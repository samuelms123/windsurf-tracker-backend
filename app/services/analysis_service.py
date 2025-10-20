import pandas as pd
import numpy as np
import json

class DataAnalysis:
    
    
    def __init__(self):
        self.results = {}
        
    
    def save_to_results(self, result_name: str, value):
        self.results[result_name] = value
    
    # testing data
    def load_stream_data(self, filepath):
        with open(filepath, 'r') as f:
            stream = json.load(f)
        return stream

    def analyze_data(self, data_stream):
        # Convert to pandas DataFrame
        df = self.parse_stream(data_stream)
        
        # Calculate rolling top speed averages
        self.top_speed_rolling_avg(df)
        
        # Acceleration
        self.top_acceleration(df, 1, 10) # from 1 m/s to 10 m/s
        self.top_acceleration(df, 1, 20)
        
        return self.results

    def parse_stream(self, stream):
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
    
    def top_acceleration(self, df: pd.DataFrame, start_speed, end_speed): # speed in m/s
        best_time = None
        i = 0
        velocities = df['velocity_smooth'].values
        times = df['time'].values
        
        while i < (len(df)):
            
            if velocities[i] >= start_speed:
                start_time = times[i]
                counter = 0
                
                for j in range(i + 1, len(df)):
                    velocity = velocities[j]
                    
                    # check if the velocity falls under starting speed for more than 5s
                    if velocity < start_speed:
                        counter += 1
                        if counter > 5:
                            i = j
                            break # return back to i loop to search for a starting point
                    else:
                        counter = 0
                        
                    if velocity >= end_speed:
                        end_time = times[j]
                        time = end_time - start_time
                        
                        if best_time is None or time < best_time:
                            best_time = time
                    
                        i = j
                        break
                while i < len(velocities) and velocities[i] > start_speed:
                    i += 1
                    
            else:
                i += 1
        
        self.results[f'acceleration_to_{end_speed}'] = float(round(best_time, 2)) if best_time is not None else None
        

    def top_speed_rolling_avg(self, df):
        df['rolling_avg_5rows'] = df['velocity_smooth'].rolling(window=5).mean()
        df['rolling_avg_10rows'] = df['velocity_smooth'].rolling(window=10).mean()
        
        avg_5_sec = float(round(df['rolling_avg_5rows'].max(), 2))
        avg_10_sec = float(round(df['rolling_avg_10rows'].max(), 2))
        
        self.save_to_results('avg_5_s', avg_5_sec)
        self.save_to_results('avg_10_s', avg_10_sec)
        
    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        """
        Calculate compass bearing between two GPS points.
        """
        d_lon = np.radians(lon2 - lon1)
        lat1 = np.radians(lat1)
        lat2 = np.radians(lat2)

        x = np.sin(d_lon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(d_lon)

        bearing = np.degrees(np.arctan2(x, y))
        bearing = (bearing + 360) % 360  # Normalize to 0-360
        return bearing
            

'''if __name__ == "__main__":
    da = DataAnalysis()
    data = da.load_stream_data('C:\Projects\Windsurf-Tracker\windsurf-tracker-backend\stream_example_response.json')
    print(da.analyze_data(data))
    df = da.parse_stream(data)
   # print(df.head(50))'''
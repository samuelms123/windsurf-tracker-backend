import pandas as pd
import json
### Data analysis logic

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
        self.top_acceleration(df, 1, 4)
        #self.top_acceleration_test(df, 1, 4)
        
        
        
        return self.results
        # top speed during 5 sec intervals
        # top speed during 10 sec intervals
        # acceleration from small speed to 5.14 m/s
        # acceleration from smaal speed to 10.3 m/s
        # gybes amount

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
        while i < (len(df)):
            start_row = df.iloc[i]

            if start_row['velocity_smooth'] >= start_speed:
                start_time = start_row['time']
                
                counter = 0
                for j in range(i + 1, len(df)):
                    end_row = df.iloc[j]
                    
                    # check if the velocity falls under starting speed for more than 5s
                    if end_row['velocity_smooth'] < start_speed:
                        counter += 1
                        if counter > 5:
                            break # return back to i loop to search for a starting point
                    else:
                        counter = 0
                        
                    if end_row['velocity_smooth'] >= end_speed:
                        end_time = end_row['time']
                        time = end_time - start_time
                        
                        if best_time is None or time < best_time:
                            best_time = time
                    
                        i = j
                        while i < len(df) and df.iloc[i]['velocity_smooth'] > start_speed:
                            i += 1
                            
                        break
                i += 1
            else:
                i += 1
        
        self.results[f'acceleration_to_{end_speed}'] = float(round(best_time, 2)) if best_time is not None else None
        
        
    def top_acceleration_test(self, df: pd.DataFrame, start_speed, end_speed):
        best_time = None
        i = 0
        while i < len(df):
            start_row = df.iloc[i]
            v_start = start_row['velocity_smooth']

            # We need to start BELOW end_speed, otherwise it's not a real acceleration segment
            if start_speed <= v_start < end_speed:
                start_time = start_row['time']
                counter = 0

                for j in range(i + 1, len(df)):
                    end_row = df.iloc[j]
                    v = end_row['velocity_smooth']

                    # If speed drops below start_speed, reset
                    if v < start_speed:
                        counter += 1
                        if counter > 5:
                            break
                    else:
                        counter = 0

                    if v >= end_speed:
                        end_time = end_row['time']
                        time_diff = end_time - start_time
                        if best_time is None or time_diff < best_time:
                            best_time = time_diff
                        break

                # Move i forward beyond this acceleration window
                while i < len(df) and df.iloc[i]['velocity_smooth'] >= start_speed:
                    i += 1
            else:
                i += 1

        self.results[f'acceleration_to_{end_speed}'] = (
            float(round(best_time, 2)) if best_time is not None else None
        )
                    
            

    def top_speed_rolling_avg(self, df):
        df['rolling_avg_5rows'] = df['velocity_smooth'].rolling(window=5).mean()
        df['rolling_avg_10rows'] = df['velocity_smooth'].rolling(window=10).mean()
        
        avg_5_sec = float(round(df['rolling_avg_5rows'].max(), 2))
        avg_10_sec = float(round(df['rolling_avg_10rows'].max(), 2))
        
        self.save_to_results('avg_5_s', avg_5_sec)
        self.save_to_results('avg_10_s', avg_10_sec)


if __name__ == "__main__":
    da = DataAnalysis()
    data = da.load_stream_data('C:\Projects\Windsurf-Tracker\windsurf-tracker-backend\stream_example_response.json')
    print(da.analyze_data(data))
    
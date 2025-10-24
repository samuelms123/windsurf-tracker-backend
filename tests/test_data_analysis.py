import pytest
import pandas as pd
from app.services.analysis_service import DataAnalysis

@pytest.fixture
def mock_data_stream(): # 20 rows
    return [
        {
            "type": "velocity_smooth",
            "data": [
                0.5, 1.2, 2.8, 3.6, 4.2, 5.5, 6.8, 7.9, 8.2, 7.8,
                7.0, 6.2, 5.8, 4.0, 3.2, 2.5, 1.8, 1.0, 0.6, 0.3
            ],
        },
        {
            "type": "distance",
            "data": [
                0, 10, 25, 40, 55, 70, 90, 115, 140, 165,
                190, 215, 240, 260, 280, 300, 315, 330, 345, 360
            ],
        },
        {
            "type": "time",
            "data": [
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                10, 11, 12, 13, 14, 15, 16, 17, 18, 19
            ],
        },
        {
            "type": "latlng",
            "data": [
                (60.0, 24.0), (60.0, 24.001), (60.0, 24.002), (60.0, 24.003),
                (60.0, 24.004), (60.0, 24.005), (60.0, 24.006), (60.0, 24.007),
                (60.0, 24.008), (60.0, 24.009), (60.0, 24.010), (60.0, 24.011),
                (60.0, 24.012), (60.0, 24.013), (60.0, 24.014), (60.0, 24.015),
                (60.0, 24.016), (60.0, 24.017), (60.0, 24.018), (60.0, 24.019)
            ],
        },
    ]
    
def test_parse_stream(mock_data_stream):
    da = DataAnalysis()
    df = da.parse_stream(mock_data_stream)
    
    # Check columns
    assert all(col in df.columns for col in ['velocity_smooth', 'distance', 'time', 'lat', 'lng'])
    
    # Check values
    assert df['velocity_smooth'].iloc[0] == 0.5
    assert df['distance'].iloc[1] == 10
    assert df['time'].iloc[1] == 1
    assert df['time'].iloc[5] == 5
    assert df['lat'].iloc[1] == 60.0
    assert df['lng'].iloc[1] == 24.001
    
    

def test_time_spend_in_time_zones(mock_data_stream):
    da = DataAnalysis()
    df = da.parse_stream(mock_data_stream)
    da.time_spend_in_time_zones(df)
    
    results = da.results['speed_zones']
    assert 'idle' in results
    assert 'low' in results
    assert 'planing_entry' in results
    assert 'planing' in results
    assert 'blasting' in results
    
    assert sum(results.values()) == len(df)
    

def test_top_speed_rolling_avg(mock_data_stream):
    da = DataAnalysis()
    df = da.parse_stream(mock_data_stream)
    da.top_speed_rolling_avg(df)
    
    assert 'max_speed_avg_5_s' in da.results
    assert 'max_speed_avg_10_s' in da.results
    assert da.results['max_speed_avg_5_s'] >= 0
    assert da.results['max_speed_avg_10_s'] >= 0
    
    

def test_fastest_meters(mock_data_stream):
    da = DataAnalysis()
    df = da.parse_stream(mock_data_stream)
    da.fastest_meters(df, 50)
    da.fastest_meters(df, 500)
    
    assert 'fastest_50' in da.results
    assert 'fastest_500' in da.results
    assert da.results['fastest_50'] >= 0
    assert da.results['fastest_500'] == None
    
    
def test_analyze_data(mock_data_stream):
    da = DataAnalysis()
    results = da.analyze_data(mock_data_stream)
    
    keys = ['speed_zones', 'max_speed_avg_5_s', 'max_speed_avg_10_s', 'fastest_100', 'fastest_500', 'fastest_1000']
    for key in keys:
        assert key in results
    
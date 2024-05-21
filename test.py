import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://air-quality-api.open-meteo.com/v1/air-quality"
params = {
	"latitude": 50.0461,
	"longitude": 1.4208,
	"current": ["european_aqi", "pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "dust", "uv_index", "uv_index_clear_sky", "ammonia"],
	"hourly": ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone", "dust", "uv_index", "uv_index_clear_sky", "ammonia"],
	"timezone": "Europe/Berlin",
	"start_date": "2024-01-01",
	"end_date": "2024-05-15"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_european_aqi = current.Variables(0).Value()
current_pm10 = current.Variables(1).Value()
current_pm2_5 = current.Variables(2).Value()
current_carbon_monoxide = current.Variables(3).Value()
current_nitrogen_dioxide = current.Variables(4).Value()
current_sulphur_dioxide = current.Variables(5).Value()
current_ozone = current.Variables(6).Value()
current_dust = current.Variables(7).Value()
current_uv_index = current.Variables(8).Value()
current_uv_index_clear_sky = current.Variables(9).Value()
current_ammonia = current.Variables(10).Value()

print(f"Current time {current.Time()}")
print(f"Current european_aqi {current_european_aqi}")
print(f"Current pm10 {current_pm10}")
print(f"Current pm2_5 {current_pm2_5}")
print(f"Current carbon_monoxide {current_carbon_monoxide}")
print(f"Current nitrogen_dioxide {current_nitrogen_dioxide}")
print(f"Current sulphur_dioxide {current_sulphur_dioxide}")
print(f"Current ozone {current_ozone}")
print(f"Current dust {current_dust}")
print(f"Current uv_index {current_uv_index}")
print(f"Current uv_index_clear_sky {current_uv_index_clear_sky}")
print(f"Current ammonia {current_ammonia}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
hourly_carbon_monoxide = hourly.Variables(2).ValuesAsNumpy()
hourly_nitrogen_dioxide = hourly.Variables(3).ValuesAsNumpy()
hourly_sulphur_dioxide = hourly.Variables(4).ValuesAsNumpy()
hourly_ozone = hourly.Variables(5).ValuesAsNumpy()
hourly_dust = hourly.Variables(6).ValuesAsNumpy()
hourly_uv_index = hourly.Variables(7).ValuesAsNumpy()
hourly_uv_index_clear_sky = hourly.Variables(8).ValuesAsNumpy()
hourly_ammonia = hourly.Variables(9).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["pm10"] = hourly_pm10
hourly_data["pm2_5"] = hourly_pm2_5
hourly_data["carbon_monoxide"] = hourly_carbon_monoxide
hourly_data["nitrogen_dioxide"] = hourly_nitrogen_dioxide
hourly_data["sulphur_dioxide"] = hourly_sulphur_dioxide
hourly_data["ozone"] = hourly_ozone
hourly_data["dust"] = hourly_dust
hourly_data["uv_index"] = hourly_uv_index
hourly_data["uv_index_clear_sky"] = hourly_uv_index_clear_sky
hourly_data["ammonia"] = hourly_ammonia

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)
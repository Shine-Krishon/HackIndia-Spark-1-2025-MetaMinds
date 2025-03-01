import pandas as pd
from flask import Flask, request, render_template
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime
from geopy.distance import geodesic

app = Flask(__name__)

# Load dataset
df = pd.read_csv('crop_data.csv')

# Data Cleaning
df = df.dropna()
df['Price Date'] = pd.to_datetime(df['Price Date'], format='%b-%y')

# Feature Engineering
df['Month'] = df['Price Date'].dt.month
df['Year'] = df['Price Date'].dt.year

# Average price per month
avg_price = df.groupby(['District', 'Crop', 'Year', 'Month'])['Crop Price (Rs per quintal)'].mean().reset_index()

# Get unique district and crop names for dropdown
districts = avg_price['District'].unique()
crops = avg_price['Crop'].unique()

# Function to forecast prices using SARIMA
def forecast_prices(district, crop):
    subset = avg_price[(avg_price['District'] == district) & (avg_price['Crop'] == crop)]
    
    if len(subset) >= 12:
        subset['Date'] = pd.to_datetime(subset[['Year', 'Month']].assign(day=1))
        subset.set_index('Date', inplace=True)
        
        model = SARIMAX(subset['Crop Price (Rs per quintal)'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        results = model.fit()
        
        forecast_values = results.get_forecast(steps=3).predicted_mean
        
        return [round(price, 2) for price in forecast_values]
    else:
        return None

# Function to recommend crops based on highest prices in the current month
def recommend_crops(district):
    current_month = datetime.now().month
    top_crops = avg_price[(avg_price['District'] == district) & (avg_price['Month'] == current_month)]
    top_crops = top_crops.groupby('Crop')['Crop Price (Rs per quintal)'].mean().nlargest(3).reset_index()
    
    return [(row["Crop"], round(row["Crop Price (Rs per quintal)"], 2)) for _, row in top_crops.iterrows()]

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', districts=districts, crops=crops)

@app.route('/forecast', methods=['POST'])
@app.route('/forecast', methods=['GET'])
def get_forecast():
    district = request.args.get('district')
    crop = request.args.get('crop')

    if not district or not crop:
        return "<p>Error: Missing district or crop parameter</p>", 400
    
    forecasted_prices = forecast_prices(district, crop)
    recommended_crops = recommend_crops(district)

    if forecasted_prices:
        return render_template('forecast.html', forecasted_prices=forecasted_prices, recommended_crops=recommended_crops, district=district, crop=crop)
    else:
        return render_template('error.html', message="Not enough data to forecast prices.")

df = pd.read_csv('crop_data.csv')
market_df = pd.read_csv("tamilnadu_markets_full_167_final.csv")  # Load market data

# Data Cleaning
df = df.dropna()
df['Price Date'] = pd.to_datetime(df['Price Date'], format='%b-%y')
df['Month'] = df['Price Date'].dt.month
df['Year'] = df['Price Date'].dt.year
avg_price = df.groupby(['District', 'Crop', 'Year', 'Month'])['Crop Price (Rs per quintal)'].mean().reset_index()

# Function to find nearby markets
# def find_nearby_markets(lat, lon, radius=50):
#     """Finds markets within the given radius (in km) of the given location."""
#     nearby_markets = []
    
#     for _, row in market_df.iterrows():
#         market_location = (row['Latitude'], row['Longitude'])
#         distance = geodesic((lat, lon), market_location).km

#         if distance <= radius:
#             nearby_markets.append((row['Market Name'], distance))

#     return sorted(nearby_markets, key=lambda x: x[1])

# @app.route('/nearby-markets', methods=['GET'])
# def get_nearby_markets():
#     lat = request.args.get('lat', type=float)
#     lon = request.args.get('lon', type=float)
#     radius = request.args.get('radius', default=50, type=float)

#     if lat is None or lon is None:
#         return "<p>Error: Missing latitude or longitude parameter</p>", 400

#     markets = find_nearby_markets(lat, lon, radius)
#     return render_template('markets.html', markets=markets)

if __name__ == '__main__':
    app.run(debug=True)

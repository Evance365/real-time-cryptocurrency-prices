import requests
import json
import time
from datetime import datetime

def fetch_crypto_prices(crypto_ids):
    """
    Fetch real-time cryptocurrency prices from CoinGecko API
    
    Args:
        crypto_ids (list): List of cryptocurrency IDs to fetch
        
    Returns:
        dict: Dictionary containing price data for requested cryptocurrencies
    """
    # CoinGecko API endpoint for price data
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    # Parameters for the API request
    params = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': 'usd,eur',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true',
        'include_last_updated_at': 'true'
    }
    
    try:
        # Make the API request
        response = requests.get(url, params=params)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def display_prices(price_data):
    """
    Display formatted cryptocurrency price data
    
    Args:
        price_data (dict): Dictionary containing price data
    """
    if not price_data:
        print("No data to display")
        return
    
    print("\n" + "="*60)
    print(f"CRYPTOCURRENCY PRICES - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    for crypto, data in price_data.items():
        # Convert Unix timestamp to readable format
        last_updated = datetime.fromtimestamp(data.get('last_updated_at', 0))
        last_updated_str = last_updated.strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n{crypto.upper()}:")
        print(f"  USD: ${data.get('usd', 'N/A'):,.2f}")
        print(f"  EUR: €{data.get('eur', 'N/A'):,.2f}")
        print(f"  24h Change (USD): {data.get('usd_24h_change', 'N/A'):+.2f}%")
        print(f"  Market Cap (USD): ${data.get('usd_market_cap', 'N/A'):,.2f}")
        print(f"  24h Volume (USD): ${data.get('usd_24h_vol', 'N/A'):,.2f}")
        print(f"  Last Updated: {last_updated_str}")
    
    print("\n" + "="*60)

def main():
    # List of cryptocurrencies to track (by CoinGecko ID)
    crypto_ids = ['bitcoin', 'ethereum', 'solana', 'cardano', 'ripple']
    
    print("Cryptocurrency Price Tracker")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            print("\nFetching latest prices...")
            price_data = fetch_crypto_prices(crypto_ids)
            display_prices(price_data)
            
            # Wait for 60 seconds before the next update
            print("\nRefreshing in 60 seconds...")
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nExiting program...")

if __name__ == "__main__":
    main()
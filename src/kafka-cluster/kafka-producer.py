import requests
import time
import signal

#Get bitcoin price from coindesk API
def get_bitcoin_price(api_url="https://api.coindesk.com/v1/bpi/currentprice.json"):
  try:
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an exception for bad status codes

    data = response.json()
    current_price = data['bpi']['USD']['rate'] 
    return {'price_usd': current_price}

  except requests.exceptions.RequestException as e:
    print(f"Error fetching Bitcoin price: {e}")
    return {'error': str(e)}

def signal_handler(sig, frame):
  print("\nStopping Bitcoin price updates...")
  exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)  # Register signal handler for Ctrl+C

  while True:
    bitcoin_price = get_bitcoin_price()
    if 'price_usd' in bitcoin_price:
      print(f"Current Bitcoin price (USD): ${bitcoin_price['price_usd']}")
    else:
      print(f"Error: {bitcoin_price['error']}") 

    time.sleep(0.01)  # Update every 60 seconds
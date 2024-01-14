import time
import requests
import json
from selenium import webdriver


def capture_screenshot_and_notify(url, file_path, discord_webhook_url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (without opening a visible browser window)
        driver = webdriver.Chrome(options=options)

        # Load the webpage
        driver.get(url)
        time.sleep(15)  # Allow time for the page to load (you may need to adjust this)

        # Take a screenshot
        driver.save_screenshot(file_path)
        print(f"Screenshot saved to {file_path} at {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Notify on Discord
        discord_message = f"Screenshot updated for {url} at {time.strftime('%Y-%m-%d %H:%M:%S')}"
        discord_payload = {"content": discord_message}
        files = {"file": open(file_path, "rb")}
        requests.post(discord_webhook_url, data=discord_payload, files=files)

    except Exception as e:
        print(f"Error capturing screenshot and notifying: {e}")

    finally:
        driver.quit()

def get_serpapi_results():
    serpapi_url = "https://serpapi.com/search"
    '''
    params = {
        "engine": engine,
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "gl": gl,
        "hl": hl,
        "currency": currency,
        "type": flight_type,
        "outbound_date": outbound_date,
        "adults": adults,
        "children": children
    }'''
    serpapi_url2 = "https://serpapi.com/search?api_key=YOUR OWN KEY7&engine=google_flights&departure_id=YUL&arrival_id=ANC&gl=us&hl=en&currency=CAD&type=2&outbound_date=2024-08-07&adults=1&children=0"
    
    try:
        #response = requests.get(serpapi_url, params=params)
        response = requests.get(serpapi_url2)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)

        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching SerpAPI results: {e}")
        return None



def parse_and_send_to_discord(json_data, discord_webhook_url):
    try:
        # Parse JSON data
        search_metadata = json_data.get("search_metadata", {})
        best_flights = json_data.get("best_flights", [])

        # Extract relevant information
        search_id = search_metadata.get("id", "")
        status = search_metadata.get("status", "")
        google_flights_url = search_metadata.get("google_flights_url", "")
        best_flight_info = best_flights[0] if best_flights else {}

        message = (
            f"Flight Search Results:\n"
            f"Search ID: {search_id}\n"
            f"Status: {status}\n"
            #f"Google Flights URL: {google_flights_url}\n\n"
            f"Best Flight Information:\n"
            f"**Price: {best_flight_info.get('price', '')}**\n"
            f"Total Duration: {best_flight_info.get('total_duration', '')}\n"
            f"Airline: {best_flight_info.get('airline', '')}\n"
            f"Flight Type: {best_flight_info.get('type', '')}\n"
            #f"Booking Token: {best_flight_info.get('booking_token', '')}\n"
            f"Layovers: {best_flight_info.get('layovers', [])}\n"
            )

        # Send message to Discord
        discord_payload = {"content": message}
        requests.post(discord_webhook_url, json=discord_payload)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    url3 = "https://serpapi.com/search?api_key=YOUR OWN KEY&engine=google_flights&departure_id=YUL&arrival_id=ANC&gl=us&hl=en&currency=CAD&type=2&outbound_date=2024-08-07&adults=1&children=0"
    screenshot_path = "website_screenshot.png"  # Specify the file path where you want to save the screenshot
    discord_webhook_url = "YOUR OWN URL"
    while True:
        #capture_screenshot_and_notify(url3, screenshot_path, discord_webhook_url)
        serpapi_results = get_serpapi_results()
        if serpapi_results:
            # Display the obtained JSON results
            print("flight found")
            # print(json.dumps(serpapi_results, indent=2))
            parse_and_send_to_discord(serpapi_results, discord_webhook_url)
            # You can use this JSON data as needed, e.g., pass it to the previous function to send to Discord
        else:
            print("Failed to fetch SerpAPI results.")
        time.sleep(43200 )  # Sleep for 12 hour (43200  seconds)


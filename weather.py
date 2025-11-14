#!/usr/bin/env python3
"""
Weather utility for querying sunrise/sunset times from Open-Meteo.
No API key required.
"""

import urllib.request
import json
import ssl
from datetime import datetime


OPEN_METEO_API = "https://api.open-meteo.com/v1/forecast"


def get_sunrise_sunset(latitude, longitude, timezone="UTC"):
    """
    Query Open-Meteo API for today's sunrise and sunset times.
    
    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
        timezone: Timezone string (e.g., 'America/New_York')
    
    Returns:
        dict with 'sunrise' and 'sunset' as datetime objects, or None on error
    """
    try:
        # Open-Meteo endpoint for astronomical data (includes sunrise/sunset)
        url = (
            f"{OPEN_METEO_API}?"
            f"latitude={latitude}&"
            f"longitude={longitude}&"
            f"timezone={timezone}&"
            f"daily=sunrise,sunset"
        )
        
        # Create SSL context to bypass certificate verification (for development)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(url, context=ssl_context, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        # Extract today's sunrise/sunset
        daily = data.get("daily", {})
        sunrise_str = daily.get("sunrise", [None])[0]
        sunset_str = daily.get("sunset", [None])[0]
        
        if not sunrise_str or not sunset_str:
            print("  ✗ Could not retrieve sunrise/sunset data")
            return None
        
        # Parse ISO format times (e.g., "2025-11-13T07:15")
        sunrise = datetime.fromisoformat(sunrise_str)
        sunset = datetime.fromisoformat(sunset_str)
        
        return {
            "sunrise": sunrise,
            "sunset": sunset,
            "sunrise_time": sunrise.time(),
            "sunset_time": sunset.time()
        }
    
    except urllib.error.URLError as e:
        print(f"  ✗ Network error: {e}")
        return None
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"  ✗ Error parsing response: {e}")
        return None
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return None


if __name__ == "__main__":
    # Test the function
    result = get_sunrise_sunset(40.7128, -74.0060, "America/New_York")
    if result:
        print(f"Sunrise: {result['sunrise_time']}")
        print(f"Sunset:  {result['sunset_time']}")
    else:
        print("Failed to retrieve data")

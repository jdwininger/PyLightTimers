#!/usr/bin/env python3
"""
Unified configuration utility for PyLightTimers.
Manages rooms, location, and other settings via text-based UI.
"""

import json
import os
import argparse
import sys


CONFIG_FILE = "config.json"
DEFAULT_ROOMS = ["Living Room", "Bedroom", "Kitchen"]
DEFAULT_CONFIG = {
    "active_rooms": DEFAULT_ROOMS,
    "latitude": 40.7128,      # Default: New York City
    "longitude": -74.0060,
    "timezone": "America/New_York"
}


def load_config():
    """Load configuration from file, or return defaults if not found."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                # Merge with defaults to handle missing keys
                merged = DEFAULT_CONFIG.copy()
                merged.update(data)
                return merged
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✓ Configuration saved to {CONFIG_FILE}")


def toggle_room(config, room_name):
    """Toggle a room on/off in the active list."""
    rooms = config["active_rooms"]
    if room_name in rooms:
        rooms.remove(room_name)
        return False
    else:
        rooms.append(room_name)
        return True


def display_main_menu():
    """Display the main configuration menu."""
    print("\n" + "=" * 60)
    print("PYLIGHTTIMERS CONFIGURATION")
    print("=" * 60)
    print("1. Manage Rooms")
    print("2. Set Location (Latitude/Longitude)")
    print("3. Set Timezone")
    print("4. View Current Configuration")
    print("-" * 60)
    print("'s' to save and exit, 'q' to exit without saving")
    print("=" * 60)


def display_rooms_menu(config):
    """Display the room selection menu."""
    active_rooms = config["active_rooms"]
    all_rooms = sorted(set(DEFAULT_ROOMS + active_rooms))
    
    print("\n" + "=" * 60)
    print("ROOM MANAGEMENT")
    print("=" * 60)
    for i, room in enumerate(all_rooms, 1):
        status = "✓" if room in active_rooms else " "
        print(f"{i}. [{status}] {room}")
    print("-" * 60)
    print(f"{len(all_rooms) + 1}. [+] Add new room")
    print("-" * 60)
    print("Enter room number to toggle, 'a' to add new, 'b' to go back")
    print("=" * 60)
    
    return all_rooms


def run_rooms_config(config):
    """Run the room configuration UI."""
    active_rooms = config["active_rooms"]
    all_rooms = sorted(set(DEFAULT_ROOMS + active_rooms))

    while True:
        all_rooms = display_rooms_menu(config)
        choice = input("Selection: ").strip().lower()

        if choice == "b":
            break
        elif choice == "a":
            # Add new room
            new_room = input("Enter new room name: ").strip()
            if new_room:
                if new_room in all_rooms:
                    print(f"  ✗ '{new_room}' already exists.")
                else:
                    all_rooms.append(new_room)
                    all_rooms.sort()
                    toggle_room(config, new_room)  # Add as enabled by default
                    print(f"  ✓ '{new_room}' added and enabled.")
            else:
                print("  ✗ Room name cannot be empty.")
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(all_rooms):
                    room = all_rooms[idx]
                    status = toggle_room(config, room)
                    print(f"  → {room}: {'enabled' if status else 'disabled'}")
                else:
                    print("  ✗ Invalid selection. Please try again.")
            except ValueError:
                print("  ✗ Please enter a number, 'a', or 'b'.")


def run_location_config(config):
    """Run the location configuration UI."""
    while True:
        print("\n" + "=" * 60)
        print("LOCATION SETTINGS")
        print("=" * 60)
        print(f"Current Latitude:  {config['latitude']}")
        print(f"Current Longitude: {config['longitude']}")
        print("-" * 60)
        print("'l' to set latitude, 'o' to set longitude, 'b' to go back")
        print("=" * 60)
        
        choice = input("Selection: ").strip().lower()
        
        if choice == "b":
            break
        elif choice == "l":
            try:
                lat = float(input("Enter latitude (-90 to 90): ").strip())
                if -90 <= lat <= 90:
                    config["latitude"] = lat
                    print(f"  ✓ Latitude set to {lat}")
                else:
                    print("  ✗ Latitude must be between -90 and 90.")
            except ValueError:
                print("  ✗ Invalid input. Please enter a number.")
        elif choice == "o":
            try:
                lon = float(input("Enter longitude (-180 to 180): ").strip())
                if -180 <= lon <= 180:
                    config["longitude"] = lon
                    print(f"  ✓ Longitude set to {lon}")
                else:
                    print("  ✗ Longitude must be between -180 and 180.")
            except ValueError:
                print("  ✗ Invalid input. Please enter a number.")
        else:
            print("  ✗ Please enter 'l', 'o', or 'b'.")


def run_timezone_config(config):
    """Run the timezone configuration UI."""
    print("\n" + "=" * 60)
    print("TIMEZONE SETTINGS")
    print("=" * 60)
    print(f"Current Timezone: {config['timezone']}")
    print("-" * 60)
    print("Common timezones: America/New_York, America/Chicago,")
    print("America/Denver, America/Los_Angeles, Europe/London,")
    print("Europe/Paris, Asia/Tokyo, Australia/Sydney")
    print("=" * 60)
    
    tz = input("Enter timezone (or 'b' to go back): ").strip()
    if tz.lower() != "b":
        config["timezone"] = tz
        print(f"  ✓ Timezone set to {tz}")


def display_current_config(config):
    """Display current configuration."""
    print("\n" + "=" * 60)
    print("CURRENT CONFIGURATION")
    print("=" * 60)
    print(f"Active Rooms: {', '.join(config['active_rooms'])}")
    print(f"Latitude:     {config['latitude']}")
    print(f"Longitude:    {config['longitude']}")
    print(f"Timezone:     {config['timezone']}")
    print("=" * 60)
    input("Press Enter to continue...")


def run_interactive_config():
    """Run the interactive configuration UI."""
    config = load_config()

    while True:
        display_main_menu()
        choice = input("Selection: ").strip().lower()

        if choice == "q":
            print("Exiting without saving.")
            break
        elif choice == "s":
            save_config(config)
            break
        elif choice == "1":
            run_rooms_config(config)
        elif choice == "2":
            run_location_config(config)
        elif choice == "3":
            run_timezone_config(config)
        elif choice == "4":
            display_current_config(config)
        else:
            print("  ✗ Invalid selection. Please try again.")


def main():
    """CLI entry point for config.py."""
    parser = argparse.ArgumentParser(description="PyLightTimers Configuration")
    parser.add_argument("-i", "--interactive", action="store_true",
                       help="Run interactive configuration UI (default)")
    args = parser.parse_args()
    
    # Always run interactive for now (default behavior)
    run_interactive_config()


if __name__ == "__main__":
    main()

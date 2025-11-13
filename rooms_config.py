#!/usr/bin/env python3
"""
Room configuration utility with a text-based UI for selecting/deselecting rooms.
"""

import json
import os


CONFIG_FILE = "rooms.json"
DEFAULT_ROOMS = ["Living Room", "Bedroom", "Kitchen"]


def load_rooms():
    """Load active rooms from config file, or return defaults if not found."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("active_rooms", DEFAULT_ROOMS)
        except (json.JSONDecodeError, IOError):
            return DEFAULT_ROOMS
    return DEFAULT_ROOMS


def save_rooms(rooms):
    """Save active rooms to config file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({"active_rooms": rooms}, f, indent=2)
    print(f"✓ Rooms saved to {CONFIG_FILE}")


def toggle_room(rooms, room_name):
    """Toggle a room on/off in the active list."""
    if room_name in rooms:
        rooms.remove(room_name)
        return False
    else:
        rooms.append(room_name)
        return True


def display_menu(rooms, all_rooms):
    """Display the room selection menu."""
    print("\n" + "=" * 50)
    print("ROOM SELECTION MENU")
    print("=" * 50)
    for i, room in enumerate(all_rooms, 1):
        status = "✓" if room in rooms else " "
        print(f"{i}. [{status}] {room}")
    print("-" * 50)
    print(f"{len(all_rooms) + 1}. [+] Add new room")
    print("-" * 50)
    print("Enter room number to toggle, 'a' to add new, 'q' to quit, 's' to save and exit")
    print("=" * 50)


def run_config():
    """Run the interactive room configuration UI."""
    active_rooms = load_rooms()
    all_rooms = sorted(set(DEFAULT_ROOMS + active_rooms))

    while True:
        display_menu(active_rooms, all_rooms)
        choice = input("Selection: ").strip().lower()

        if choice == "q":
            print("Exiting without saving.")
            break
        elif choice == "s":
            save_rooms(active_rooms)
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
                    toggle_room(active_rooms, new_room)  # Add as enabled by default
                    print(f"  ✓ '{new_room}' added and enabled.")
            else:
                print("  ✗ Room name cannot be empty.")
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(all_rooms):
                    room = all_rooms[idx]
                    status = toggle_room(active_rooms, room)
                    print(f"  → {room}: {'enabled' if status else 'disabled'}")
                else:
                    print("  ✗ Invalid selection. Please try again.")
            except ValueError:
                print("  ✗ Please enter a number, 'a', 'q', or 's'.")


if __name__ == "__main__":
    run_config()

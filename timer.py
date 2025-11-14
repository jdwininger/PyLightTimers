import time
import random
import datetime
import argparse
import sys
from config import load_config
from weather import get_sunrise_sunset

def generate_random_number(start, end):
    return random.randint(start, end)

class Room:
    def __init__(self, name):
        self.name = name
        self.light_on = False

    def toggle_light(self):
        self.light_on = not self.light_on

# Load active rooms from config file
config = load_config()
active_room_names = config["active_rooms"]
rooms = [Room(name) for name in active_room_names]

# Stage 3 decision: single random bit (0 or 1)
# We'll generate a single 0/1 with `generate_random_number(0, 1)` and
# use that to decide whether to change the selected room's light.
# If the room is ON: 0 -> turn off, 1 -> leave on
# If the room is OFF: 1 -> turn on, 0 -> leave off

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="PyLightTimers")
    p.add_argument("-i", "--interval", type=int, choices=(15, 30), default=15,
                   help="Interval size in minutes for Stage 1 (15 or 30). Default: 15")
    p.add_argument("-c", "--config", action="store_true",
                   help="Run configuration UI and exit")
    p.add_argument("--use-sunset", action="store_true",
                   help="Use sunset/sunrise times instead of fixed 6pm-8am window")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    
    # Handle --config flag
    if args.config:
        from config import run_interactive_config
        run_interactive_config()
        return
    
    interval_minutes = args.interval
    use_sunset = args.use_sunset

    while True:
        # Determine active window: either fixed (6pm-8am) or dynamic (sunset-sunrise)
        if use_sunset:
            # Fetch sunrise/sunset times from Open-Meteo
            weather_data = get_sunrise_sunset(
                config["latitude"],
                config["longitude"],
                config["timezone"]
            )
            if weather_data:
                start_time = weather_data["sunset_time"]
                end_time = weather_data["sunrise_time"]
                print(f"Using dynamic times: sunset={start_time}, sunrise={end_time}")
            else:
                print("  ! Failed to get sunrise/sunset; using default 6pm-8am")
                start_time = datetime.time(18, 0)  # 6pm
                end_time = datetime.time(8, 0)     # 8am
        else:
            start_time = datetime.time(18, 0)  # 6pm
            end_time = datetime.time(8, 0)     # 8am

        def in_active_window(now=None):
            if now is None:
                now = datetime.datetime.now()
            current_time = now.time()
            # window wraps midnight when start > end
            if start_time <= end_time:
                return start_time <= current_time < end_time
            else:
                return current_time >= start_time or current_time < end_time

        now = datetime.datetime.now()
        if not in_active_window(now):
            # compute next start datetime
            next_start = now.replace(
                hour=start_time.hour,
                minute=start_time.minute,
                second=start_time.second,
                microsecond=0
            )
            if now.time() >= start_time:
                # we're after today's start -> next start is tomorrow
                next_start += datetime.timedelta(days=1)
            seconds_to_sleep = (next_start - now).total_seconds()
            print(f"Outside active window ({now.time()}). Sleeping until {next_start.time()} ({int(seconds_to_sleep)}s)...")
            time.sleep(seconds_to_sleep)
            continue

        # Stage 1: generate random time frame and wait for that amount of time
        if interval_minutes == 15:
            max_units = 12  # 12 * 15m = 3 hours max
        else:
            max_units = 6   # 6 * 30m = 3 hours max
        time_frame = generate_random_number(1, max_units)
        print(f"Waiting {time_frame} {interval_minutes} minute increments...")
        time.sleep(time_frame * interval_minutes * 60)

        # Stage 2: select a room randomly
        selected_room = rooms[generate_random_number(0, len(rooms)-1)]
        print(f"Selected room: {selected_room.name}")

        # Stage 3: decide whether to change the light state using single random bit (0/1)
        decision = generate_random_number(0, 1)
        if selected_room.light_on:
            # Light is currently on: 0 -> turn off, 1 -> leave on
            if decision == 0:
                selected_room.toggle_light()
                print("Light turned off")
            else:
                print("Left light on")
        else:
            # Light is currently off: 1 -> turn on, 0 -> leave off
            if decision == 1:
                selected_room.toggle_light()
                print("Light turned on")
            else:
                print("Left light off")


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nExiting")
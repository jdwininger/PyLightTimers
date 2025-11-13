import time
import random

def generate_random_number(start, end):
    return random.randint(start, end)

class Room:
    def __init__(self, name):
        self.name = name
        self.light_on = False

    def toggle_light(self):
        self.light_on = not self.light_on

# create rooms and add to a list or dictionary
rooms = [Room("Living Room"), Room("Bedroom"), Room("Kitchen")]

# Stage 3 decision: single random bit (0 or 1)
# We'll generate a single 0/1 with `generate_random_number(0, 1)` and
# use that to decide whether to change the selected room's light.
# If the room is ON: 0 -> turn off, 1 -> leave on
# If the room is OFF: 1 -> turn on, 0 -> leave off

while True:

    # Stage 1: generate random time frame and wait for that amount of time
    time_frame = generate_random_number(1,12) # in 15 minute increments
    print(f"Waiting {time_frame} 15 minute increments...")
    time.sleep(time_frame * 900) # convert 1/4 hours to seconds

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
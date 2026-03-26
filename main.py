from elevator import Elevator
from passenger import Passenger
import random
import time

# -------------------------
# SETUP
# -------------------------
MAX_FLOOR = 10

# Add capacity here (e.g., 4 passengers)
e1 = Elevator("A", 0)
e2 = Elevator("B", 6)
e3 = Elevator("C", 2)
elevators = [e1, e2, e3]

passengers = []
step = 0

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def spawnPassenger():
    start = random.randint(0, MAX_FLOOR)
    end = random.randint(0, MAX_FLOOR)
    while end == start:
        end = random.randint(0, MAX_FLOOR)

    name = f"P{len(passengers)}"
    p = Passenger(start, end, name)
    passengers.append(p)
    print(f"{name} spawned at {start} → {end}")
    p.callElevator(elevators)


def printBuilding():
    print("-" * 25)
    for floor in reversed(range(MAX_FLOOR + 1)):
        line = f"{floor:2} | "
        for elevator in elevators:
            if elevator.currentFloor == floor:
                if elevator.getDirection() == "up":
                    line += f" E{elevator.label}↑"
                if elevator.getDirection() == "down":
                    line += f" E{elevator.label}↓"
                if elevator.getDirection() == "idle":
                    line += f" E{elevator.label}𝗓"
            else:
                line += " .  "

        for p in passengers:
            if p.currentFloor == floor and p.status == "waiting":
                if p.direction == "up":
                    line += f" {p.name}↑ "
                if p.direction == "down":
                    line += f" {p.name}↓ "

        print(line)
    print("-" * 25)


def getState():
    return {
        "elevators": [
            {
                "label": e.label,
                "floor": e.currentFloor,
                "direction": e.direction,
                "floorsToGo": e.floorsToGo,
                "numPassengers": e.numPassengers
            }
            for e in elevators
        ],
        "passengers": [
            {
                "name": p.name,
                "floor": p.currentFloor,
                "status": p.status,
                "direction": p.direction,
                "targetFloor": p.targetFloor,
                "elevator": p.elevator.label if p.elevator else None
            }
            for p in passengers
            if not (
                p.status == "at target floor"
                and hasattr(p, "arrivalTime")
                and time.time() - p.arrivalTime > 3
            )
        ],
        "steps": step
    }


# -------------------------
# SIMULATION LOOP
# -------------------------
def run_simulation():
    global step

    spawnPassenger()  # start with one passenger

    while True:
    # while any(p.status != "at target floor" for p in passengers):

        print(f"\n=== Step {step} ===")

        # 1️⃣ Randomly spawn passengers
        if random.random() < 0.3:
            spawnPassenger()

        for elevator in elevators:
            # print(elevator.label, elevator.getFloorsToGo())
            arrivedFloor = elevator.move()

            # Move passengers inside the elevator with it
            for p in passengers:
                if p.status == "in elevator" and p.elevator == elevator:
                    p.setCurrentFloor(elevator.getCurrentFloor())

            # 🚨 If elevator stops at a floor
            if arrivedFloor is not None:

                # 2️⃣ Passengers GET OFF
                exiting = [p for p in passengers if p.status == "in elevator" and p.elevator == elevator and p.targetFloor == arrivedFloor]
                for p in exiting:
                    p.atTarget()
                    elevator.numPassengers -= 1
                    print(f"{p.name} got OFF at {arrivedFloor}")

                # 3️⃣ Passengers GET ON
                waiting_here = [p for p in passengers if p.status == "waiting" and p.currentFloor == arrivedFloor and p.elevator == elevator]# and p.elevator.getDirection() == p.getDirection()]
                for p in waiting_here:
                    if elevator.numPassengers < elevator.capacity:
                        p.status = "in elevator"
                        elevator.numPassengers += 1
                        print(f"{p.name} got ON at {arrivedFloor}")
                    else:
                        # elevator full → passenger will try again next step
                        print(f"{p.name} could NOT get on Elevator {elevator.label} (full)")
                        p.elevator = None  # reset elevator so they can re-call
                for p in waiting_here:
                        p.elevatorArrives()

        # 4️⃣ Re-call elevators if needed
        for p in passengers:
            if p.status == "waiting":
                if p.elevator is None:
                    p.callElevator(elevators)
                else:
                    e = p.elevator
                    if p.currentFloor not in e.getFloorsToGo():
                        print(f"{p.name} is re-calling elevator")
                        p.callElevator(elevators)

        # printBuilding()
        step += 1
        # input("continue: ")
        time.sleep(1)

        # print("All passengers served")
import time

class Passenger:
    def __init__(self, currentFloor=0, targetFloor=1, name=""):
        self.currentFloor = currentFloor
        self.targetFloor = targetFloor
        self.name = name
        self.status = "idle"  # idle, waiting, in elevator, at target floor
        self.updateDirection()
        self.stepsWaited = 0
        self.arrivalTime = None
        self.elevator = None

    def setCurrentFloor(self, floor):
        self.currentFloor = floor
        self.updateDirection()

    def setTargetFloor(self, floor):
        self.targetFloor = floor
        self.updateDirection()

    def setCurrentTarget(self, current, target):
        self.currentFloor = current
        self.targetFloor = target
        self.updateDirection()

    def setElevator(self, elevator):
        self.elevator = elevator

    def newStepWaited(self):
        self.stepsWaited += 1
    
    def updateDirection(self):
        if self.targetFloor > self.currentFloor:
            self.direction = "up"
        elif self.targetFloor < self.currentFloor:
            self.direction = "down"
        else:
            self.direction = None

    def getDirection(self):
        return self.direction
    def getStepsWaited(self):
        return self.stepsWaited

    def callElevator(self, elevators):
        if self.direction not in ("up", "down"):
            return

        self.status = "waiting"

        bestElevator = None
        bestScore = float("inf")

        for elevator in elevators:
            eFloor = elevator.getCurrentFloor()
            eDir = elevator.getDirection()
            eFTG = elevator.getFloorsToGo()

            valid = False

            if eDir == "idle":
                valid = True
            elif eDir == "up" and eFloor <= self.currentFloor:
                valid = True
            elif eDir == "down" and eFloor >= self.currentFloor:
                valid = True
            
            if len(eFTG) <= 5:
                valid = True

            if not valid:
                continue

            score = abs(eFloor - self.currentFloor)

            # prefer matching direction
            if len(eFTG) > 2:
                if self.currentFloor > min(eFTG) or self.currentFloor < max(eFTG):
                    if eDir == "up" and eFloor <= self.currentFloor:
                        score += 6
                    elif eDir == "down" and eFloor >= self.currentFloor:
                        score += 6
                else:
                    if eDir != self.direction:
                        score += 5
            if self.currentFloor in eFTG:
                score -= 1
            if eDir == "idle":
                score -= 3
            

            if score < bestScore:
                bestScore = score
                bestElevator = elevator

        # If we found a good elevator, call it
        if bestElevator is not None:
            self.elevator = bestElevator
            print(self.elevator.label)
            return self.elevator.newWaiting(self.currentFloor, self.direction)

    def elevatorArrives(self):
        if self.elevator is not None:
            self.elevator.newWaiting(self.targetFloor, self.direction)


    def atTarget(self):
        self.status = "at target floor"
        self.direction = None
        self.arrivalTime = time.time()  # 👈 add this

    def __repr__(self):
        return f"Passenger({self.currentFloor}->{self.targetFloor}, status={self.status}, direction={self.direction})"
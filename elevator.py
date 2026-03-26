class Elevator:
    def __init__(self, label, currentFloor=0, minFloor=0, maxFloor=10, numPassengers=0):
        self.label = label
        self.currentFloor = currentFloor
        self.numPassengers = numPassengers
        self.capacity = 8
        self.floorsToGo = []
        self.floorsToGoUp = []
        self.floorsToGoDown = []
        self.nextFloor = None
        self.direction = "idle" # 'up', 'down', or 'idle'
        self.minFloor = minFloor
        self.maxFloor = maxFloor

    def getCurrentFloor(self):
        return self.currentFloor
    def getNumPassengers(self):
        return self.numPassengers
    def getFloorsToGo(self):
        return self.floorsToGo
    def getDirection(self):
        return self.direction

    def upOneFloor(self, entering=0, leaving=0):
        self.currentFloor += 1
        self.numPassengers += entering
        self.numPassengers -= leaving

    def downOneFloor(self, entering=0, leaving=0):
        self.currentFloor -= 1
        self.numPassengers += entering
        self.numPassengers -= leaving

    def goToFloor(self, floor, entering=0, leaving=0):
        self.currentFloor = floor
        self.numPassengers += entering
        self.numPassengers -= leaving
    

    def newWaiting(self, waitingOn, direction):
        if direction == "up":
            if waitingOn not in self.floorsToGoUp:
                self.floorsToGoUp.append(waitingOn)

        elif direction == "down":
            if waitingOn not in self.floorsToGoDown:
                self.floorsToGoDown.append(waitingOn)



    def determineNextFloor(self):
        self.floorsToGo = self.floorsToGoUp + self.floorsToGoDown
        if not self.floorsToGo:
            self.nextFloor = None
            return
        
        if self.direction == "idle":
            if self.floorsToGo[0] > self.currentFloor:
                self.direction = "up"
            elif self.floorsToGo[0] < self.currentFloor:
                self.direction = "down"
            else:
                self.direction = "idle"
                self.nextFloor = self.currentFloor
                return

        if self.direction == "up":
            self.floorsToGo = sorted(self.floorsToGoUp) + sorted(self.floorsToGoDown, reverse=True)
            for floor in self.floorsToGo:
                if floor > self.currentFloor:
                    self.nextFloor = floor
                    return
            self.nextFloor = self.floorsToGo[0]
            self.direction = "idle"

        elif self.direction == "down":
            self.floorsToGo = sorted(self.floorsToGoDown, reverse=True) + sorted(self.floorsToGoUp)
            for floor in self.floorsToGo:
                if floor < self.currentFloor:
                    self.nextFloor = floor
                    return
            self.nextFloor = self.floorsToGo[0]
            self.direction = "idle"


    def move(self):
        self.determineNextFloor()

        if self.nextFloor is None:
            self.direction = "idle"
            return None

        # Move ONE floor toward target
        if self.currentFloor < self.nextFloor:
            self.direction = "up"
            self.currentFloor += 1
        elif self.currentFloor > self.nextFloor:
            self.direction = "down"
            self.currentFloor -= 1

        print(f"Elevator {self.label} at floor {self.currentFloor} going {self.direction}")

        # Only "ding" when you actually arrive
        if self.currentFloor == self.nextFloor:
            print(f"🔔 Ding! Elevator {self.label} arrived at floor {self.currentFloor}")

            if self.currentFloor in self.floorsToGo:
                self.floorsToGo.remove(self.currentFloor)
            if self.currentFloor in self.floorsToGoUp:
                self.floorsToGoUp.remove(self.currentFloor)
            if self.currentFloor in self.floorsToGoDown:
                self.floorsToGoDown.remove(self.currentFloor)

            return self.currentFloor

        if self.currentFloor in self.floorsToGo:
            self.floorsToGo.remove(self.currentFloor)
        if self.currentFloor in self.floorsToGoUp:
            self.floorsToGoUp.remove(self.currentFloor)
        if self.currentFloor in self.floorsToGoDown:
            self.floorsToGoDown.remove(self.currentFloor)

        self.determineNextFloor()
        return None
    


        
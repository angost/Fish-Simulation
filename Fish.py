
from random import randint
WIDTH = 640
HEIGHT = 1080

class Fish:
    def __init__(self, name: str, base_size: float, color: tuple[int, int, int], speed: float, max_hunger: float):
        self.name = name
        self.base_size = base_size
        self.color = color
        self.speed = speed
        self.max_hunger = max_hunger
        self.hunger = max_hunger
        self.pos = [randint(0, WIDTH), randint(0, HEIGHT)]
        self.direction = 1
        self.alive = True

    def swim(self):
        if self.alive:
            self.pos[0] += self.direction
            # Turn if reached screen border
            if self.pos[0] == WIDTH or self.pos[0] == 0:
                self.direction *= -1

            self.hunger -= self.max_hunger * 0.05
            if self.hunger <= 0:
                self.alive = False
                print("x_x")
                
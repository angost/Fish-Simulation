
from random import randint
WIDTH = 800
HEIGHT = 600

class Fish:
    def __init__(self, name: str, base_size: float, color: tuple[int, int, int], speed: float, max_hunger: float):
        self.name = name
        self.base_size = base_size
        self.size = self.base_size
        self.color = color
        self.speed = speed
        self.max_hunger = max_hunger
        self.hunger = max_hunger
        self.pos = [randint(0, WIDTH), randint(0, HEIGHT)]
        self.direction_horizontal = 1
        self.direction_vertical = 1
        self.alive = True

    def __str__(self):
        fish_info = self.name.ljust(20) + " Size: " + str(self.size) + " Speed: " + str(self.speed) + " Hunger: " + str(self.hunger)
        return fish_info

    def swim(self):
        if self.alive:
            self.pos[0] += self.direction_horizontal * self.speed
            self.pos[1] += self.direction_vertical * self.speed
            # print(self.pos[0])
            # Turn if reached screen border
            if self.pos[0] >= WIDTH or self.pos[0] <= 0:
                self.direction_horizontal *= -1
            if self.pos[1] >= HEIGHT or self.pos[1] <= 0:
                self.direction_vertical *= -1


            self.hunger -= (self.max_hunger * 0.0001)*self.speed
            if self.hunger <= 0:
                self.alive = False
                print("x_x")

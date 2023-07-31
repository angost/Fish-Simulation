
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
        self.direction_horizontal = 1   # 1 = swimming right, -1 = swimming left
        self.direction_vertical = 1     # 1 = swimming down, -1 = swimming up
        self.alive = True
        self.following_target = None


    def __str__(self):
        fish_info = self.name.ljust(20) + " Size: " + str(self.size) + " Speed: " + str(self.speed) + " Hunger: " + str(self.hunger)
        return fish_info


    def swim(self, all_fish):
        if self.alive:
            if self.hunger >= self.max_hunger/2:
                self.neutral_swim()
            else:
                self.follow_swim(all_fish)

            self.hunger -= (self.max_hunger * 0.01)*self.speed
            if self.hunger <= 0:
                self.alive = False
                print("x_x")


    def neutral_swim(self):
        self.pos[0] += self.direction_horizontal * self.speed
        self.pos[1] += self.direction_vertical * self.speed
        # print(self.pos[0])
        # Turn if reached screen border
        if self.pos[0] >= WIDTH or self.pos[0] <= 0:
            self.direction_horizontal *= -1
        if self.pos[1] >= HEIGHT or self.pos[1] <= 0:
            self.direction_vertical *= -1


    def follow_swim(self, all_fish):
        # Finding target (nearest smaller fish) if not found already
        if not self.following_target:
            self.following_target = self.find_nearest_target(all_fish)
        # Following the target - changing coordinates to be closer to it
        # x axis
        if self.following_target.pos[0] < self.pos[0]:
            self.pos[0] -=  self.speed
        else:
            self.pos[0] +=  self.speed
        # y axis
        if self.following_target.pos[1] < self.pos[1]:
            self.pos[1] -=  self.speed
        else:
            self.pos[1] +=  self.speed


    def find_nearest_target(self, all_fish: list):
        # Target - smaller fish
        # self doesn't end up in targets list beaceuse its not true that self.size < self.size; if lookingfor targets method were to change, self not being in targets list has to be guaranteed
        targets = [fish for fish in all_fish if fish.size < self.size]
        nearest_target = min(targets, key = lambda fish : calculate_distance(self.pos, fish.pos))
        return nearest_target
        # TODO: ASSURE TARGET IS NOT DEAD


def calculate_distance(pos1: list[float, float], pos2: list[float, float]):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
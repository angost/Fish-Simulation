
from random import randint
from math import sqrt
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

            self.hunger -= (self.max_hunger * 0.0001)*self.speed
            if self.hunger <= 0:
                self.alive = False
                print("x_x")


    def neutral_swim(self):
        self.pos[0] += self.direction_horizontal * self.speed/2
        self.pos[1] += self.direction_vertical * self.speed/2
        # print(self.pos[0])
        # Turn if reached screen border
        if self.pos[0] >= WIDTH or self.pos[0] <= 0:
            self.direction_horizontal *= -1
        if self.pos[1] >= HEIGHT or self.pos[1] <= 0:
            self.direction_vertical *= -1


    def follow_swim(self, all_fish):
        # FINDING TARGET (nearest smaller fish) if not found already
        if not self.following_target:
            self.following_target = self.find_nearest_target(all_fish)
        # Did not find a target (self.target is still None) -> do neutral swim
        if not self.following_target:
            self.neutral_swim()
        # Found a target -> follow it
        else:
            # Changing coordinates to be closer to target
            # x axis
            if self.following_target.pos[0] < self.pos[0]:
                self.pos[0] -= self.speed/2
            else:
                self.pos[0] += self.speed/2
            # y axis
            if self.following_target.pos[1] < self.pos[1]:
                self.pos[1] -= self.speed/2
            else:
                self.pos[1] += self.speed/2

            # CHECKING IF FISH CAUGHT UP THE TARGET
            if self.check_if_overlapping(self.following_target):
                self.eat_other_fish(self.following_target)


    def find_nearest_target(self, all_fish: list):
        # Target - smaller fish
        # self doesn't end up in targets list beaceuse its not true that self.size < self.size; if lookingfor targets method were to change, self not being in targets list has to be guaranteed
        targets = [fish for fish in all_fish if fish.size < self.size]
        # Returns None when there are no smaller fish
        if len(targets) == 0:
            return None
        nearest_target = min(targets, key = lambda fish : calculate_pos_difference(self.pos, fish.pos))
        return nearest_target
        # TODO: ASSURE TARGET IS NOT DEAD


    def check_if_overlapping(self, other_fish):
        # For fish as circles miniumum distance without overlapping is size (radius) of one fish + size (radius) of other fish
        # Checking if distance between fish is smaller than that
        return self.calculate_distance(other_fish) < self.size + other_fish.size


    def calculate_distance(self, other_fish):
        return sqrt((self.pos[0] - other_fish.pos[0])**2 + (self.pos[1] - other_fish.pos[1])**2)


    def die(self):
        self.alive = False


    def grow(self, amount):
        self.size += amount




    #def eat_fish(other)
    # area1 + area2 -> calc radius -> this is new radius



def calculate_pos_difference(pos1: list[float, float], pos2: list[float, float]):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
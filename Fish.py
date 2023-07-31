
from random import randint, randrange, uniform
from math import sqrt, pi
import pygame
# WIDTH = 800
# HEIGHT = 600
WIDTH = 1024
HEIGHT = 768

class Fish:
    def __init__(self, name: str, img_path: str, base_size: list[float, float], speed: float, max_hunger: float = 100):
        self.name = name
        # [width, height]
        self.size = base_size
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        self.speed = speed
        self.max_hunger = max_hunger
        self.prey_hunger = max_hunger/2
        self.change_hunger(round(uniform(max_hunger*2/3, max_hunger), 2))
        # self.change_hunger(randrange(round(max_hunger*2/3), max_hunger, 5))
        # self.pos = center of the image
        self.pos = [randint(0, WIDTH), randint(0, HEIGHT)]
        self.img_pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2]
        self.direction_horizontal = 1   # 1 = swimming right, -1 = swimming left
        self.direction_vertical = 1     # 1 = swimming down, -1 = swimming up
        self.alive = True
        self.following_target = None


    def __str__(self):
        fish_info = self.name.ljust(20) + " Size: " + str(self.size) + " Speed: " + str(self.speed) + " Hunger: " + str(self.hunger)
        return fish_info


    def change_pos(self, x_diff, y_diff):
        self.pos[0] += x_diff
        self.img_pos[0] += x_diff

        self.pos[1] += y_diff
        self.img_pos[1] += y_diff


    def swim(self, all_fish):
        if self.alive:
            if self.hunger >= self.prey_hunger:
                self.neutral_swim()
            else:
                self.follow_swim(all_fish)

            self.change_hunger(self.hunger - (self.max_hunger * 0.0001)*self.speed)
            if self.hunger <= 0:
                self.die()
        else:
            # Falling to the bottom of the screen
            if self.pos[1] < HEIGHT:
                self.change_pos(0, 1)


    def neutral_swim(self):
        self.change_pos(self.direction_horizontal * self.speed/2, self.direction_vertical * self.speed/2)
        # Turn if reached screen border
        if self.pos[0] >= WIDTH or self.pos[0] <= 0:
            self.direction_horizontal *= -1
        if self.pos[1] >= HEIGHT or self.pos[1] <= 0:
            self.direction_vertical *= -1


    def follow_swim(self, all_fish):
        # FINDING TARGET (nearest smaller fish) if not found already or previous target died or previous target got too big
        if not self.following_target or not self.following_target.alive or self.following_target.area() > self.area():
            self.following_target = self.find_nearest_target(all_fish)
            if self.following_target:
                print(self.name + " is hungry...")
        # Did not find a target (self.target is still None) -> do neutral swim
        if not self.following_target:
            self.neutral_swim()
        # Found a target -> follow it
        else:
            # Changing coordinates to be closer to target
            # x axis
            if self.following_target.pos[0] < self.pos[0]:
                self.change_pos(-self.speed/2, 0)
            else:
                self.change_pos(self.speed/2, 0)
            # y axis
            if self.following_target.pos[1] < self.pos[1]:
                self.change_pos(0, -self.speed/2)
            else:
                self.change_pos(0, self.speed/2)

            # CHECKING IF FISH CAUGHT UP THE TARGET
            if self.check_if_overlapping(self.following_target):
                self.eat_other_fish(self.following_target)


    def find_nearest_target(self, all_fish: list):
        '''Finds nearest target. Target = alive! smaller fish\n
        Calculates distance between centres of imgs'''
        # TIP: self doesn't end up in targets list beaceuse its not true that self.size < self.size; if lookingfor targets method were to change, self not being in targets list has to be guaranteed
        targets = [fish for fish in all_fish if (fish.alive and fish.area() < self.area())]
        # Returns None when there are no smaller fish
        if len(targets) == 0:
            return None
        nearest_target = min(targets, key = lambda fish : self.calculate_distance(fish))
        return nearest_target


    def check_if_overlapping(self, other_fish):
        if self.img_pos[0] < other_fish.img_pos[0]:
            left_object, right_object = self, other_fish
        else:
            left_object, right_object = other_fish, self
        # Right side of left object overlaps with left side of right object
        horizontal_overlap = left_object.img_pos[0] + left_object.size[0] > right_object.img_pos[0]

        if self.img_pos[1] < other_fish.img_pos[1]:
            top_object, bottom_object = self, other_fish
        else:
            top_object, bottom_object = other_fish, self
        # Bottom side of top object overlaps with top side of bottom object
        vertical_overlap = top_object.img_pos[1] + top_object.size[1] > bottom_object.img_pos[1]

        return horizontal_overlap and vertical_overlap


    def calculate_distance(self, other_fish):
        return sqrt((self.pos[0] - other_fish.pos[0])**2 + (self.pos[1] - other_fish.pos[1])**2)


    def grow_to_size(self, new_size: list[float, float]):
        self.size = new_size
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        # Also updates img_pos (when growing, center stays in the same place, but top left corner of img changes)
        self.img_pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2]


    def area(self):
        return self.size[0] * self.size[1]


    def change_hunger(self, new_hunger):
        new_hunger = max(0, new_hunger)
        new_hunger = min(self.max_hunger, new_hunger)
        self.hunger = new_hunger

        self.update_color()


    def update_color(self):
        '''Updates fish color according to its hunger level.\n
        Green - full hunger bar, yellow - less full, red - getting to prey lvl, black - preying'''
        # Two possible values - bigger ex.227, smaller ex.61; Two components are always the same
        # G bigger - green; R,G bigger - yellow; R bigger - red; B bigger - blue; etc.
        green =     (61, 227, 61)
        yellow =    (227, 227, 61)
        red =       (227, 61, 61)
        black =     (0,0,0)

        if self.hunger <= self.prey_hunger:
            new_color = black
        elif self.hunger == self.max_hunger:
            new_color = green
        # Calculate proper color
        else:
            # Calculating how many steps from red (prey color) have to be taken; red -> yellow -> green
            max_nr_of_color_steps = abs(green[0] - yellow[0]) + abs(yellow[1] - red[1])
            max_nr_of_hunger_steps = self.max_hunger - self.prey_hunger
            component_steps_left = round((self.hunger - self.prey_hunger) * (max_nr_of_color_steps/max_nr_of_hunger_steps))
            new_color = list(red)

            # Making as many component steps as needed
            # red -> yellow
            max_G_component_steps = yellow[1] - red[1]
            new_color[1] += min(max_G_component_steps, component_steps_left)
            component_steps_left = max(0, component_steps_left - max_G_component_steps)
            # yellow -> green
            max_R_component_steps = yellow[0] - green[0]
            new_color[0] -= min(max_R_component_steps, component_steps_left)
            component_steps_left = max(0, component_steps_left - max_R_component_steps)

            new_color = tuple(new_color)

        self.color = new_color


    def eat_other_fish(self, other_fish):
        ''' Fish gets more hunger and grows. Other fish dies.'''
        old_area = self.area()
        # Fish absorbs eaten fish area
        w_to_h = self.size[0]/self.size[1]
        new_area = self.area() + other_fish.area()
        new_h = sqrt(new_area / w_to_h)
        new_w = new_h * w_to_h
        self.grow_to_size([new_w, new_h])

        self.change_hunger(self.hunger + sqrt(other_fish.area()))
        self.following_target = None

        print("Dziab!!\t" + self.name + " has eaten " + other_fish.name + ". Size: " + str(old_area) + " -> " + str(new_area))
        other_fish.die()


    def die(self):
        self.alive = False
        self.img_path = "assets/fish_bones.png"
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        print("x_x")


class BlueFish(Fish):
    def __init__(self):
        super().__init__("Bluefish", "assets/blue_fish.png", [35, 35], 1)

class SwordFish(Fish):
    def __init__(self):
        super().__init__("Sword-fish", "assets/sword_fish.png", [80, 60], 2.5)

class CatFish(Fish):
    def __init__(self):
        super().__init__("Catfish", "assets/catfish.png", [80, 50], 1)

class NemoFish(Fish):
    def __init__(self):
        super().__init__("Nemo", "assets/clown_fish.png", [50, 50], 2)

class GoldFish(Fish):
    def __init__(self):
        super().__init__("Goldfish", "assets/goldfish.png", [35, 35], 1)

class FishGroup(Fish):
    def __init__(self):
        super().__init__("Fish group", "assets/fish_group2.png", [80, 80], 2)

class PufferFish(Fish):
    def __init__(self):
        super().__init__("Puffer-fish", "assets/puffer_fish.png", [90, 90], 1)

class TropicalFish(Fish):
    def __init__(self):
        super().__init__("Tropical fish", "assets/tropical_fish.png", [50, 40], 1.5)

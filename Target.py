
import pygame
from math import sqrt


class PointTarget():
    ''' Target with just position '''
    def __init__(self, pos: list[float, float]):
        # self.pos = center of the image
        self.pos = pos


    def change_pos_to(self, pos: list[float, float]):
        self.pos = pos


    def change_pos_by(self, x_diff: float, y_diff: float):
        self.pos[0] += x_diff
        self.pos[1] += y_diff


class MouseTarget(PointTarget):
    def __init__(self, pos: list[float]):
        super().__init__(pos)


class AreaTarget(PointTarget):
    ''' Target that has area and image. '''
    def __init__(self, pos: list[float], img_path: str, base_size: float):
        # self.pos = center of the image; self.img_pos = top left corner of the img
        super().__init__(pos)
        self.size = base_size
        self.img_pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2]
        # [width, height]

        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))

        self.direction_horizontal = 1   # 1 = facing right, -1 = facing left
        self.direction_vertical = 1     # 1 = facing down, -1 = facing up


    # POSITION
    def change_pos_to(self, pos: list[float, float]):
        self.pos = pos
        self.img_pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2]


    def change_pos_by(self, x_diff: float, y_diff: float):
        self.pos[0] += x_diff
        self.img_pos[0] += x_diff

        self.pos[1] += y_diff
        self.img_pos[1] += y_diff


    # DISTANCE
    def calculate_distance(self, other_target):
        return sqrt((self.pos[0] - other_target.pos[0])**2 + (self.pos[1] - other_target.pos[1])**2)


    def check_if_overlapping(self, other_target):
        if self.img_pos[0] < other_target.img_pos[0]:
            left_object, right_object = self, other_target
        else:
            left_object, right_object = other_target, self
        # Right side of left object overlaps with left side of right object
        horizontal_overlap = left_object.img_pos[0] + left_object.size[0] > right_object.img_pos[0]

        if self.img_pos[1] < other_target.img_pos[1]:
            top_object, bottom_object = self, other_target
        else:
            top_object, bottom_object = other_target, self
        # Bottom side of top object overlaps with top side of bottom object
        vertical_overlap = top_object.img_pos[1] + top_object.size[1] > bottom_object.img_pos[1]

        return horizontal_overlap and vertical_overlap


    #SIZE
    def area(self):
        return self.size[0] * self.size[1]


    def grow_to_size(self, new_size: list[float, float]):
        self.size = new_size
        self.update_img()
        # Also updates img_pos (when growing, center stays in the same place, but top left corner of img changes)
        self.img_pos = [self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2]


    # IMAGE
    def update_img(self):
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        if self.direction_horizontal == -1:
            self.img = pygame.transform.flip(self.img, True, False)












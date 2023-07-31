
import pygame
from random import randint, choice
from Fish import Fish, BlueFish, SwordFish

def fish_setup(nr_of_fish):
    fish = []
    available_fish = {0: BlueFish, 1: SwordFish}
    if len(available_fish) != 0:
        for fish_index in range(nr_of_fish):
            drawn_fish_kind = randint(0, len(available_fish)-1)
            fish.append(available_fish[drawn_fish_kind]())

    return fish


def main():
    # WIDTH = 800
    # HEIGHT = 600
    WIDTH = 1024
    HEIGHT = 768
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()

    all_fish = fish_setup(10)
    for fish in all_fish:
        print(fish)

    main_loop = True
    while main_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False

        screen.fill((42, 108, 212))
        for fish in all_fish:
            fish.swim(all_fish)
            pygame.draw.circle(screen, fish.color, fish.pos, max(fish.size)/2)
            screen.blit(fish.img, fish.img_pos)

        pygame.display.flip()
        clock.tick(45)
    pygame.quit()


main()



# f = Fish("Losos", 150, (randint(0,255), randint(0,255), randint(0,255)), 10, 20)
# print("Pos: ", f.pos[0], "Hunger: ", f.hunger)
# for i in range(300):
#     f.swim()
#     print(f.pos[0])
# print("Pos: ", f.pos[0], "Hunger: ", f.hunger)

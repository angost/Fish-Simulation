
import pygame
from random import randint, choice
from Fish import Fish, BlueFish, SwordFish, CatFish, NemoFish, GoldFish, FishGroup, PufferFish, TropicalFish

def fish_setup(nr_of_fish):
    fish = []
    available_fish = {
        0: BlueFish,
        1: SwordFish,
        2: CatFish,
        3: NemoFish,
        4: GoldFish,
        5: FishGroup,
        6: PufferFish,
        7: TropicalFish
        }

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
    transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    clock = pygame.time.Clock()

    all_fish = fish_setup(20)
    for fish in all_fish:
        print(fish)

    follow_mouse = False
    main_loop = True
    while main_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not follow_mouse and pygame.mouse.get_pressed()[0]:
                    follow_mouse = True
                    print("Follow mouse")
                elif pygame.mouse.get_pressed()[2]:
                    print("Spawn food")
                pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if follow_mouse and not pygame.mouse.get_pressed()[0]:
                    follow_mouse = False
                    print("Stop following")


        # Semi-transparent circles
        screen.fill((42, 108, 212))
        transparent_surface.fill((42, 108, 212))
        for fish in all_fish:
            pygame.draw.circle(transparent_surface, tuple(list(fish.color) + [190]), fish.pos, max(fish.size)/2)
        screen.blit(transparent_surface, (0, 0))
        # Fish imgs, functionality
        for fish in all_fish:
            screen.blit(fish.img, fish.img_pos)
            fish.swim(all_fish)


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

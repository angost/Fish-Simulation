
import pygame
from random import randint, choice
from Target import PointTarget, AreaTarget
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
    mouse_target = PointTarget([0,0])

    main_loop = True
    while main_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Started mouse following
                if not follow_mouse and pygame.mouse.get_pressed()[0]:
                    print("Follow mouse")
                    follow_mouse = True
                    # Set mouse cursor as target of every fish
                    for fish in all_fish:
                        fish.following_target = mouse_target
                elif pygame.mouse.get_pressed()[2]:
                    print("Spawn food")
            elif event.type == pygame.MOUSEBUTTONUP:
                # Stopped mouse following
                if follow_mouse and not pygame.mouse.get_pressed()[0]:
                    print("Stop following")
                    follow_mouse = False
                    # Reset every fish target to None
                    for fish in all_fish:
                        fish.following_target = None

        # Update current mouse position
        if follow_mouse:
            mouse_pos = list(pygame.mouse.get_pos())
            mouse_target.change_pos_to(mouse_pos)

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

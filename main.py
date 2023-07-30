
import pygame
from random import randint, choice
from Fish import Fish

def fish_setup(nr_of_fish):
    fish = []
    fish_names = ("Losos", "Karp", "Pstrag", "Dorsz", "Rozdymka", "Miecznik", "Nemo")

    for fish_index in range(nr_of_fish):
        fish.append(Fish
                    (choice(fish_names),
                    randint(1,300),
                    (randint(0,255), randint(0,255), randint(0,255)),
                    randint(1,20),
                    randint(5,100)))
    return fish


def main():
    WIDTH = 800
    HEIGHT = 600
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()

    fish = fish_setup(10)
    for f in fish:
        print(f)

    main_loop = True
    while main_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_loop = False

        fish[0].swim()

        screen.fill((42, 108, 212))
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

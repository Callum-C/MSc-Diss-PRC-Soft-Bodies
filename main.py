import pygame
import numpy as np
import math

from colours import FILL, SILVER, BACKGROUND_COLOUR, RED

from Classes.Particle import Particle
from Classes.Spring import Spring
from Classes.Square import Square
from Classes.C_Elegen import C_Elegen
from Classes.TestEnt import Test

# Visual Params

#(width, height) = (1280, 720)
(width, height) = (1800, 900)
entities = []
titlefont = None
myfont = None
count = 0

def main():
    global count
    clock = pygame.time.Clock()

    elegen = C_Elegen((200, 100), 5, 100)
    #entities.append(elegen)

    test = Test((200, 100))
    entities.append(test)

    screen = pygame.display.set_mode((width, height))
    screen_setup(entities, screen)

    pygame.display.update()

    running = True
    counting = False
    while running:
        clock.tick(30)

        if count == 10:
            entities[0].particles[0].locked = True
            entities[0].particles[1].locked = False
            entities[0].particles[2].locked = False

        if count == 20:
            entities[0].particles[0].locked = False
            entities[0].particles[1].locked = True
            entities[0].particles[2].locked = False
            
        if count == 30:
            entities[0].particles[0].locked = False
            entities[0].particles[1].locked = False
            entities[0].particles[2].locked = True
            count = 0

        events = pygame.event.get()
        for event in events:

            # C_Elegen Moving Head Stuff
            """
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    elegen.unlock_head()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = get_pos()
                    elegen.move_to_cursor(pos)
                    elegen.lock_head()

                if event.button == 3:
                    elegen.toggle_head_lock()
            """

            if event.type == pygame.MOUSEBUTTONDOWN:
                counting = True
                change = [np.array((-5, 0.0))]
                entities[0].add_force(change)

            if event.type == pygame.QUIT:
                running = False

        #if count > 120:
        for e in entities:
            e.update()

        update_screen(entities, screen)
        
        if counting:
            count += 1


def get_pos():
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return (pos)


def screen_setup(entities, screen):
    """
    Initialise pygame screen and draw initial state.
    
    Params
    ------

    entities: list
    List of entity objects.

    screen: Pygame Screen
    Screent to draw assets to.
    """
    global myfont, titlefont
    pygame.init()
    pygame.display.set_caption("Spring Damper")

    titlefont = pygame.font.SysFont("monospace", 20)
    myfont = pygame.font.SysFont("monospace", 15)

    update_screen(entities, screen)


def update_screen(entities, screen):
    """
    Update screen, called every frame.
    
    Params
    ------

    entities: list
    List of entity objects.

    screen: Pygame Screen
    Screen to draw assets to.
    """
    screen.fill(BACKGROUND_COLOUR)

    for e in entities:
        e.draw(screen)

    title = titlefont.render("Spring Lengths and Forces", 5, SILVER)
    screen.blit(title, (1400, 100))

    # Draw Spring Lengths to Screen
    for i, length in enumerate(entities[0].get_spring_lengths()):
        length = math.floor(length)
        label = myfont.render("{}".format(length), 1, SILVER)
        screen.blit(label, (1400, (150 + i * 50)))

    # Draw Spring Forces to Screen
    for i, force in enumerate(entities[0].get_spring_forces()):
        label = myfont.render("{}".format(force), 1, SILVER)
        screen.blit(label, (1500, (150 + i * 50)))
    
    label = myfont.render("Count: {}".format(count), 1, SILVER)
    screen.blit(label, (1500, 250))

    # pygame.draw.rect(screen, SILVER, pygame.Rect(200, 100, 400, 400), 2)

    pygame.display.update()


if __name__ == '__main__':
    main()

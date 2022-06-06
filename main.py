import pygame
import numpy as np

from Particle import Particle
from Spring import Spring

# Visual Params
FILL =      (45, 197, 244)
BACKGROUND_COLOR = (112, 50, 126)
(width, height) = (1280, 720)

def main():
    bob = Particle((640,600), FILL, mass=2)
    doge = Particle((640, 400), FILL, mass=1.5)
    anchor = Particle((640, 360), FILL, lock=False)

    spring = Spring(anchor, doge, 150, 0.01, FILL)
    spring2 = Spring(doge, bob, 150, 0.01, FILL)

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((width, height))
    screen_setup(bob, anchor, doge, spring, spring2, screen)

    running = True
    while running:
        clock.tick(60)

        # Update Springs
        spring.update()
        spring2.update()

        # Update particles
        bob.update_pos()
        anchor.update_pos()
        doge.update_pos()

        update_screen(bob, anchor, doge, spring, spring2, screen)
        
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                pos = get_pos()
                bob.set_pos(pos)
                update_screen(bob, anchor, doge, spring, spring2, screen)

            if event.type == pygame.QUIT:
                running = False

def get_pos():
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return (pos)

def screen_setup(bob, anchor, doge, spring, spring2, screen):
    """Initialise pygame screen and draw initial state."""

    pygame.init()
    pygame.display.set_caption("Spring Damper")

    update_screen(bob, anchor, doge, spring, spring2, screen) 

def update_screen(bob, anchor, doge, spring, spring2, screen):
    """Update screen, called every frame."""

    screen.fill(BACKGROUND_COLOR)

    bob.draw(screen)
    anchor.draw(screen)
    doge.draw(screen)
    spring.draw(screen)
    spring2.draw(screen)

    pygame.display.update()

if __name__ == '__main__':
    main()
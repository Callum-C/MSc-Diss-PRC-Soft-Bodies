import pygame
import numpy as np

from Classes.Particle import Particle
from Classes.Spring import Spring

# Visual Params
FILL =      (45, 197, 244)
BACKGROUND_COLOR = (112, 50, 126)
(width, height) = (1280, 720)

def main():
    clock = pygame.time.Clock()

    particles = []
    springs = []
    spacing = 50

    for i in range(10):
        particles.append(Particle((640, spacing*(i+1)), FILL, gravity=False))

        if i != 0:
            springs.append(Spring(particles[i-1], particles[i], spacing, 0.01, FILL))
    
    particles[0].locked = True


    screen = pygame.display.set_mode((width, height))
    screen_setup(particles, springs, screen)

    running = True
    while running:
        clock.tick(60)

        # Update Springs
        for spring in springs:
            spring.update()

        # Update particles
        for particle in particles:
            particle.update_pos()

        update_screen(particles, springs, screen)
        
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.MOUSEBUTTONUP:
                pos = get_pos()
                particles[len(particles)-1].set_pos(pos)
                update_screen(particles, springs, screen)

            if event.type == pygame.QUIT:
                running = False

def get_pos():
    pos = pygame.mouse.get_pos()
    pos = (float(pos[0]), float(pos[1]))
    return (pos)

def screen_setup(particles, springs, screen):
    """Initialise pygame screen and draw initial state."""

    pygame.init()
    pygame.display.set_caption("Spring Damper")

    update_screen(particles, springs, screen) 

def update_screen(particles, springs, screen):
    """Update screen, called every frame."""

    screen.fill(BACKGROUND_COLOR)

    for particle in particles:
        particle.draw(screen)
        

    for spring in springs:
        spring.draw(screen)

    pygame.display.update()

if __name__ == '__main__':
    main()
import pygame
import random
import math

pygame.init()
screenLength = 800
screenWidth = 800
window = pygame.display.set_mode((screenLength, screenWidth))
pygame.display.set_caption("2d Lander")
clock = pygame.time.Clock()

velocity = [random.randint(0, int(screenLength*4/7)), random.randint(0, int(screenWidth*4/7))]
position = [0, 0]
fuelConsumption = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #autopilot (calculating the angle and the throttle)
    modulus = math.sqrt(velocity[0]*velocity[0] + velocity[1]*velocity[1])
    angle = math.acos(velocity[0]/modulus)

    if modulus < 100:
        throttle = 1
        fuelConsumption += 1
    else:
        throttle = 3
        fuelConsumption += 3
    
    #physics
    velocity[0] = velocity[0] - throttle*math.cos(angle)
    velocity[1] = velocity[1] - throttle*math.sin(angle)

    position[0] = position[0] + velocity[0]/100
    position[1] = position[1] + velocity[1]/100
    velocity[1] += 1

    #drawing
    window.fill("white")
    pygame.draw.rect(window, "red", (position[0], position[1], 10, 10))

    #wincondition
    if position[1]+10 >= screenWidth and modulus <= 100:
        print(f"Succesfull landing (fuel consumed: {fuelConsumption})")
        pygame.quit()
        exit()
    if position[1]+10 >= screenWidth and modulus > 100:
        print("Failed landing")
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(60)
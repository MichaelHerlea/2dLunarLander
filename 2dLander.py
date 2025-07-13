import pygame
import random
import math

pygame.init()
screen_length = 800
screen_width = 800
window = pygame.display.set_mode((screen_length, screen_width))
pygame.display.set_caption("2d Lander")
clock = pygame.time.Clock()
text_font = pygame.font.SysFont(None, 30)

velocity = [random.randint(0, int(screen_length*4/7)), random.randint(0, int(screen_width*4/7))]
position = [0, 0]
fuel_consumption = 0
throttle = 1
angle = 0

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    window.blit(img, (x, y))

while True:
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    #math
    modulus = math.sqrt(velocity[0]**2 + velocity[1]**2)

    #autopilot algorithm (calculating the angle and the throttle)
    angle = math.acos(velocity[0]/modulus)

    if modulus < 100:
        throttle = 1
    else:
        throttle = 3
    
    #physics
    velocity[0] = velocity[0] - throttle*math.cos(angle)
    velocity[1] = velocity[1] - throttle*math.sin(angle)

    position[0] = position[0] + velocity[0]/100
    position[1] = position[1] + velocity[1]/100
    velocity[1] += 1

    fuel_consumption = fuel_consumption + throttle

    #drawing
    window.fill("white")
    pygame.draw.rect(window, "red", (position[0], position[1], 10, 10))
    formated_angle = round(angle*180/math.pi, 1)
    draw_text(f"Angle: {formated_angle}", text_font, "black", 0, 0)
    draw_text(f"Throttle: {throttle}", text_font, "black", 0, 20)

    #wincondition
    if position[1]+10 >= screen_width and modulus <= 100:
        print(f"Succesfull landing (fuel consumed: {fuel_consumption})")
        pygame.quit()
        exit()
    if position[1]+10 >= screen_width and modulus > 100:
        print("Failed landing")
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(60)
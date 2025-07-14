import pygame
import random
import math
from matplotlib import pyplot

pygame.init()
screen_length = 800
screen_width = 800
window = pygame.display.set_mode((screen_length, screen_width))
pygame.display.set_caption("2d Lander")
clock = pygame.time.Clock()
text_font = pygame.font.SysFont(None, 30)

star_position = []
for i in range(int((screen_length*screen_width)/1000)):
    star_position.append([random.randint(0, screen_length), random.randint(0, screen_width-100)])

lunar_lander_image = pygame.image.load("media/LunarLander.png").convert()
lunar_lander_image.set_colorkey((255, 255, 255))

velocity = [random.randint(0, int(screen_length*4/7)), random.randint(0, int(screen_width*4/7))]
position = [0, 0]
fuel_consumption = 0
throttle = 1
angle = 0

time = []
angle_over_time = []
fuel_consumption_over_time = []
throttle_over_time = []

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
    window.fill("black")
    pygame.draw.rect(window, "darkgrey", (0, screen_width-100, screen_length, 100))

    for i in range(len(star_position)):
        pygame.draw.rect(window, "white", (star_position[i][0], star_position[i][1], 2, 2))

    angle_in_degrees = round(angle*180/math.pi, 1)

    lunar_lander_image_rotated = pygame.transform.rotate(lunar_lander_image, 90-angle_in_degrees)
    window.blit(lunar_lander_image_rotated, (position[0]-20, position[1]-20))

    draw_text(f"Angle: {angle_in_degrees}", text_font, "white", 0, 0)
    draw_text(f"Throttle: {throttle}", text_font, "white", 0, 20)

    #data collection
    angle_over_time.append(angle_in_degrees)
    fuel_consumption_over_time.append(fuel_consumption)
    throttle_over_time.append(throttle)

    #wincondition
    if position[1]+20 >= screen_width-100 and modulus <= 100:
        print(f"Succesfull landing (fuel consumed: {fuel_consumption})")
        for i in range(len(angle_over_time)):
            time.append(i)
        pyplot.figure(num = "Data", figsize = (12, 5))
        pyplot.subplot(1, 3, 1)
        pyplot.plot(time, angle_over_time)
        pyplot.title("Angle")
        pyplot.subplot(1, 3, 2)
        pyplot.plot(time, fuel_consumption_over_time)
        pyplot.title("Fuel consumption")
        pyplot.subplot(1, 3, 3)
        pyplot.plot(time, throttle_over_time)
        pyplot.title("Throttle")
        pygame.quit()
        pyplot.show()
        exit()
    if position[1]+20 >= screen_width-100 and modulus > 100:
        print("Failed landing")
        pygame.quit()
        exit()

    pygame.display.update()
    clock.tick(60)
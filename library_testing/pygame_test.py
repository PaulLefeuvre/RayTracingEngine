import pygame

pygame.init()
window = pygame.display.set_mode((255, 255))
window.fill((255, 255, 255))
pygame.display.update()

for j in range(256):
    for i in range(256):
        window.fill((i, j, 0), ((i, j), (1, 1)))
        pygame.display.update()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

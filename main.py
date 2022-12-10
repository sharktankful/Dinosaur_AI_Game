import pygame
import os
import random
import sys

pygame.init()

# CONSTANT VARIABLES
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

running = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))]

jumping = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))

bg = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))

font = pygame.font.SysFont('comicsans.tff', 20)


class Dinosaur:
    x_pos = 80
    y_pos = 310
    JUMP_VEL = 8.5

    def __init__(self, image=running[0]):
        self.image = image
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.x_pos, self.y_pos, image.get_width(), image.get_height())
        self.step_index = 0
    
    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0
    
    def jump(self):
        self.image = jumping
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL
    
    def run(self):
        self.image = running[self.step_index // 5]
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos
        self.step_index += 1
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))




def main():
    clock = pygame.time.Clock()

    dinosaurs = [Dinosaur()]

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255,255,255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(screen)
        
        user_input = pygame.key.get_pressed()

        for i, dinosaur in enumerate(dinosaurs):
            if user_input[pygame.K_SPACE]:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        clock.tick(60)
        pygame.display.update()


main()
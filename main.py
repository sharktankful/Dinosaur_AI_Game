import pygame
import os
import random
import sys
import neat
import math

pygame.init()

# CONSTANT VARIABLES
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))

running = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))]

jumping = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))

small_cactus = [pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus1.png')),
                pygame.image.load(os.path.join(
                    'Assets/Cactus', 'SmallCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus3.png'))]

large_cactus = [pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus1.png')),
                pygame.image.load(os.path.join(
                    'Assets/Cactus', 'LargeCactus2.png')),
                pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus3.png'))]

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
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  
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
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        for obstacle in obstacles:
            pygame.draw.line(screen, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)

class Obstacle:
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300


def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2+dy**2)


def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20
    points = 0
    clock = pygame.time.Clock()

    obstacles = []
    dinosaurs = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render(f'Points: {str(points)}', True, (0, 0, 0))
        screen.blit(text, (950, 50))

    def statistics():
        global dinosaurs, game_speed, ge
        text_1 = font.render(f'Dinosaurs Alive: {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = font.render(f'Generation: {pop.generation+ 1}', True, (0, 0, 0))
        text_3 = font.render(f'Game Speed: {str(game_speed)}', True, (0, 0, 0))

        screen.blit(text_1, (50, 450))
        screen.blit(text_2, (50, 480))
        screen.blit(text_3, (50, 510))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = bg.get_width()
        screen.blit(bg, (x_pos_bg, y_pos_bg))
        screen.blit(bg, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(screen)

        if len(dinosaurs) == 0:
            break

        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(
                    small_cactus, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(
                    large_cactus, random.randint(0, 2)))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    remove(i)

        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate((dinosaur.rect.y, distance(
                (dinosaur.rect.x, dinosaur.rect.y), obstacle.rect.midtop)))
            if output[0] > 0.5 and dinosaur.rect.y == dinosaur.y_pos:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        statistics()
        score()
        background()
        clock.tick(30)
        pygame.display.update()


# SETUP THE NEAT
def run(config_path):
    global pop
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

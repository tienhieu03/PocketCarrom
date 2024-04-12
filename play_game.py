import pygame
import sys
import pymunk
import pymunk.pygame_util
import define as df
from define import *
from cue import Cue
import math
class PlayGame:
    def __init__(self):
        pygame.init()
        self.window_color = COLOR_BACKGROUND
        self.WINDOW_GAME = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "board.png"), (BOARD_SIZE)).convert()

        #khai bao them
        self.space = pymunk.Space()
        self.static_body = self.space.static_body
        self.draw_options = pymunk.pygame_util.DrawOptions(self.WINDOW_GAME)
        pos = (self.WINDOW_GAME.get_width() //2 , 663)
        self.cue_ball = self.create_ball(38 / 2, pos)
        self.clock = pygame.time.Clock()
        self.balls = []
        rows = 5
        dia = 38
        for col in range(5):
            for row in range(rows):
                pos = (550 + (col * (dia + 1)), 330 + (row * (dia + 1)) + (col * dia / 2))
                new_ball = self.create_ball(dia / 2, pos)
                self.balls.append(new_ball)
            rows -= 1
        self.force = 0
        new_size = (int(self.cue_ball.radius * 2), int(self.cue_ball.radius * 2))
        self.ball_image = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "striker.png").convert_alpha(), new_size)
        self.white_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "white_new.png").convert_alpha(), new_size)
        self.black_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "black_new.png").convert_alpha(), new_size)
        self.queen = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "queen.png").convert_alpha(), new_size)
        self.cue = Cue(self.cue_ball.body.position)
        self.potted_ball = []
        self.ball_images = []
    def create_ball(self,radius, pos):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.mass = 5
        shape.elasticity = 0.8
        # use pivot joint to add friction
        pivot = pymunk.PivotJoint(body, self.static_body, (0, 0), (0, 0))
        pivot.max_bias = 0
        pivot.max_force = 1000
        self.space.add(body, shape, pivot)
        return shape
    def create_cushion(self,polydim):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = ((0, 0))
        shape = pymunk.Poly(body, polydim)
        shape.elasticity = 0.8
        self.space.add(body, shape)

    def is_moving(self):
        velocity = self.cue_ball.body.velocity
        return velocity != (0, 0)

    def start_game(self):
        running = True
        mouse_pressed = False
        key_down = False
        FORCE_DIRECTION = 1
        POWERING_UP = True
        for c in CUSHION:
            self.create_cushion(c)
        while running:
            taking_shot = True
            self.space.step(1 / 60)
            dt = self.clock.tick(60) / 1000
            self.WINDOW_GAME.fill(self.window_color)
            self.WINDOW_GAME.blit(self.bg, BOARD_POSITION)
            self.WINDOW_GAME.blit(self.ball_image,(self.cue_ball.body.position[0] - self.cue_ball.radius, self.cue_ball.body.position[1] - self.cue_ball.radius))

            for i, ball in enumerate(self.balls):
                for pocket in POCKETS:
                    ball_x_dist = abs(ball.body.position[0] - pocket[0])
                    ball_y_dist = abs(ball.body.position[1] - pocket[1])
                    ball_dist = math.sqrt(ball_x_dist ** 2 + ball_y_dist ** 2)
                    if ball_dist <= POCKET_DIA / 2:
                        self.space.remove(ball.body)
                        self.balls.remove(ball)
                        self.potted_ball.append(self.ball_images[i])
                        self.ball_images.pop(i)
            #print(self.potted_ball)

            for i, ball in enumerate(self.balls):
                if i == 9:
                    self.WINDOW_GAME.blit(self.queen,(ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))
                    self.ball_images.append(self.queen)
                elif i % 2 == 0:
                    self.WINDOW_GAME.blit(self.white_ball, (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))
                    self.ball_images.append(self.white_ball)
                else:
                    self.WINDOW_GAME.blit(self.black_ball, (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))
                    self.ball_images.append(self.black_ball)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Kiểm tra sự kiện khi nút chuột được nhấn
                if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
                    if event.button == 1:  # Nút chuột trái
                        POWERING_UP = True
                        mouse_pressed = True
                # Kiểm tra sự kiện khi nút chuột được thả
                if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
                    POWERING_UP = False
                    key_down = True;

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.cue_ball.body.position = (
                            self.cue_ball.body.position[0] - 10, self.cue_ball.body.position[1])
                        key_down = False;
                    elif event.key == pygame.K_RIGHT:
                        self.cue_ball.body.position = (
                            self.cue_ball.body.position[0] + 10, self.cue_ball.body.position[1])
                        key_down = False;
            for ball in self.balls:
                if int(self.cue_ball.body.velocity[0]) != 0 or int(self.cue_ball.body.velocity[1]) != 0:
                    taking_shot = False
                if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                    taking_shot = False
            if taking_shot == True:
                # calculate cute angle
                mouse_pos = pygame.mouse.get_pos()
                self.cue.rect.center = self.cue_ball.body.position
                x_dist = -(self.cue_ball.body.position[0] - mouse_pos[0])
                y_dist = self.cue_ball.body.position[1] - mouse_pos[1]
                cue_angle = math.degrees(math.atan2(y_dist, x_dist))
                self.cue.update(cue_angle)
                self.cue.draw(self.WINDOW_GAME)

            # Tăng lực nếu nút chuột được nhấn và giữ
            if mouse_pressed and POWERING_UP == True:
                self.force += INCREASE_RATE * dt * FORCE_DIRECTION
                if self.force >= MAXFORCE or self.force <= 0:
                    FORCE_DIRECTION *= -1
            # Giảm lực nếu không có nút chuột nào được nhấn
            elif POWERING_UP == False and taking_shot == True:
                x_impulse = self.force * math.cos(math.radians(self.cue.angle))
                y_impulse = self.force * math.sin(math.radians(self.cue.angle))
                self.cue_ball.body.apply_impulse_at_local_point((x_impulse * 100, -(y_impulse * 100)), (0, 0))
                self.force = 0
                mouse_pressed = False

            #if self.is_moving() == False and key_down == True:
            #    self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 663)
            #    key_down == False
            print(self.cue_ball.body.position)
            self.space.debug_draw(self.draw_options)
            pygame.draw.rect(self.WINDOW_GAME, (50, 248, 8, 1), (350, 700, MAXFORCE * 5, 30))
            pygame.draw.rect(self.WINDOW_GAME, COLOR_BLACK, (350, 700, self.force * 5, 30))

            pygame.display.flip()

        pygame.quit()
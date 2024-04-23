from tkinter import font

import pygame
import sys
import pymunk
import pymunk.pygame_util
import define as df
from define import *
from cue import Cue
import math
from ai import *
from balls import *

class PlayGame:
    def __init__(self):
        pygame.init()
        self.window_color = COLOR_BACKGROUND
        self.WINDOW_GAME = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "board.png"), (BOARD_SIZE)).convert()
        # khai bao them
        self.space = pymunk.Space()
        self.static_body = self.space.static_body
        self.draw_options = pymunk.pygame_util.DrawOptions(self.WINDOW_GAME)
        pos = (self.WINDOW_GAME.get_width() // 2, 663)
        self.cue_ball = self.create_ball(38/2,pos)
        self.clock = pygame.time.Clock()
        self.balls = []
        self.ball_images = []
        self.mouse_pressed = False
        self.key_down = False
        self.force_direction = 1
        self.powering_up = True
        self.player_turn = True
        self.ai_turn = False
        self.player_ball = []
        self.ai_ball = []
        rows = 5
        dia = 38
        # for col in range(5):
        #     for row in range(rows):
        #         pos = (550 + (col * (dia + 1)), 330 + (row * (dia + 1)) + (col * dia / 2))
        #         new_ball = self.create_ball(dia/2, pos)
        #         self.balls.append(new_ball)
        #     rows -= 1
        pattern = [
            ['', '', '0', '', ''],
            ['', '0', '*', '*', ''],
            ['*', '0', 'Q', '0', '*'],
            ['', '*', '*', '0', ''],
            ['', '', '0', '', '']
        ]
        self.force = 0
        new_size = (int(self.cue_ball.radius * 2), int(self.cue_ball.radius * 2))
        self.ball_image = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "striker.png").convert_alpha(),new_size)
        self.white_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "white_new.png").convert_alpha(),new_size)
        self.black_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "black_new.png").convert_alpha(),new_size)
        self.queen = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "queen.png").convert_alpha(), new_size)
        # for i in range(0, 16):
        #     if i == 9:
        #         the_ball = self.queen
        #     elif i % 2 == 0:
        #         the_ball = self.black_ball
        #     else:
        #         the_ball = self.white_ball
        #     self.ball_images.append(the_ball)

        self.force = 0
        self.cue = Cue(self.cue_ball.body.position)
        self.potted = []
        self.potted_ball = []
        self.old_potted = []
        self.queen_ball = []
        self.playcount = 0
        self.to_remove = []
        self.ball_potted_in_turn = False
        # for i, ball in enumerate(self.balls):
        #     if i % 2 == 0:
        #         self.ai_ball.append(ball)
        #     else:
        #         self.player_ball.append(ball)
        for row in range(5):
            for col in range(5):

                pos = (BALL_POSITION[0] + (col * (DIA + 1)), BALL_POSITION[1] + (row * (DIA + 1)))

                if pattern[row][col] != '':
                    new_ball = self.create_ball(DIA/2, pos)
                    self.balls.append(new_ball)

                    if pattern[row][col] == '*':
                        self.ball_images.append(self.black_ball)
                        self.ai_ball.append(new_ball)
                    elif pattern[row][col] == '0':
                        self.ball_images.append(self.white_ball)
                        self.player_ball.append(new_ball)
                    else:
                        self.ball_images.append(self.queen)
                        self.queen_ball.append(new_ball)
                        self.player_ball.append(new_ball)
                        self.ai_ball.append(new_ball)

    def create_ball(self, radius, pos):
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
    def create_cushion(self, polydim):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = ((0, 0))
        shape = pymunk.Poly(body, polydim)
        shape.elasticity = 0.8
        self.space.add(body, shape)

    def is_moving(self):
        cue_ball_velocity = self.cue_ball.body.velocity
        balls_velocity = [ball.body.velocity for ball in self.balls]
        return cue_ball_velocity != (0, 0) or any(ball_velocity != (0, 0) for ball_velocity in balls_velocity)

    def are_balls_and_cue_ball_stopped(self):
        if int(self.cue_ball.body.velocity[0]) != 0 or int(self.cue_ball.body.velocity[1]) != 0:
            return False  # The cue ball is moving

        for ball in self.balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                return False  # At least one ball is moving

        return True
    def checkEvent(self, event, taking_shot):
        # Kiểm tra sự kiện khi nút chuột được nhấn
        if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
            if event.button == 1:  # Nút chuột trái
                self.powering_up = True
                self.mouse_pressed = True
        # Kiểm tra sự kiện khi nút chuột được thả
        if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
            self.powering_up = False
            self.key_down = True;
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_x = max(min(self.cue_ball.body.position[0] - 10, 1000), 380)
                self.cue_ball.body.position = (new_x, self.cue_ball.body.position[1])
                self.key_down = False
            elif event.key == pygame.K_RIGHT:
                new_x = max(min(self.cue_ball.body.position[0] + 10, 820), 380)
                self.cue_ball.body.position = (new_x, self.cue_ball.body.position[1])
                self.key_down = False
    def display_winner_message(self, message):
        """Display a winner message."""
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.WINDOW_GAME.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
    def change_turn(self):
        self.player_turn = not self.player_turn
        self.ai_turn = not self.ai_turn

    def start_game(self):
        running = True
        font = pygame.font.Font(None, 36)  # Choose a font and font size
        self.player_switch_timer = 8
        for c in CUSHION:
            self.create_cushion(c)
        while running:
            taking_shot = True

            self.space.step(1 / 60)
            dt = self.clock.tick(60) / 1000
            self.WINDOW_GAME.fill(self.window_color)
            self.WINDOW_GAME.blit(self.bg, BOARD_POSITION)
            self.WINDOW_GAME.blit(self.ball_image, (self.cue_ball.body.position[0] - self.cue_ball.radius,
                                                    self.cue_ball.body.position[1] - self.cue_ball.radius))
            if taking_shot and not self.is_moving():
                self.player_switch_timer -= dt
            self.player_switch_timer = max(self.player_switch_timer, 0)
            timer_text = font.render("Timer: " + str(int(self.player_switch_timer)), True, (255, 255, 255))
            self.WINDOW_GAME.blit(timer_text, (10, 10))  # Adjust position as needed
            if self.player_switch_timer <= 0:
                self.change_turn()
                self.player_switch_timer = 8

            for i, ball in enumerate(self.balls):
                for pocket in POCKETS:
                    ball_x_dist = abs(ball.body.position[0] - pocket[0])
                    ball_y_dist = abs(ball.body.position[1] - pocket[1])
                    ball_dist = math.sqrt(ball_x_dist ** 2 + ball_y_dist ** 2)
                    if ball_dist <= POCKET_DIA / 2:
                        if ball in self.ai_ball:
                            self.ai_ball.remove(ball)
                            self.player_turn = False
                            self.ai_turn = True
                            pygame.display.flip()
                        elif ball in self.player_ball:
                            if ball in self.player_ball:  # Check if the ball exists in the list before removing
                                self.player_ball.remove(ball)
                            if self.is_moving() == False:
                                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 663)
                            self.player_turn = True
                            self.ai_turn = False
                            self.key_down = True
                            pygame.display.flip()
                        self.potted.append(self.ball_images[i])
                        ball.collision_type = 1
                        handler = self.space.add_collision_handler(1, 0)  # 0 is the collision type of the other objects
                        handler.begin = lambda a, b, arbiter: False  # Modify this line
                        self.to_remove.append(ball)
                        self.space.remove(ball.body)
                        self.balls.remove(ball)
                        self.potted_ball.append(self.ball_images[i])
                        self.ball_images.pop(i)

            #gọi AI
            if self.is_moving() == False and self.key_down == True and self.ai_turn == False:
                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 140)
                ai(self, 80, 500, 0.3, 0.9, dt, 70, 70)
                self.key_down = False
                self.change_turn()
                self.player_switch_timer = 8

            if self.is_moving() == False and self.player_turn == False:
                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 663)
                self.key_down = False
                self.change_turn()
                self.player_switch_timer = 8

            for i, ball in enumerate(self.balls):
                self.WINDOW_GAME.blit(self.ball_images[i],(ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.checkEvent(event, taking_shot)

            for ball in self.balls:
                if self.are_balls_and_cue_ball_stopped() == False:
                    taking_shot = False

            if taking_shot == True and self.player_turn == True:
                # calculate cue angle
                mouse_pos = pygame.mouse.get_pos()
                self.cue.rect.center = self.cue_ball.body.position
                x_dist = -(self.cue_ball.body.position[0] - mouse_pos[0])
                y_dist = self.cue_ball.body.position[1] - mouse_pos[1]
                cue_angle = math.degrees(math.atan2(y_dist, x_dist))
                self.cue.update(cue_angle)
                self.cue.draw(self.WINDOW_GAME)

                # Tăng lực nếu nút chuột được nhấn và giữ
            if self.mouse_pressed and self.powering_up == True:
                self.force += INCREASE_RATE * dt * self.force_direction
                if self.force >= MAXFORCE or self.force <= 0:
                    self.force_direction *= -1
                # Giảm lực nếu không có nút chuột nào được nhấn
            elif self.powering_up == False and taking_shot == True:
                x_impulse = self.force * math.cos(math.radians(self.cue.angle))
                y_impulse = self.force * math.sin(math.radians(self.cue.angle))
                self.cue_ball.body.apply_impulse_at_local_point((x_impulse * 100, -(y_impulse * 100)), (0, 0))
                self.force = 0
                mouse_pressed = False

            for obj in self.to_remove:
                if obj.body in self.space.bodies:  # Check if the body is in the space
                    self.space.remove(obj.body)
                    self.balls.remove(obj)
                    self.potted_ball.append(self.ball_images[self.balls.index(obj)])
                    self.ball_images.pop(self.balls.index(obj))
            self.to_remove.clear()

            # print(self.cue_ball.body.position)
            # self.space.debug_draw(self.draw_options)
            pygame.draw.rect(self.WINDOW_GAME, (50, 248, 8, 1), (350, 700, MAXFORCE * 5, 30))
            pygame.draw.rect(self.WINDOW_GAME, COLOR_BLACK, (350, 700, self.force * 5, 30))

            pygame.display.flip()

        pygame.quit()

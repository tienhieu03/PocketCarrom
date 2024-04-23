import pygame
import sys
import pymunk
import pymunk.pygame_util
import math


from define import *
from cue import Cue
from ai import *
from balls import *
from pvp.player import *
from pvp.score import *


class PVPGame:
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
        self.striker_balls = []
        self.mouse_pressed = False
        self.key_down = False
        self.force_direction = 1
        self.powering_up = True
        self.player1 = True
        self.player2 = False
        self.black_list = []
        self.white_list= []
        self.ball_images = []
        self.to_remove = []


        new_size = (int(self.cue_ball.radius * 2), int(self.cue_ball.radius * 2))
        self.striker_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "striker.png"),(BALL_SIZE)).convert_alpha()
        self.white_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "white_new.png"),(WHITE_BALL_SIZE)).convert_alpha()
        self.black_ball = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "black_new.png"),(BLACK_BALL_SIZE)).convert_alpha()
        self.queen = pygame.transform.scale(pygame.image.load(PATH_IMAGE + "queen.png"), (BALL_SIZE)).convert_alpha()
        #self.playert1 = Player("player1", self.striker_ball, self.WINDOW_GAME, self.black_list)
        #self.playert2 = Player("player2", self.striker_ball, self.WINDOW_GAME, self.white_list)
        self.white_list.append(self.white_ball)
        self.black_list.append(self.black_ball)

        self.player1_ball_type = "white"
        self.player2_ball_type = "black"

        self.queen_potted = False
        # Define the pattern based on the shape file
        pattern = [
            ['', '', '0', '', ''],
            ['', '0', '*', '*', ''],
            ['*', '0', 'Q', '0', '*'],
            ['', '*', '*', '0', ''],
            ['', '', '0', '', '']
        ]

        for row in range(5):
            for col in range(5):

                pos = (BALL_POSITION[0] + (col * (DIA + 1)), BALL_POSITION[1] + (row * (DIA + 1)))

                if pattern[row][col] != '':
                    new_ball = self.create_ball(DIA/2, pos)
                    self.balls.append(new_ball)

                    if pattern[row][col] == '*':
                        self.striker_balls.append(self.black_ball)
                        self.black_list.append(new_ball)
                    elif pattern[row][col] == '0':
                        self.striker_balls.append(self.white_ball)
                        self.white_list.append(new_ball)
                    else:
                        self.striker_balls.append(self.queen)

        self.force = 0

        for i in range(0, 16):
            if i == 9:
                the_ball = self.queen
            elif i % 2 == 0:
                the_ball = self.black_ball
            else:
                the_ball = self.white_ball
            self.striker_balls.append(the_ball)
        self.cue = Cue(self.cue_ball.body.position)
        self.potted_ball = []
        self.old_potted = []
        self.black_ball_potted = False
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
    def are_balls_and_cue_ball_stopped(self):
        if int(self.cue_ball.body.velocity[0]) != 0 or int(self.cue_ball.body.velocity[1]) != 0:
            return False  # The cue ball is moving

        for ball in self.balls:
            if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0:
                return False  # At least one ball is moving

        return True
    def is_moving(self):
        cue_ball_velocity = self.cue_ball.body.velocity
        balls_velocity = [ball.body.velocity for ball in self.balls]
        return cue_ball_velocity != (0, 0) or any(ball_velocity != (0, 0) for ball_velocity in balls_velocity)


    def checkEvent(self, event, taking_shot):
        # Check if the balls are moving
        if not self.are_balls_and_cue_ball_stopped():
            return

        # Check the event when the mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN and taking_shot == True:
            if event.button == 1:  # Left mouse button
                self.powering_up = True
                self.mouse_pressed = True

        # Check the event when the mouse button is released
        if event.type == pygame.MOUSEBUTTONUP and taking_shot == True:
            self.powering_up = False
            self.key_down = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_x = max(min(self.cue_ball.body.position[0] - 10, 1000), 380)
                self.cue_ball.body.position = (new_x, self.cue_ball.body.position[1])
                self.key_down = False
            elif event.key == pygame.K_RIGHT:
                new_x = max(min(self.cue_ball.body.position[0] + 10, 820), 380)
                self.cue_ball.body.position = (new_x, self.cue_ball.body.position[1])
                self.key_down = False

    def switch_players(self):
        if self.player1 == True:
            self.player1 = False
            self.player2 = True
            self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 140)
        elif self.player2 == True:
            self.player2 = False
            self.player1 = True
            self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 663)

    def check_potted_ball(self, ball):
        if ball == self.queen:
            if len(self.white_list) == 1 or len(self.black_list) == 1:
                # Một trong hai bên không còn viên của mình, viên queen có thể bị bắn xuống lỗ
                self.queen_potted = True
            else:
                # Cả hai bên vẫn còn viên của mình, viên queen sẽ được đưa lại giữa bàn
                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 663)
                self.balls.append(self.queen)
                self.striker_balls.append(self.queen)

        elif ball in self.black_list:
            if self.player1_ball_type == "black":
                pass
            else:
                self.switch_players()
        elif ball in self.white_list:
            if self.player1_ball_type == "white":
                pass
            else:
                self.switch_players()
        elif ball == self.queen:
            pass

    def start_game(self):
        running = True
        font = pygame.font.Font(None, 36)  # Choose a font and font size
        self.player_switch_timer = 8  # Timer in seconds (adjust as needed)
        for c in CUSHION:
            self.create_cushion(c)
        while running:
            taking_shot = True
            self.space.step(1 / 60)
            dt = self.clock.tick(60) / 1000
            self.WINDOW_GAME.fill(self.window_color)
            self.WINDOW_GAME.blit(self.bg, BOARD_POSITION)
            self.WINDOW_GAME.blit(self.striker_ball, (self.cue_ball.body.position[0] - self.cue_ball.radius,
                                                      self.cue_ball.body.position[1] - self.cue_ball.radius))

            if taking_shot and not self.is_moving():
                self.player_switch_timer -= dt
            self.player_switch_timer = max(self.player_switch_timer, 0)
            timer_text = font.render("Timer: " + str(int(self.player_switch_timer)), True, (255, 255, 255))
            self.WINDOW_GAME.blit(timer_text, (10, 10))  # Adjust position as needed
            if self.player_switch_timer <= 0:
                self.switch_players()
                self.player_switch_timer = 8


            # Kiểm tra xem tất cả các viên bi và bi striker có đang di chuyển hay không
            # if self.are_balls_and_cue_ball_stopped() and not self.is_moving():
            #     # Thay đổi lượt người chơi sau khi bắn và tất cả các viên bi đã dừng lại
            #     self.player1, self.player2 = self.player2, self.player1

            player_text = font.render("Black's Turn", True, COLOR_WHITE) if self.player1 else font.render("White's Turn", True, COLOR_WHITE)
            self.WINDOW_GAME.blit(player_text, (10, 50))
            for i, ball in enumerate(self.balls):
                for pocket in POCKETS:
                    ball_x_dist = abs(ball.body.position[0] - pocket[0])
                    ball_y_dist = abs(ball.body.position[1] - pocket[1])
                    ball_dist = math.sqrt(ball_x_dist ** 2 + ball_y_dist ** 2)
                    if ball_dist <= POCKET_DIA / 2:
                        self.check_potted_ball(ball)
                        if ball in self.black_list:
                            self.black_list.remove(ball)
                            print("Black ball pocketed")
                            self.player1 = False
                            self.player2 = True
                            pygame.display.flip()
                        elif ball in self.white_list:
                            self.white_list.remove(ball)
                            print("White ball pocketed")
                            self.player1 = True
                            self.player2 = False
                            pygame.display.flip()
                        ball.collision_type = 1
                        handler = self.space.add_collision_handler(1, 0)  # 0 is the collision type of the other objects
                        handler.begin = lambda a, b, arbiter: False  # Modify this line
                        self.to_remove.append(ball)
                        self.space.remove(ball.body)
                        self.balls.remove(ball)
                        self.potted_ball.append(self.striker_balls[i])
                        self.striker_balls.pop(i)
            if self.queen_potted:
                if len(self.white_list) == 0:
                    print("White wins!")
                elif len(self.black_list) == 0:
                    print("Black wins!")
                self.queen_potted = False

            # print(self.potted_ball)

            if self.is_moving() == False and self.key_down == True and self.player2 == False:
                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 140)
                self.key_down = False
                self.switch_players()
                self.player_switch_timer = 8

            if self.is_moving() == False and self.key_down == True and self.player1 == False:
                self.cue_ball.body.position = (self.WINDOW_GAME.get_width() // 2, 663)
                self.key_down = False
                self.switch_players()
                self.player_switch_timer = 8

            for i, ball in enumerate(self.balls):
                self.WINDOW_GAME.blit(self.striker_balls[i],(ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.checkEvent(event, taking_shot)

            for ball in self.balls:
                if self.are_balls_and_cue_ball_stopped() == False:
                    taking_shot = False

            if taking_shot == True:
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
                    self.potted_ball.append(self.striker_balls[self.balls.index(obj)])
                    self.striker_balls.pop(self.balls.index(obj))
            self.to_remove.clear()

            #print(self.cue_ball.body.position)
            #self.space.debug_draw(self.draw_options)
            # if len(self.potted_ball) <= len(self.old_potted) and len(self.potted_ball) > 0:
            #     if self.player1 == True:
            #         self.player1 = False
            #         self.player2 = True
            #     elif self.player2 == True:
            #         self.player1 = True
            #         self.player2 = False
            # elif len(self.potted_ball) > len(self.old_potted):
            #     self.old_potted = self.potted_ball.copy()



            if len(self.black_list) == 0:
                pass
            elif len(self.white_list) == 0:
                pass

            pygame.draw.rect(self.WINDOW_GAME, COLOR_DARK_BROWN, (*POWER_BAR_POSITION, *POWER_BAR_SIZE))
            pygame.draw.rect(self.WINDOW_GAME, COLOR_WHITE, (
            POWER_BAR_POSITION[0], POWER_BAR_POSITION[1] + POWER_BAR_SIZE[1] - self.force * 5, POWER_BAR_SIZE[0],
            self.force * 5))
            pygame.display.flip()
        pygame.quit()
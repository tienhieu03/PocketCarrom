import math

import pymunk
from numpy.lib.user_array import container
from pygame import Vector2
from define import *
def ___(angle_):
    """ This function is used to normalize angles """
    angle_ = angle_ % 360
    return angle_ if angle_ <= 180 else angle_ - 360
def straight_shot_speed(play_game, striker_position: Vector2, coin_position: Vector2,
                        pocket_center: Vector2, decelerate, e):
    from play_game import PlayGame
    assert isinstance(play_game, PlayGame)
    distance_coin_pocket = pocket_center.distance_to(coin_position)
    distance_striker_coin = striker_position.distance_to(coin_position)
    col_coin_speed = math.sqrt(2 * distance_coin_pocket * decelerate)
    col_striker_speed = col_coin_speed * (5.5 + 15) / ((1 + e) * 15)
    striker_speed = math.sqrt(col_striker_speed ** 2 + 2 * decelerate * distance_striker_coin)
    return striker_speed
def check_along_path(start, end, distance, coins, round_start=False, round_end=False):
    """ This function checks if any of the coins lies within the given distance, of the line joining
    the given two vectors, representing the end points """
    for coin in coins:
        diff_vector = end - start
        section = (coin.body.position - start).dot(diff_vector) / (diff_vector.x ** 2 + diff_vector.y ** 2)
        """ Whether to round or not """
        section = section if not round_start else max(0, section)
        section = section if not round_end else min(1, section)
        if 0 <= section <= 1:
            projection = start + section * (end - start)
            diff_vector = coin.body.position - projection
            distance_to_coin = math.sqrt(diff_vector.x ** 2 + diff_vector.y ** 2)
            if distance_to_coin <= distance:
                """ Coin lies within the distance of the vector """
                return True
    return False



def ai(play_game, max_angle, max_speed, decelerate, e, dt, max_cut_shot_angle=70, max_rebound_cut_shot_angle=70):
    """ Carrom Ai which knows to play direct shots, rebound shots and cuts """
    from play_game import PlayGame
    assert isinstance(play_game, PlayGame), "play_game must be an instance of PlayGame class"
    #player, opponent = play_game.player, (play_game.playcount + 1) % 2
    """ Coins on the board and the coins which player can hit """
    board_coins = play_game.balls
    ai_coin = play_game.ai_ball
    #if not play_game.pocketed_queen:
    #    board_coins.append(play_game.queen)
    direction_vec = Vector2(0, -1) if play_game.playcount == 0 else Vector2(0, 1)
    x_limits = (380,820)
    y_position = 140
    coin_radius, striker_radius = play_game.cue_ball.radius, play_game.cue_ball.radius
    #board, container = play_game.board, play_game.board.container
    pocket_radius = POCKET_DIA / 2
    pocket_centers = POCKETS
    if not play_game.are_balls_and_cue_ball_stopped():
        return
    """ Simply hit straight at some coin """
    for coin in play_game.ai_ball:
        for striker_x in range(int(x_limits[0]), int(x_limits[1] + 1), 1):
            striker_position = play_game.cue_ball.body.position
            dx = coin.body.position[0] - striker_position[0]
            dy = coin.body.position[1] - striker_position[1]
            angle_of_attack = math.degrees(math.atan2(dy, dx))
            attack_vector = coin.body.position - striker_position
            collision_position = striker_position + attack_vector.normalized() * (
                        attack_vector.length - coin_radius - striker_radius)
            """ Simply hit the coins with max speed """
            play_game.cue_ball.body.position = tuple(striker_position)
            striker_angle = -90 - angle_of_attack if play_game.playcount == 0 else 90 - angle_of_attack

            r, theta = max_speed, striker_angle
            # Set the velocity
            #play_game.cue_ball.body.velocity = pymunk.Vec2d(dx, dy) * 2
            play_game.cue_ball.body.apply_impulse_at_local_point((dx * 20, dy * 20), (0, 0))

            print("AI does a simply direct hit with angle:",
                  "%0.2f" % angle_of_attack, "degrees 20")
            pygame.time.wait(4)
            return
        """ If nothing can be hit either way don't worry about the fouls try hitting the coin """
        """ Simply hit straight at some coin """
        for coin in play_game.ai_ball:
            for striker_x in range(int(x_limits[0]), int(x_limits[1] + 1), 1):
                striker_position = Vector2(striker_x, y_position)
                dx = coin.body.position[0] - striker_position[0]
                dy = coin.body.position[1] - striker_position[1]
                angle_of_attack = math.degrees(pymunk.Vec2d(dx, dy).get_angle_between(direction_vec))
                attack_vector = coin.body.position - striker_position
                if abs(angle_of_attack) <= max_angle:
                    """ Simply hit the coins with max speed """
                    play_game.cue_ball.body.position = tuple(striker_position)
                    striker_angle = -90 - angle_of_attack if play_game.playcount == 0 else 90 - angle_of_attack
                    theta_radians = math.radians(striker_angle)
                    dx = max_speed * math.cos(theta_radians)
                    dy = max_speed * math.sin(theta_radians)
                    play_game.cue_ball.body.velocity = pymunk.Vec2d(dx, dy) * 2
                    print("AI does a simply direct hit with angle:",
                          "%0.2f" % angle_of_attack, "degrees", "may face penalty 10")
                    return


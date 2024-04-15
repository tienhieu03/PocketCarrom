import pygame
import math
import heapq
import pymunk

from play_game import *
import play_game as pg
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

class AI():
    cue_image = pygame.image.load("assets/game/circles2.png")

    def __init__(self, position, ball_image, balls):
        self.space = pymunk.Space()
        self.static_body = self.space.static_body
        self.cue = self.create_ball(38 / 2, position)
        self.striker = ball_image
        self.position = position
        self.balls = balls
        self.pocket_centers = [(265, 61), (941, 58), (942, 736), (266, 729)]
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
    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def calculate_best_shot(self):
        start = (self.cue.x, self.cue.y)
        goal = self.pocket_centers[0]  # Assume the goal is the first pocket for simplicity
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.game.neighbors(current):
                new_cost = cost_so_far[current] + self.game.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far

    def execute_shot(self):
        came_from, cost_so_far = self.calculate_best_shot()
        # Find the path from the cue ball to the pocket
        current = self.pocket_centers[0]
        path = []
        while current != (self.cue.x, self.cue.y):
            path.append(current)
            current = came_from[current]
        path.append((self.cue.x, self.cue.y))
        path.reverse()
        # Apply an impulse to the cue ball in the direction of the first step of the path
        next_step = path[1]
        dx = next_step[0] - self.cue.x
        dy = next_step[1] - self.cue.y
        angle = math.atan2(dy, dx)
        self.cue.apply_impulse_at_local_point((math.cos(angle) * 100, math.sin(angle) * 100), (0, 0))
import math
import pygame
import random

SCREEN_DIM = (800, 600)

class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        return Vec2d(self.x * k, self.y * k)

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2))

    def int_pair(self):
        return int(self.x), int(self.y)

    def __repr__(self):
        return f"Vec2d({self.x}, {self.y})"


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self, screen_dim):
        for i in range(len(self.points)):
            self.points[i] = self.points[i] + self.speeds[i]
            if self.points[i].x > screen_dim[0] or self.points[i].x < 0:
                self.speeds[i] = Vec2d(-self.speeds[i].x, self.speeds[i].y)
            if self.points[i].y > screen_dim[1] or self.points[i].y < 0:
                self.speeds[i] = Vec2d(self.speeds[i].x, -self.speeds[i].y)

    def draw_points(self, game_display, style="line", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(game_display, color,
                                 self.points[p_n].int_pair(),
                                 self.points[p_n + 1].int_pair(), width)
        elif style == "points":
            for point in self.points:
                pygame.draw.circle(game_display, color,
                                   point.int_pair(), width)


class Knot(Polyline):
    def __init__(self, steps=100):
        super().__init__()
        self.steps = steps
        self.smooth_points = []

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.smooth_points = self.get_knot()

    def set_points(self, screen_dim):
        super().set_points(screen_dim)
        self.smooth_points = self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        return [self.get_point(base_points, i * alpha) for i in range(count)]

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, self.steps))
        return res

    def draw_points(self, game_display, style="line", width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(self.smooth_points) - 1):
                pygame.draw.line(game_display, color,
                                 self.smooth_points[p_n].int_pair(),
                                 self.smooth_points[p_n + 1].int_pair(), width)
        elif style == "points":
            super().draw_points(game_display, style, width, color)


class Game:
    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode(SCREEN_DIM)
        pygame.display.set_caption("MyScreenSaver")
        self.steps = 100
        self.working = True
        self.knot = Knot(steps=self.steps)
        self.show_help = False
        self.pause = True
        self.hue = 0
        self.color = pygame.Color(0)

    def draw_help(self):
        self.game_display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = [
            ["F1", "Show Help"],
            ["R", "Restart"],
            ["P", "Pause/Play"],
            ["Num+", "More points"],
            ["Num-", "Less points"],
            ["", ""],
            [str(self.steps), "Current points"]
        ]
        pygame.draw.lines(self.game_display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.game_display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.game_display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def run(self):
        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.knot = Knot(steps=self.steps)
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                        self.knot.steps = self.steps
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0
                        self.knot.steps = self.steps

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.knot.add_point(Vec2d(*event.pos), Vec2d(random.random() * 2, random.random() * 2))

            self.game_display.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            self.knot.draw_points(self.game_display, style="line", width=3, color=self.color)
            self.knot.draw_points(self.game_display, style="points", width=3, color=(255, 255, 255))
            if not self.pause:
                self.knot.set_points(SCREEN_DIM)
            if self.show_help:
                self.draw_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()


# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()

import random
import sys
import time

import pygame

import config


class Game:
    def __init__(self):
        self.width = 720
        self.height = 460
        self.fps = 20

        # Set window surface
        self.playing_surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake (by Dumanski)')

        # Clock
        self.clock = pygame.time.Clock()

        # Result
        self.score = 0

        # Init pygame
        pygame.init()

    @staticmethod
    def event_tracking(direction_to_change: str) -> str:
        """Tracking of the player's keystrokes and returns direction"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction_to_change = 'UP'
                if event.key == pygame.K_DOWN:
                    direction_to_change = 'DOWN'
                if event.key == pygame.K_LEFT:
                    direction_to_change = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    direction_to_change = 'RIGHT'

                # Shortcut to Quit
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return direction_to_change

    def refresh_screen(self):
        """Refresh screen and set FPS"""
        pygame.display.flip()
        self.clock.tick(self.fps)

    def show_score(self, choice: int = 1) -> None:
        """Shows the score"""
        score_font = pygame.font.SysFont('Arial', 24)
        score_surface = score_font.render(f'Score: {self.score}', True, config.BLACK)
        score_rect = score_surface.get_rect()

        if choice == 1:
            score_rect.midtop = (80, 10)
        else:
            score_rect.midtop = (360, 250)
        self.playing_surface.blit(score_surface, score_rect)

    def game_over(self) -> None:
        """Displays "Game Over, Score" and ends the game"""
        game_over_font = pygame.font.SysFont('Arial', 80)
        game_over_surface = game_over_font.render("Game Over", True, config.RED, config.BACKGROUND)
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (360, 150)
        self.playing_surface.blit(game_over_surface, game_over_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


class Snake:
    def __init__(self):
        self.snake_head_position = [200, 100]
        self.snake_body = [[200, 100], [190, 100], [180, 100]]
        self.snake_color = config.GREEN
        self.snake_direction = 'RIGHT'
        self.direction_to_change = self.snake_direction

    def check_change_direction(self) -> None:
        """Check and change the direction of movement only if it is
        not opposite to the current one"""
        if any((self.direction_to_change == "RIGHT" and not self.snake_direction == "LEFT",
                self.direction_to_change == "LEFT" and not self.snake_direction == "RIGHT",
                self.direction_to_change == "UP" and not self.snake_direction == "DOWN",
                self.direction_to_change == "DOWN" and not self.snake_direction == "UP")):
            self.snake_direction = self.direction_to_change

    def change_head_position(self) -> None:
        """Change snake's head position"""
        if self.snake_direction == 'RIGHT':
            self.snake_head_position[0] += 10
        if self.snake_direction == 'LEFT':
            self.snake_head_position[0] -= 10
        if self.snake_direction == 'UP':
            self.snake_head_position[1] -= 10
        if self.snake_direction == 'DOWN':
            self.snake_head_position[1] += 10

    def snake_body_mechanics(self, score: int, food_position: list, width, height) -> (int, list):
        self.snake_body.insert(0, list(self.snake_head_position))
        if self.snake_head_position[0] == food_position[0] and self.snake_head_position[1] == food_position[1]:
            food_position = [random.randrange(1, width / 10) * 10,
                             random.randrange(1, height / 10) * 10]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_position

    def draw_snake(self, playing_surface, surface_color) -> None:
        """Draws a snake based on body coordinates"""
        playing_surface.fill(surface_color)
        for position in self.snake_body:
            pygame.draw.rect(playing_surface, self.snake_color,
                             pygame.Rect(position[0], position[1], 10, 10))

    def collision_check(self, game_over, width, height) -> None:
        """Checks if the snake collided with a wall or with its own body"""
        if any((
                self.snake_head_position[0] > width - 10
                or self.snake_head_position[0] < 0,
                self.snake_head_position[1] > height - 10
                or self.snake_head_position[1] < 0
        )):
            game_over()

        for element in self.snake_body[1:]:
            if (element[0] == self.snake_head_position[0] and
                    element[1] == self.snake_head_position[1]):
                game_over()


class Food:
    def __init__(self, width, height):
        self.food_color = config.BLUE
        self.food_size = 10
        self.food_position = [random.randrange(1, width / 10) * 10,
                              random.randrange(1, height / 10) * 10]

    def draw_food(self, playing_surface) -> None:
        """Draws food on the playing field"""
        pygame.draw.rect(
            playing_surface, self.food_color, pygame.Rect(
                self.food_position[0], self.food_position[1],
                self.food_size, self.food_size)
        )


if __name__ == '__main__':

    game = Game()
    snake = Snake()
    food = Food(game.width, game.height)

    while True:
        snake.direction_to_change = game.event_tracking(snake.direction_to_change)

        snake.check_change_direction()
        snake.change_head_position()

        game.score, food.food_position = snake.snake_body_mechanics(
            game.score, food.food_position, game.width, game.height)

        snake.draw_snake(game.playing_surface, config.BACKGROUND)

        food.draw_food(game.playing_surface)

        snake.collision_check(
            game.game_over, game.width, game.height)

        game.show_score()
        game.refresh_screen()

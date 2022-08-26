import pygame


class Game:
    def __init__(self):
        self.width = 500
        self.height = 400
        self.fps = 60

        # Clock
        self.clock = pygame.time.Clock()

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.FRAME_COLOR = (0, 255, 204)

        # Result
        self.score = 0

        # Init pygame and check for errors
        self.init_and_check_errors()

    def init_and_check_errors(self) -> None:
        """Init pygame and check for errors"""
        self.check_errors = pygame.init()
        if self.check_errors[1] > 0:
            pygame.quit()

    def set_surface_and_title(self) -> None:
        """Set width/height for screen and set window title"""
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake (by Dumanski)')

    def event_tracking(self, direction: str) -> str:
        """Tracking of the player's keystrokes and returns direction"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                if event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                if event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'

                # Shortcut to Quit
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        return direction

    def refresh_screen(self):
        """Refresh screen and set FPS"""
        pygame.display.flip()
        self.clock.tick(self.fps)

    def show_score(self, choice=1):
        score_font = pygame.font.SysFont('Arial', 24)
        # TODO: change upper line when download necessary font: score.font = pygame.font.Font('/where/font.ttf', size)
        score_surface = score_font.render(
            f'Score: {self.score}',
            True,
            self.BLACK
        )
        score_rect = score_surface.get_rect()

        if choice == 1:
            score_rect.midtop = (80, 10)
        else:
            score_rect.midtop = (360, 120)
        self.screen.blit(score_surface, score_rect)

    def game_over(self):
        """Displays "Game Over, Score" and ends the game"""
        game_over_font = pygame.font.SysFont('Arial', 72)
        game_over_surface = game_over_font.render(
            "Game Over",
            True,
            self.RED
        )
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (360, 15)
        self.screen.blit(game_over_surface, game_over_rect)
        self.show_score(0)
        pygame.display.flip()
        pygame.quit()






game = Game()
game.init_and_check_errors()
game.set_surface_and_title()

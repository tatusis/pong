# menu.py

from scene import Scene
import pygame


SCREEN_COLOR = pygame.color.THECOLORS["grey0"]
FONT_FAMILY = "resources/Minisystem.otf"
TITLE_FONT_SIZE = 100
OPTION_FONT_SIZE = 35
TEXT_COLOR = pygame.color.THECOLORS["grey50"]
BACKGROUND_MUSIC = "resources/background.mp3"


class Menu:
    """Define o menu"""

    def __init__(self, screen: pygame.surface.Surface) -> None:
        """Inicializa o menu"""
        self.scene_name = Scene.MENU
        self.next_scene_name = Scene.MENU
        self.screen = screen

        # Sound
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        # Título
        self.title_font = pygame.font.Font(FONT_FAMILY, TITLE_FONT_SIZE)
        self.title_text = self.render_text("PONG", self.title_font)

        # Opções
        self.option_font = pygame.font.Font(FONT_FAMILY, OPTION_FONT_SIZE)
        self.option_start_text = self.render_text("Press [ ENTER ] to play", self.option_font)
        self.option_exit_text = self.render_text("Press [ ESC ] to exit", self.option_font)

        self.running = True

    def process_events(self) -> None:
        """Processa os eventos do menu"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    self.next_scene_name = Scene.GAME
            elif event.type == pygame.QUIT:
                self.running = False

    def process_logic(self, dt: float) -> None:
        """Processa a lógica do menu"""
        pass

    def process_frames(self) -> None:
        """Processa os frames do menu"""
        self.screen.fill(SCREEN_COLOR)

        # Título
        title_text_rect = self.title_text.get_rect()
        title_text_rect.centerx = self.screen.get_rect().centerx
        title_text_rect.centery = round(self.screen.get_rect().bottom * (3 / 10))
        self.screen.blit(self.title_text, title_text_rect)

        # Opções
        option_start_text_rect = self.option_start_text.get_rect()
        option_start_text_rect.centerx = self.screen.get_rect().centerx
        option_start_text_rect.centery = round(self.screen.get_rect().bottom * (6 / 10))
        self.screen.blit(self.option_start_text, option_start_text_rect)

        option_exit_text_rect = self.option_exit_text.get_rect()
        option_exit_text_rect.centerx = self.screen.get_rect().centerx
        option_exit_text_rect.centery = round(self.screen.get_rect().bottom * (7 / 10))
        self.screen.blit(self.option_exit_text, option_exit_text_rect)

        pygame.display.flip()

    def render_text(self, text: str, font: pygame.font.Font) -> pygame.surface.Surface:
        """Rederiza o texto"""
        return font.render(text, True, TEXT_COLOR)

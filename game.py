import pygame
import pygame_gui

from grid import Grid

pygame.init()
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
UI_HEIGHT = 100

GAME_HEIGHT = WINDOW_HEIGHT - UI_HEIGHT

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

GAME_BACKGROUND_COLOR = '#000000'
UI_BACKGROUND_COLOR = '#000000'

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

game_background = pygame.Surface((WINDOW_WIDTH, GAME_HEIGHT))
game_background.fill(pygame.Color(GAME_BACKGROUND_COLOR))


ui_background = pygame.Surface((WINDOW_WIDTH, UI_HEIGHT))
ui_background.fill(pygame.Color(UI_BACKGROUND_COLOR))

manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((70, GAME_HEIGHT + 30), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                            text='Start',
                                            manager=manager)

reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((2*70 + BUTTON_WIDTH, GAME_HEIGHT + 30), (BUTTON_WIDTH, BUTTON_HEIGHT)),
                                            text='Reset',
                                            manager=manager)

g = Grid((WINDOW_WIDTH, GAME_HEIGHT), window_surface, 15, 15)
g.flip(2, 1)
g.flip(3, 2)
g.flip(1, 3)
g.flip(2, 3)
g.flip(3, 3)

clock = pygame.time.Clock()
is_running = True
game_on = False

while is_running:
    time_delta = clock.tick(5) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    game_on = not game_on

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(game_background, (0, 0))
    window_surface.blit(ui_background, (0, GAME_HEIGHT))
    manager.draw_ui(window_surface)

    if game_on:
        g.compute_future_states()
        g.update()

    g.draw(window_surface)
    pygame.display.update()

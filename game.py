import pygame
import pygame_gui

from grid import Grid

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UI_SURFACE_HEIGHT = 100

GAME_BACKGROUND_COLOR = '#0F0F00'
UI_BACKGROUND_COLOR = '#FFFFFF'

BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_Y_COORD = SCREEN_HEIGHT - UI_SURFACE_HEIGHT + BUTTON_HEIGHT / 2


pygame.init()

pygame.display.set_caption("Conway's Game of Life")
window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - UI_SURFACE_HEIGHT))
game_background.fill(pygame.Color(UI_BACKGROUND_COLOR))


def initial_grid_state():
    new_grid = Grid((SCREEN_WIDTH, SCREEN_HEIGHT - UI_SURFACE_HEIGHT), 15, 15)
    return new_grid


g = initial_grid_state()
g.flip(2, 1)
g.flip(3, 2)
g.flip(1, 3)
g.flip(2, 3)
g.flip(3, 3)

ui_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
ui_background.fill(pygame.Color(GAME_BACKGROUND_COLOR))

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((BUTTON_WIDTH/2, BUTTON_Y_COORD), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    text='Start',
    manager=manager)

reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((BUTTON_WIDTH*2, BUTTON_Y_COORD), (BUTTON_WIDTH, BUTTON_HEIGHT)),
    text='Reset',
    manager=manager)

clock = pygame.time.Clock()

game_state = {'is_running': True, 'animation_running': False, 'grid': g}
while game_state['is_running']:
    current_grid = game_state['grid']
    time_delta = clock.tick(5) / 1000.0
    for event in pygame.event.get():
        # pass the event and the game state to the controller
        # controller figures out what kind of event to address
        # updates the game state accordingly
        if event.type == pygame.QUIT:
            game_state['is_running'] = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == reset_button:
                    current_grid = initial_grid_state()
                if event.ui_element == start_button:
                    game_state['animation_running'] = not game_state['animation_running']
                    start_button.set_text('Pause') if game_state['animation_running'] else start_button.set_text('Start')

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            current_grid.check_clicks(pos)

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(game_background, (0, 0))
    window_surface.blit(ui_background, (0, SCREEN_HEIGHT-UI_SURFACE_HEIGHT))
    manager.draw_ui(window_surface)

    if game_state['animation_running']:
        current_grid.compute_future_states()
        current_grid.update()

    current_grid.draw(window_surface)
    pygame.display.update()



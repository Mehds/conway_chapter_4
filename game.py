import pygame
import pygame_gui

from grid import Grid

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1000, 750))

game_background = pygame.Surface((1000, 550))
game_background.fill(pygame.Color('#0F0F00'))

g = Grid((1000, 550), window_surface, 15, 15)
g.flip(2, 1)
g.flip(3, 2)
g.flip(1, 3)
g.flip(2, 3)
g.flip(3, 3)

ui_background = pygame.Surface((1000, 200))
ui_background.fill(pygame.Color('#FFFFFF'))

manager = pygame_gui.UIManager((1000, 750))

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 600), (100, 50)),
                                            text='Start',
                                            manager=manager)

reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 600), (100, 50)),
                                            text='Reset',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True
game_on = True

while is_running:
    time_delta = clock.tick(5) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                pass

        manager.process_events(event)

    manager.update(time_delta)

    # window_surface.blit(game_background, (0, 0))
    window_surface.blit(ui_background, (0, 550))
    manager.draw_ui(window_surface)

    if game_on:
        g.compute_future_states()
        g.update()

    g.draw(window_surface)
    pygame.display.update()

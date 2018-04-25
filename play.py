class Colour(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Direction(object):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


if __name__ == "__main__":
    import pygame

    display_width = 800
    display_height = 600

    pygame.init()

    GAME_DISPLAY = pygame.display

    SURFACE = GAME_DISPLAY.set_mode((display_width, display_height))
    GAME_DISPLAY.set_caption("Hack'n'Slash")
    clock = pygame.time.Clock()

    CHARACTER_IDLE = pygame.transform.smoothscale(pygame.image.load("character_idle.png"),
                                                  (int(display_width * 0.2), int(display_height * 0.2)))

    CHARACTER_RECT = CHARACTER_IDLE.get_rect()

    CHARACTER_RECT.x = display_width * 0.5
    CHARACTER_RECT.y = display_height * 0.5


    def character_idle_position(rectangle):
        SURFACE.blit(CHARACTER_IDLE, rectangle)


    player_quit = False
    x_change = 0
    y_change = 0
    player_direction = Direction.RIGHT
    while not player_quit:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                player_quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    player_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                    player_direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    y_change = -5
                    player_direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                    player_direction = Direction.DOWN

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        CHARACTER_RECT.x += x_change if -CHARACTER_RECT.width / 2 < int(
            CHARACTER_RECT.x + x_change) <= display_width - CHARACTER_RECT.width / 2 else 0
        CHARACTER_RECT.y += y_change if -CHARACTER_RECT.height / 2 < int(
            CHARACTER_RECT.y + y_change) <= display_height - CHARACTER_RECT.height / 2 else 0

        SURFACE.fill(Colour.WHITE)
        character_idle_position(CHARACTER_RECT)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

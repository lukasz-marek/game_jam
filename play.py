class Colour(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Direction(object):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Character(object):
    def __init__(self, image_up, image_down, image_left, image_right):
        self._direction = Direction.LEFT
        self._images = {Direction.UP: image_up, Direction.DOWN: image_down, Direction.LEFT: image_left,
                        Direction.RIGHT: image_right}
        self._rectangles = {Direction.UP: image_up.get_rect(), Direction.DOWN: image_down.get_rect(),
                            Direction.LEFT: image_left.get_rect(), Direction.RIGHT: image_right.get_rect()}

    @property
    def image(self):
        return self._images[self._direction]

    @property
    def rectangle(self):
        return self._rectangles[self._direction]

    @property
    def direction(self):
        return self._direction

    def put(self, x, y):
        for rectangle in self._rectangles.values():
            rectangle.x = x
            rectangle.y = y

    def move(self, dx, dy):
        for rectangle in self._rectangles.values():
            rectangle.x += x_change if -rectangle.width / 2 < int(
                rectangle.x + x_change) <= display_width - rectangle.width / 2 else 0
            rectangle.y += y_change if -rectangle.height / 2 < int(
                rectangle.y + y_change) <= display_height - rectangle.height / 2 else 0
        self._change_direction(dx, dy)

    def _change_direction(self, dx, dy):
        if abs(dx) > abs(dy):
            self._direction = Direction.UP if dx > 0 else Direction.DOWN
        elif abs(dx) < abs(dy):
            self._direction = Direction.RIGHT if dy > 0 else Direction.LEFT


if __name__ == "__main__":
    import pygame

    display_width = 800
    display_height = 600

    pygame.init()

    GAME_DISPLAY = pygame.display

    SURFACE = GAME_DISPLAY.set_mode((display_width, display_height))
    GAME_DISPLAY.set_caption("Hack'n'Slash")
    clock = pygame.time.Clock()

    idle_character = pygame.transform.smoothscale(pygame.image.load("character_idle.png"),
                                                  (int(display_width * 0.2), int(display_height * 0.2)))

    PLAYER = Character(idle_character, idle_character, idle_character, idle_character)
    PLAYER.put(display_width * 0.5, display_height * 0.5)


    def character_idle_position(player):
        SURFACE.blit(player.image, player.rectangle)


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

        PLAYER.move(x_change, y_change)

        SURFACE.fill(Colour.WHITE)
        character_idle_position(PLAYER)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

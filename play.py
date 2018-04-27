from copy import deepcopy


class Colour(object):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Direction(object):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Orientation(object):
    HORIZONTAL = 1
    VERTICAL = 0


class Projectile(object):
    def __init__(self, image_horizontal, image_vertical, orientation):
        self._images = {Orientation.HORIZONTAL: image_horizontal, Orientation.VERTICAL: image_vertical}
        self._rectangles = {Orientation.HORIZONTAL: image_horizontal.get_rect(),
                            Orientation.VERTICAL: image_vertical.get_rect()}
        self._orientation = orientation
        self._is_fired = False
        self._is_destroyed = False
        self._dx = 0
        self._dy = 0

    @property
    def is_destroyed(self):
        return self._is_destroyed

    @property
    def image(self):
        return self._images[self._orientation]

    @property
    def rectangle(self):
        return self._rectangles[self._orientation]

    @property
    def orientation(self):
        return self._orientation

    def put(self, x, y):
        for rectangle in self._rectangles.values():
            rectangle.x = x
            rectangle.y = y

    def progress(self):
        if not self._is_fired:
            return

        for rectangle in self._rectangles.values():
            rectangle.x += self._dx if self.orientation == Orientation.HORIZONTAL else 0
            rectangle.y += self._dy if self.orientation == Orientation.VERTICAL else 0

            if rectangle.x + rectangle.width/2 < 0 or rectangle.x + rectangle.width/2 > display_width or rectangle.y + rectangle.height/2 < 0 or rectangle.y + rectangle.height/2 > display_height:
                self._is_destroyed = True

    def fire(self, dx, dy):
        self._dx = dx
        self._dy = dy
        self._is_fired = True

    def reflect(self):
        self._dx *= -1
        self._dy *= -1


class Wall(object):
    def __init__(self, image):
        self._image = image
        self._rectangle = image.get_rect()

    @property
    def image(self):
        return self._image

    @property
    def rectangle(self):
        return self._rectangle

    def put(self, x, y):
        self._rectangle.x = x
        self._rectangle.y = y


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
            self._direction = Direction.RIGHT if dx > 0 else Direction.LEFT
        elif abs(dx) < abs(dy):
            self._direction = Direction.DOWN if dy > 0 else Direction.UP


def is_move_allowed(character, obstacle, dx, dy):
    character_rect = deepcopy(character.rectangle)
    character_rect.x += dx
    character_rect.y += dy
    return not character_rect.colliderect(obstacle.rectangle)


if __name__ == "__main__":
    import pygame

    display_width = 800
    display_height = 600

    pygame.init()

    GAME_DISPLAY = pygame.display

    SURFACE = GAME_DISPLAY.set_mode((display_width, display_height))
    GAME_DISPLAY.set_caption("Hack'n'Slash")
    clock = pygame.time.Clock()

    character_left_img = pygame.transform.smoothscale(pygame.image.load("character_left.png"),
                                                      (int(display_width * 0.1), int(display_height * 0.2)))
    character_right_img = pygame.transform.smoothscale(pygame.image.load("character_right.png"),
                                                       (int(display_width * 0.1), int(display_height * 0.2)))
    character_up_img = pygame.transform.smoothscale(pygame.image.load("character_up.png"),
                                                    (int(display_width * 0.1), int(display_height * 0.2)))
    character_down_img = pygame.transform.smoothscale(pygame.image.load("character_down.png"),
                                                      (int(display_width * 0.1), int(display_height * 0.2)))

    projectile_horizontal = pygame.transform.smoothscale(pygame.image.load("bullet_left_right.png"),
                                                         (int(display_width * 0.01), int(display_height * 0.02)))
    projectile_vertical = pygame.transform.smoothscale(pygame.image.load("bullet_up_down.png"),
                                                       (int(display_width * 0.02), int(display_height * 0.01)))

    wall_img = pygame.transform.smoothscale(pygame.image.load("wall.png"),
                                            (int(display_width * 0.2), int(display_height * 0.2)))


    def fire_projectile(character):
        projectile = Projectile(projectile_vertical, projectile_horizontal,
                                Orientation.VERTICAL if character.direction in [Direction.UP,
                                                                                Direction.DOWN] else Orientation.HORIZONTAL)
        projectile.put(character.rectangle.x, character.rectangle.y)
        projectile.fire(20 if character.direction == Direction.RIGHT else -20,
                        20 if character.direction == Direction.DOWN else -20)
        return projectile


    PLAYER = Character(character_up_img, character_down_img, character_left_img, character_right_img)
    PLAYER.put(display_width * 0.5, display_height * 0.5)
    WALLS = [Wall(wall_img)]
    WALLS[0].put(display_width * 0.2, display_height * 0.2)

    PROJECTILES = []

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
                elif event.key == pygame.K_SPACE:
                    PROJECTILES.append(fire_projectile(PLAYER))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        collision_detected = not all(map(lambda x: is_move_allowed(PLAYER, x, x_change, y_change), WALLS))
        if not collision_detected:
            PLAYER.move(x_change, y_change)

        SURFACE.fill(Colour.WHITE)
        SURFACE.blit(PLAYER.image, PLAYER.rectangle)

        for wall in WALLS:
            SURFACE.blit(wall.image, wall.rectangle)

        for projectile in PROJECTILES:
            projectile.progress()
            if projectile.is_destroyed or any(map(lambda x: projectile.rectangle.colliderect(x.rectangle), WALLS)):
                PROJECTILES.remove(projectile)
            else:
                SURFACE.blit(projectile.image, projectile.rectangle)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

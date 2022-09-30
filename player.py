import pygame
# REMOVE THIS BRACKEKRETKJKKSKDJLWAJLSKDJLKWJALSJDLWJALSJDLJSKAJSKDJWLKAJKLSDJKLAWJ


class Player():  # create player class
    def __init__(self, position):  # takes position of player as parameter

        self.position = pygame.math.Vector2(position[0], position[1])  # set position using parameter

        self.pos_rect = pygame.Rect(0, 0, 100, 100)  # create player rectangle
        self.pos_rect.center = (int(self.position.x), int(self.position.y))  # set centre using self.position
        self.colour = pygame.Color("#00FF00")  # this will be removed after an image takes its place

        # movement variables
        self.speed = 5
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        self.rotation_speed = 100.0
        self.current_rotation = 0.0

        self.original_image = pygame.Surface(self.pos_rect.size, flags=pygame.SRCALPHA)
        self.original_image.fill(self.colour)
        self.current_image = self.original_image.copy()

    def movement(self, time_delta):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move_left = True
            self.move_right = False
            self.position.x -= self.speed
        if keys[pygame.K_d]:
            self.move_left = True
            self.move_right = False
            self.position.x += self.speed
        if keys[pygame.K_w]:
            self.move_up = True
            self.move_down = False
            self.position.y -= self.speed
        if keys[pygame.K_s]:
            self.move_up = False
            self.move_down = True
            self.position.y += self.speed

        x, y = pygame.mouse.get_rel()
        self.current_rotation = self.current_rotation - (x * time_delta * self.rotation_speed)
        #print(self.current_rotation)

    def update(self, time_delta):
        self.movement(time_delta)

        self.current_image = pygame.transform.rotate(self.original_image, self.current_rotation)
        self.pos_rect.size = self.current_image.get_size()
        self.pos_rect.center = (int(self.position.x), int(self.position.y))

    def draw(self, target_surface):
        target_surface.blit(self.current_image, self.pos_rect)

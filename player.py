import pygame


class Player:  # create player class
    def __init__(self, position):  # takes position of player as parameter

        self.position = pygame.math.Vector2(position[0], position[1])  # set position using parameter

        self.pos_rect = pygame.Rect(0, 0, 100, 100)  # create player rectangle
        self.pos_rect.center = (int(self.position.x), int(self.position.y))  # set centre using self.position
        self.colour = pygame.Color("#00FF00")  # this will be removed after an image takes its place

        self.view_pos_rect = self.pos_rect.copy()
        # movement variables
        self.speed = 5
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        # mouse rotation variables
        self.rotation_speed = 100.0
        self.current_rotation = 0.0

        # image of player gets copied, so it is not continuously loaded
        self.original_image = pygame.Surface(self.pos_rect.size, flags=pygame.SRCALPHA)
        self.original_image.fill(self.colour)
        self.current_image = self.original_image.copy()

    def movement(self, time_delta):  # this is where player movement is processed
        keys = pygame.key.get_pressed()  # get all key presses
        if keys[pygame.K_a]:  # if key is pressed
            self.move_left = True
            self.move_right = False
            self.position.x -= self.speed
        if keys[pygame.K_d]:  # if key is pressed
            self.move_left = True
            self.move_right = False
            self.position.x += self.speed
        if keys[pygame.K_w]:  # if key is pressed
            self.move_up = True
            self.move_down = False
            self.position.y -= self.speed
        if keys[pygame.K_s]:  # if key is pressed
            self.move_up = False
            self.move_down = True
            self.position.y += self.speed

        # find how much the mouse has moved relative to its last position
        relative_mouse_x, relative_mouse_y = pygame.mouse.get_rel()
        self.current_rotation = self.current_rotation - (relative_mouse_x * time_delta * self.rotation_speed)

    def update(self, time_delta, camera):  # update takes time since last frame as parameter
        self.movement(time_delta)  # check for movement

        # rotate the image of the player when the mouse is moved
        self.current_image = pygame.transform.rotate(self.original_image, self.current_rotation)
        self.pos_rect.size = self.current_image.get_size()  # resize the image in case it has changed size
        self.pos_rect.center = (int(self.position.x), int(self.position.y))  # recenter the image incase it has shifted
        self.view_pos_rect.centerx = self.pos_rect.centerx - camera.viewport_rect.left
        self.view_pos_rect.centery = self.pos_rect.centery - camera.viewport_rect.top

    def draw(self, target_surface):  # draw player image
        target_surface.blit(self.current_image, self.view_pos_rect)

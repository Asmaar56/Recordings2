import pygame


class Object1():  # create object1 class
    def __init__(self, position):

        self.position = pygame.math.Vector2(position[0], position[1])

        self.pos_rect = pygame.Rect(0, 0, 32, 32)  # create object rectangle
        self.pos_rect.center = (int(self.position.x), int(self.position.y))  # set object position
        self.colour = pygame.Color("#134874")

        #self.original_image = pygame.Surface(self.pos_rect.size, flags=pygame.SRCALPHA)
        self.block = pygame.image.load('game-images/block.png')
        #self.original_image.fill(self.colour)
        self.current_block = self.block.copy()

        self.block_rotation = 0

    def update(self, time_delta):

        self.current_block = pygame.transform.rotate(self.block, self.block_rotation)
        self.pos_rect.size = self.current_block.get_size()
        self.pos_rect.center = (int(self.position.x), int(self.position.y))

    def draw(self, target_surface):
        target_surface.blit(self.current_block, self.pos_rect)
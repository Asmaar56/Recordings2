import pygame


class Object1:  # create object1 class
    def __init__(self, position):

        self.position = pygame.math.Vector2(position[0], position[1])

        self.pos_rect = pygame.Rect(0, 0, 32, 32)  # create object rectangle
        self.pos_rect.center = (int(self.position.x), int(self.position.y))  # set object position

        self.block = pygame.image.load('level_states/game_images/block.png')
        self.current_block = self.block.copy()

        self.block_rotation = 0

    def update(self, time_delta):

        self.current_block = pygame.transform.rotate(self.block, self.block_rotation)
        self.pos_rect.size = self.current_block.get_size()
        self.pos_rect.center = (int(self.position.x), int(self.position.y))

    def draw(self, target_surface):
        target_surface.blit(self.current_block, self.pos_rect)
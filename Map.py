import pygame
import random


class Map:
    def __init__(self, game, WINDOW_WIDTH, WINDOW_HEIGHT):
        self.size_block = 40
        self.height = int(WINDOW_WIDTH / self.size_block)
        self.width = int(WINDOW_WIDTH / self.size_block)
        self.object_count = 15
        self.objects = []
        self.generate_world(game)

    def generate_world(self, game):
        # Создаем границы мира
        # Создаем верхние и нижние границы
        for i in range(self.width):
            if i != 1 and i != self.width - 2:
                self.objects.append( Object("wall", i * self.size_block, 0, self.size_block))
                self.objects.append(Object("wall", i * self.size_block, (self.height - 1) * self.size_block, self.size_block))
            else:
                self.objects.append(Object("guildhall", i * self.size_block, 0, self.size_block))
                self.objects.append(Object("guildhall", i * self.size_block, (self.height - 1) * self.size_block, self.size_block))
        # Создаем левые и правые границы
        for i in range(self.height - 1):
            self.objects.append(
                Object("wall", 0, i * self.size_block + 1, self.size_block))
            self.objects.append(
                Object("wall", (self.width - 1) * self.size_block, i * self.size_block + 1, self.size_block))
        # Создаем объекты внутри карты
        is_church = False
        is_guildhall = False
        is_theatre = False
        for i in range(4):
            for j in range(4):
                # Случайным образом угадываем, какой тип объекта размещать
                guess_object = random.randrange(0, 40)
                random_object = ""
                if 0 <= guess_object < 10 and not is_church:
                    random_object = "church"
                    is_church = True
                    is_guildhall = True
                elif 10 <= guess_object < 20 and not is_theatre:
                    random_object = "theatre"
                    is_theatre = True
                elif 20 <= guess_object < 30:
                    random_object = "old_house"
                elif 30 <= guess_object < 40:
                    random_object = "civilian_house"
                else:
                    random_object = "house"
                # Создаем объект
                self.objects.append(
                    Object(random_object, self.size_block * 2 + self.size_block * j * 2,
                           self.size_block * i * 2 + self.size_block * 2, self.size_block))

        # Добавляем все созданные объекты в общий массив спрайтов
        for i in self.objects:
            game.all_sprites.add(i)
            game.wall_sprites.add(i)


class Object(pygame.sprite.Sprite):
    def __init__(self, types, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.width = size
        self.height = size
        if types == "wall":
            self.image = pygame.image.load("img/wall.png")
            self.rect = self.image.get_rect()
        if types == "house":
            self.image = pygame.image.load("img/house.png")
            self.rect = self.image.get_rect()
        if types == "church":
            self.image = pygame.image.load("img/church.png")
            self.rect = self.image.get_rect()
        if types == "civilian_house":
            self.image = pygame.image.load("img/civilian_house.png")
            self.rect = self.image.get_rect()
        if types == "guildhall":
            self.image = pygame.image.load("img/guildhall.png")
            self.rect = self.image.get_rect()
        if types == "old_house":
            self.image = pygame.image.load("img/old_house.png")
            self.rect = self.image.get_rect()
        if types == "forest":
            self.image = pygame.image.load("img/forest.png")
            self.rect = self.image.get_rect()
            self.image.set_colorkey(pygame.Color(0, 0, 0))
        if types == "theatre":
            self.image = pygame.image.load("img/theatre.png")
            self.rect = self.image.get_rect()
            self.image.set_colorkey(pygame.Color(0, 0, 0))
        self.rect.x = x
        self.rect.y = y
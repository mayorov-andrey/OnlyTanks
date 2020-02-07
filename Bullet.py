import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, game, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.speed = 6
        self.tank = tank
        self.fly_direction = ""
        if self.tank.up:
            self.fly_direction = "Up"
            self.rect.x = self.tank.rect.x + self.tank.rect.width / 2 - 1
        if self.tank.down:
            self.fly_direction = "Down"
            self.rect.x = self.tank.rect.x + self.tank.rect.width / 2 - 1
            self.rect.y = self.tank.rect.y + self.tank.rect.height
        if self.tank.left:
            self.fly_direction = "Left"
            self.rect.x = self.tank.rect.x
            self.rect.y = self.tank.rect.y + self.tank.rect.height / 2 - 1
        if self.tank.right:
            self.fly_direction = "Right"
            self.rect.x = self.tank.rect.x + self.tank.rect.width
            self.rect.y = self.tank.rect.y + self.tank.rect.height / 2 - 1
        game.all_sprites.add(self)

    def update(self):
        self.fly()
        self.hit()

    def fly(self):
        if self.fly_direction == "Up":
            self.rect.y -= self.speed
        elif self.fly_direction == "Down":
            self.rect.y += self.speed
        if self.fly_direction == "Left":
            self.rect.x -= self.speed
        elif self.fly_direction == "Right":
            self.rect.x += self.speed

    def hit(self):
        # Обработка столкновений пули c стенами
        hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False)
        if hits:
            self.game.all_sprites.remove(self)
        # Обработка столкновений пули c танками-врагами
        for i in self.game.enemies:
            hits = pygame.Rect.colliderect(i.rect, self.rect)
            if hits:
                i.die()
                self.game.all_sprites.remove(self)
                break
        # Обработка столкновений пули c танком игрока
        hits = pygame.Rect.colliderect(self.game.player_tank.rect, self.rect)
        if hits:
            self.game.player_tank.die()
            self.game.all_sprites.remove(self)
            self.game.is_game_over = True

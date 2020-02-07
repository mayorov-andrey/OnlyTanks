import pygame
from Bullet import Bullet


class Tank(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("img/tank.png"), pygame.image.load("img/tank2.png"),
                       pygame.image.load("img/tank3.png"), pygame.image.load("img/tank4.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.up = True
        self.left = False
        self.right = False
        self.down = False
        self.game = game
        self.speed = 2
        self.bullets = []
        self.shoot_speed = 1000
        self.last_shoot = -self.shoot_speed
        self.game.all_sprites.add(self)
        # Загружаем звуки
        self.sound_shoot = pygame.mixer.Sound("sound/shoot.wav")
        self.sound_explosion = pygame.mixer.Sound("sound/explosion.wav")

    def update(self):
        self.go()
        self.hits()
        self.shoot()

    def go(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.up = False
            self.down = False
            self.left = True
            self.right = False
            self.image = self.images[2]
            old_x = self.rect.x
            old_y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = old_x
            self.rect.y = old_y
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.up = False
            self.down = False
            self.left = False
            self.right = True
            self.image = self.images[1]
            old_x = self.rect.x
            old_y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = old_x
            self.rect.y = old_y
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.up = True
            self.down = False
            self.left = False
            self.right = False
            self.image = self.images[0]
            old_x = self.rect.x
            old_y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = old_x
            self.rect.y = old_y
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.up = False
            self.down = True
            self.left = False
            self.right = False
            self.image = self.images[3]
            old_x = self.rect.x
            old_y = self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = old_x
            self.rect.y = old_y

    def hits(self):
        # Обработка столкновений танка c стенами
        hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False)
        if hits:
            if self.up:
                self.rect.y += self.speed
            if self.down:
                self.rect.y -= self.speed
            if self.right:
                self.rect.x -= self.speed
            if self.left:
                self.rect.x += self.speed
        # Обработка танка игрока с другими танками
        for i in self.game.enemies:
            hits = pygame.Rect.colliderect(i.rect, self.rect)
            if hits:
                # не даем двигаться танку врага
                if i.up:
                    i.rect.y += i.speed
                if i.down:
                    i.rect.y -= i.speed
                if i.right:
                    i.rect.x -= i.speed
                if i.left:
                    i.rect.x += i.speed
                # не даем двигаться танку игрока
                if self.up:
                    self.rect.y += self.speed
                if self.down:
                    self.rect.y -= self.speed
                if self.right:
                    self.rect.x -= self.speed
                if self.left:
                    self.rect.x += self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_speed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.bullets.append(Bullet(self.rect.x, self.rect.y, self.game, self))
                self.last_shoot = pygame.time.get_ticks()
                self.sound_shoot.play()

    def die(self):
        self.sound_explosion.play()
        self.game.all_sprites.remove(self)


class Enemy_tanks(Tank):
    def __init__(self, x, y, game):
        Tank.__init__(self, game, x, y)
        self.speed = 1
        self.images = [pygame.image.load("img/tank_enemy.png"), pygame.image.load("img/tank_enemy2.png"),
                       pygame.image.load("img/tank_enemy3.png"), pygame.image.load("img/tank_enemy4.png")]
        self.image = self.images[0]

    def go(self):
        # Проверяем, нехаодиться ли танк на линии карты, где можно ехать:
        if self.is_move_down():
            self.move_down()
        if self.is_move_right():
            self.move_right()
        if self.is_move_up():
            self.move_up()
        if self.is_move_left():
            self.move_left()

    def is_move_down(self):
        is_move_down = False
        now_y = self.rect.y
        final_y = self.game.player_tank.rect.y
        x_now_line = self.rect.y // self.game.game_map.size_block
        x_final_line = self.game.player_tank.rect.y // self.game.game_map.size_block
        if x_final_line % 2 == 0:
            x_final_line -= 1
        if x_now_line < x_final_line:
            if (self.rect.x + self.rect.width) // self.game.game_map.size_block % 2 != 0 and self.rect.x // self.game.game_map.size_block % 2 != 0:
                is_move_down = True
        if self.down:
            if ((self.rect.y - self.rect.height * 2) // self.game.game_map.size_block) % 2 != 0:
                is_move_down = True
            if ((self.rect.y - self.rect.height) // self.game.game_map.size_block) % 2 != 0:
                is_move_down = True
            if (self.rect.y // self.game.game_map.size_block) % 2 != 0:
                is_move_down = True
        return is_move_down

    def is_move_up(self):
        is_move_up = False
        now_y = self.rect.y
        final_y = self.game.player_tank.rect.y
        x_now_line = self.rect.y // self.game.game_map.size_block
        x_final_line = self.game.player_tank.rect.y // self.game.game_map.size_block
        if x_final_line % 2 == 0:
            x_final_line += 1
        if x_now_line >= x_final_line:
            if (self.rect.x + self.rect.width) // self.game.game_map.size_block % 2 != 0 and self.rect.x // self.game.game_map.size_block % 2 != 0:
                is_move_up = True
        if self.up:
            if ((self.rect.y + self.rect.height * 2) // self.game.game_map.size_block) % 2 != 0:
                is_move_up = True
            if ((self.rect.y + self.rect.height) // self.game.game_map.size_block) % 2 != 0:
                is_move_up = True
            if (self.rect.y // self.game.game_map.size_block) % 2 != 0:
                is_move_up = True
        return is_move_up

    def is_move_right(self):
        is_move_right = False
        now_x = self.rect.x
        final_x = self.game.player_tank.rect.x
        y_now_line = self.rect.x // self.game.game_map.size_block
        y_final_line = self.game.player_tank.rect.x // self.game.game_map.size_block
        if y_final_line % 2 == 0:
            y_final_line -= 1
        if y_now_line < y_final_line:
            if (self.rect.y + self.rect.height) // self.game.game_map.size_block % 2 != 0 and self.rect.y // self.game.game_map.size_block % 2 != 0:
                is_move_right = True
        if self.right:
            if ((self.rect.x + self.rect.width * 2) // self.game.game_map.size_block) % 2 != 0:
                is_move_right = True
            if ((self.rect.x + self.rect.width) // self.game.game_map.size_block) % 2 != 0:
                is_move_right = True
            if (self.rect.x // self.game.game_map.size_block) % 2 != 0:
                is_move_right = True
        return is_move_right

    def is_move_left(self):
        is_move_left = False
        now_x = self.rect.x
        final_x = self.game.player_tank.rect.x
        y_now_line = self.rect.x // self.game.game_map.size_block
        y_final_line = self.game.player_tank.rect.x // self.game.game_map.size_block
        if y_final_line % 2 == 0:
            y_final_line += 1
        if y_now_line >= y_final_line:
            if (self.rect.y + self.rect.height) // self.game.game_map.size_block % 2 != 0 and self.rect.y // self.game.game_map.size_block % 2 != 0:
                is_move_left = True
        if self.left:
            if ((self.rect.x - self.rect.width * 2) // self.game.game_map.size_block) % 2 != 0:
                is_move_left = True
            if ((self.rect.x - self.rect.width) // self.game.game_map.size_block) % 2 != 0:
                is_move_left = True
            if (self.rect.x // self.game.game_map.size_block) % 2 != 0:
                is_move_left = True
        return is_move_left

    def move_down(self):
        # Ехать вниз
        self.rect.y += self.speed
        self.up = False
        self.down = True
        self.left = False
        self.right = False
        self.image = self.images[3]
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y

    def move_up(self):
        # Ехать вверх
        self.rect.y -= self.speed
        self.up = True
        self.down = False
        self.left = False
        self.right = False
        self.image = self.images[0]
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y

    def move_left(self):
        # Ехать налево
        self.rect.x -= self.speed
        self.up = False
        self.down = False
        self.left = True
        self.right = False
        self.image = self.images[2]
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y

    def move_right(self):
        # Ехать направо
        self.rect.x += self.speed
        self.up = False
        self.down = False
        self.left = False
        self.right = True
        self.image = self.images[1]
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y

    def hits(self):
        # Обработка столкновений танка c стенами
        hits = pygame.sprite.spritecollide(self, self.game.wall_sprites, False)
        if hits:
            if self.up:
                self.rect.y += self.speed
            if self.down:
                self.rect.y -= self.speed
            if self.right:
                self.rect.x -= self.speed
            if self.left:
                self.rect.x += self.speed
        # Обработка столкновений танка с танком игрока
        hits = pygame.Rect.colliderect(self.rect, self.game.player_tank.rect)
        if hits:
            if self.up:
                self.rect.y += self.speed
            if self.down:
                self.rect.y -= self.speed
            if self.right:
                self.rect.x -= self.speed
            if self.left:
                self.rect.x += self.speed
            # не даем двигаться танку игрока
            if self.game.player_tank.up:
                self.game.player_tank.rect.y += self.game.player_tank.speed
            if self.game.player_tank.down:
                self.game.player_tank.rect.y -= self.game.player_tank.speed
            if self.game.player_tank.right:
                self.game.player_tank.rect.x -= self.game.player_tank.speed
            if self.game.player_tank.left:
                self.game.player_tank.rect.x += self.game.player_tank.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_speed:
            if self.is_shoot():
                self.bullets.append(Bullet(self.rect.x, self.rect.y, self.game, self))
                self.last_shoot = pygame.time.get_ticks()

    def is_shoot(self):
        is_shooting = True
        if self.game.player_tank.rect.x <= self.rect.x <= self.game.player_tank.rect.x + self.game.player_tank.rect.width:
            is_shooting = True
            if self.rect.y < self.game.player_tank.rect.y:
                self.move_down()
            if self.rect.y > self.game.player_tank.rect.y:
                self.move_up()
        if self.game.player_tank.rect.y <= self.rect.y <= self.game.player_tank.rect.y + self.game.player_tank.rect.height:
            is_shooting = True
            if self.rect.x < self.game.player_tank.rect.x:
                self.move_right()
            if self.rect.x > self.game.player_tank.rect.x:
                self.move_left()
        return is_shooting

    def die(self):
        self.sound_explosion.play()
        self.game.all_sprites.remove(self)
        self.game.spawn_enemies()
        self.game.enemies.remove(self)
        explosion_tank = Explosion(self.game, self)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, tank):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/explosion.png")
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.x
        self.rect.y = tank.rect.y
        self.game = game
        self.tank = tank
        self.time_start = pygame.time.get_ticks()
        self.time_duration = 200
        game.all_sprites.add(self)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.time_start > self.time_duration:
            self.game.all_sprites.remove(self)
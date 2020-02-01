import pygame
import random

FPS = 17
WINDOW_WIDTH = 440
WINDOW_HEIGHT = 440


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tanks")
        self.bg_img_game_start = pygame.image.load("img/game_start.png")
        self.bg_img = pygame.image.load("img/bg.png")

        # Создаем игровые объекты
        self.all_sprites = pygame.sprite.Group()  # Создаем группу всех спрайтов игры
        self.wall_sprites = pygame.sprite.Group()  # Создае группу всех спрайтов-стен игры
        self.game_map = Map(self)
        self.player_tank = Tank(self, random.randrange(self.game_map.size_block,
                                                       self.game_map.width * self.game_map.size_block - self.game_map.size_block * 2,
                                                       self.game_map.size_block),
                                self.game_map.height * self.game_map.size_block - self.game_map.size_block * 2)
        self.enemies = []
        for i in range(1):
            self.enemies.append(
                Enemy_tanks(self.game_map.size_block + i * self.game_map.size_block * 2, self.game_map.size_block,
                            self))
        self.is_game_over = False
        self.is_game_start = False
        self.music = pygame.mixer.Sound("sound/music.wav")
        # Запускаем игру
        self.play()

    def draw_text(self, surf, text, size, x, y, color):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = x - (text_rect.width / 2)
        text_rect.y = y
        surf.blit(text_surface, text_rect)

    def play(self):
        # Запускаем основной цикл игры
        self.music.play(loops=-1)
        run = True
        while run:
            # Устанавливаем FPS и проверям нажатие на значек 'Выход'
            pygame.time.delay(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if not self.is_game_start:
                self.game_start()
            else:
                if not self.is_game_over:
                    # Рисуем фон и обновляем состояние всех спрайтов
                    self.screen.blit(self.bg_img, (0, 0))
                    self.all_sprites.update()
                    # Рисуем все спрайты и обновляем экран
                    self.all_sprites.draw(self.screen)
                else:
                    self.game_over()
            # Обновляем основной цикл игры
            pygame.display.update()
        pygame.quit()

    def game_start(self):
        self.screen.blit(self.bg_img_game_start, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.is_game_start = True

    def game_over(self):
        self.music.stop()
        self.screen.fill(pygame.Color(0, 0, 0))
        self.draw_text(self.screen, "Game Over", self.game_map.size_block * 2, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2  - self.game_map.size_block, pygame.Color(255, 0, 0))

    def spawn_enemies(self):
        spawn_x = self.game_map.size_block
        spawn_y = self.game_map.size_block
        for i in range(1):
            self.enemies.append(Enemy_tanks(spawn_x, spawn_y, self))


class Map:
    def __init__(self, game):
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


def main():
    new_game = Game()

main()
import pygame
import random
from Tank import Tank, Enemy_tanks
from Map import Map


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
        self.game_map = Map(self, WINDOW_WIDTH, WINDOW_WIDTH)
        self.player_tank = Tank(self, random.randrange(self.game_map.size_block,
            self.game_map.width * self.game_map.size_block - self.game_map.size_block * 2, self.game_map.size_block),
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


def main():
    new_game = Game()


main()

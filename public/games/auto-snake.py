import pygame
import random
import time
import os
from datetime import datetime

# Инициализация Pygame
pygame.init()

# Цвета
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "GRAY": (200, 200, 200)
}

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SettingsInput:
    def __init__(self, x, y, width, height, default_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = default_text
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        color = COLORS["BLUE"] if self.active else COLORS["WHITE"]
        pygame.draw.rect(screen, color, self.rect, 2)
        font = pygame.font.SysFont("Arial", 24)
        text_surface = font.render(self.text, True, COLORS["WHITE"])
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

class SnakeGame:
    def __init__(self, field_size, speed):
        self.cell_size = 20
        self.field_width, self.field_height = field_size
        self.speed = speed
        
        # Рассчитываем размеры окна
        self.game_width = self.field_width * self.cell_size
        self.game_height = self.field_height * self.cell_size
        self.info_panel_width = 300
        self.log_panel_height = 100
        self.screen = pygame.display.set_mode(
            (self.game_width + self.info_panel_width, 
             self.game_height + self.log_panel_height)
        )
        
        self.reset_game()
        
    def reset_game(self):
        self.snake = Snake(self)
        self.food = Food(self)
        self.start_time = datetime.now()
        self.total_food_eaten = 0
        self.running = True
        self.current_score = 0
        self.best_score = self.load_best_score()

    def load_best_score(self):
        if os.path.exists("best_score.dat"):
            with open("best_score.dat", "r") as f:
                return int(f.read())
        return 0

    def save_best_score(self):
        with open("best_score.dat", "w") as f:
            f.write(str(max(self.best_score, self.current_score)))

    def draw_interface(self):
        self.screen.fill(COLORS["BLACK"])
        
        # Основное игровое поле
        pygame.draw.rect(self.screen, COLORS["BLUE"], 
                       (0, 0, self.game_width, self.game_height), 3)
        
        # Змейка
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, COLORS["GREEN"],
                           (segment[0], segment[1], 
                            self.cell_size-1, self.cell_size-1))
        
        # Еда
        pygame.draw.rect(self.screen, COLORS["RED"],
                        (self.food.position[0], self.food.position[1],
                         self.cell_size-1, self.cell_size-1))
        
        # Информационная панель
        self.draw_info_panel()
        
        # Лог-панель
        self.draw_log_panel()

    def draw_info_panel(self):
        panel_x = self.game_width + 10
        font = pygame.font.SysFont("Arial", 20)
        
        info = [
            f"Размер змейки: {len(self.snake.body)}",
            f"Съедено яблок: {self.total_food_eaten}",
            f"Текущий счет: {self.current_score}",
            f"Рекорд: {self.best_score}",
            f"Скорость: {self.speed}",
            f"Размер поля: {self.field_width}x{self.field_height}"
        ]
        
        for i, text in enumerate(info):
            text_surface = font.render(text, True, COLORS["WHITE"])
            self.screen.blit(text_surface, (panel_x, 20 + i*30))

    def draw_log_panel(self):
        panel_y = self.game_height
        font = pygame.font.SysFont("Arial", 18)
        
        game_time = datetime.now() - self.start_time
        head_x = self.snake.body[0][0] // self.cell_size
        head_y = self.snake.body[0][1] // self.cell_size
        
        texts = [
            f"Время: {str(game_time).split('.')[0]}",
            f"Координаты: ({head_x}, {head_y})"
        ]
        
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, COLORS["WHITE"])
            self.screen.blit(text_surface, (10, panel_y + 10 + i*25))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw_interface()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_best_score()
                self.running = False

    def update(self):
        self.snake.auto_control()
        if not self.snake.move():
            self.game_over()
        
        if self.snake.body[0] == self.food.position:
            self.handle_food_collision()

    def handle_food_collision(self):
        self.snake.grow = True
        self.current_score += 1
        self.total_food_eaten += 1
        if self.current_score > self.best_score:
            self.best_score = self.current_score
        self.food = Food(self)

    def game_over(self):
        self.save_best_score()
        time.sleep(1)
        self.reset_game()

class Snake:
    def __init__(self, game):
        self.game = game
        self.reset()
        
    def reset(self):
        self.body = [(self.game.game_width//2, self.game.game_height//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False
        
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx * self.game.cell_size) % self.game.game_width,
            (head_y + dy * self.game.cell_size) % self.game.game_height
        )
        
        if new_head in self.body:
            return False
            
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True
    
    def auto_control(self):
        head_x, head_y = self.body[0]
        fx, fy = self.game.food.position
        
        desired_direction = None
        if fx < head_x and self.direction != RIGHT:
            desired_direction = LEFT
        elif fx > head_x and self.direction != LEFT:
            desired_direction = RIGHT
        elif fy < head_y and self.direction != DOWN:
            desired_direction = UP
        elif fy > head_y and self.direction != UP:
            desired_direction = DOWN
        
        if desired_direction and self.is_safe_direction(desired_direction):
            self.direction = desired_direction
        else:
            safe_directions = []
            for dir in [UP, DOWN, LEFT, RIGHT]:
                if dir != (-self.direction[0], -self.direction[1]) and self.is_safe_direction(dir):
                    safe_directions.append(dir)
            if safe_directions:
                self.direction = random.choice(safe_directions)
                
    def is_safe_direction(self, direction):
        head_x, head_y = self.body[0]
        dx, dy = direction
        next_pos = (
            (head_x + dx * self.game.cell_size) % self.game.game_width,
            (head_y + dy * self.game.cell_size) % self.game.game_height
        )
        return next_pos not in self.body

class Food:
    def __init__(self, game):
        self.game = game
        self.position = self.random_position()
        
    def random_position(self):
        while True:
            x = random.randrange(0, self.game.game_width, self.game.cell_size)
            y = random.randrange(0, self.game.game_height, self.game.cell_size)
            if (x, y) not in self.game.snake.body:
                return (x, y)

def start_screen():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Настройки игры")
    
    size_input = SettingsInput(200, 100, 200, 40, "30x20")
    speed_input = SettingsInput(200, 200, 200, 40, "10")
    start_btn = pygame.Rect(250, 300, 100, 50)
    
    running = True
    while running:
        screen.fill(COLORS["BLACK"])
        
        font = pygame.font.SysFont("Arial", 24)
        screen.blit(font.render("Размер поля (ширина x высота):", True, COLORS["WHITE"]), (50, 110))
        screen.blit(font.render("Скорость змейки:", True, COLORS["WHITE"]), (50, 210))
        
        size_input.draw(screen)
        speed_input.draw(screen)
        
        pygame.draw.rect(screen, COLORS["GREEN"], start_btn)
        screen.blit(font.render("Старт", True, COLORS["BLACK"]), (270, 315))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            size_input.handle_event(event)
            speed_input.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN and start_btn.collidepoint(event.pos):
                try:
                    field_size = tuple(map(int, size_input.text.split('x')))
                    speed = int(speed_input.text)
                    return field_size, speed
                except:
                    pass

if __name__ == "__main__":
    field_size, speed = start_screen()
    game = SnakeGame(field_size, speed)
    game.run()
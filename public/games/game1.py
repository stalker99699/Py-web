from browser import document, window
import random
import math

# Подключаемся к контейнеру вывода и очищаем его
output = document['pythonOutput']
output.clear()

# Создаем и добавляем canvas
canvas = document.createElement('canvas')
output <= canvas
ctx = canvas.getContext('2d')

WIDTH, HEIGHT = 800, 600
canvas.width = WIDTH
canvas.height = HEIGHT

class Ball:
    def __init__(self):
        self.x = random.random() * WIDTH
        self.y = random.random() * HEIGHT
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.radius = random.randint(5, 25)
        self.color = f'hsl({random.randint(0, 360)}, 100%, 50%)'
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < 0 or self.y > HEIGHT: self.vy *= -1
    
    def draw(self):
        ctx.beginPath()
        ctx.arc(self.x, self.y, self.radius, 0, 2 * math.pi)
        ctx.fillStyle = self.color
        ctx.fill()

balls = [Ball() for _ in range(15)]

def animate():
    ctx.clearRect(0, 0, WIDTH, HEIGHT)
    for ball in balls:
        ball.update()
        ball.draw()
    window.requestAnimationFrame(animate)

animate()
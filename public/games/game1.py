from browser import document, window
import random

canvas = document.createElement('canvas')
document.body.appendChild(canvas)
ctx = canvas.getContext('2d')

WIDTH, HEIGHT = 800, 600
canvas.width = WIDTH
canvas.height = HEIGHT

class Ball:
    def __init__(self):
        self.x = random.random() * WIDTH
        self.y = random.random() * HEIGHT
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.radius = random.randint(5, 20)
        self.color = f'hsl({random.randint(0, 360)}, 100%, 50%)'
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0 or self.x > WIDTH: self.vx *= -1
        if self.y < 0 or self.y > HEIGHT: self.vy *= -1
    
    def draw(self):
        ctx.beginPath()
        ctx.arc(self.x, self.y, self.radius, 0, 2 * 3.1415)
        ctx.fillStyle = self.color
        ctx.fill()

balls = [Ball() for _ in range(20)]

def animate():
    ctx.clearRect(0, 0, WIDTH, HEIGHT)
    for ball in balls:
        ball.update()
        ball.draw()
    window.requestAnimationFrame(animate)

animate()
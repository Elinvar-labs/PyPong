import pygame as pg
from random import choice
pg.init()
pg.mixer.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

WIDTH = 640
HEIGHT = 480


class Sprite(pg.sprite.Sprite):
    def __init__(self, x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        if self.rect.y > HEIGHT:
            self.y_velocity *= -1
        if self.rect.y < -self.rect.height:
            self.y_velocity *= -1
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.rect.x, self.rect.y = WIDTH//2, HEIGHT//2

player_wall = Sprite(64, HEIGHT//2-HEIGHT//4, WIDTH // 32, HEIGHT // 4)
bot_wall = Sprite(WIDTH-64, HEIGHT//2-HEIGHT//4, WIDTH // 32, HEIGHT // 4)
ball = Sprite(WIDTH//2, HEIGHT//2,16,16)
font = pg.font.Font('Kubasta.ttf', 36)

all_sprites = pg.sprite.Group()
all_sprites.add(player_wall)
all_sprites.add(bot_wall)
all_sprites.add(ball)

clock = pg.time.Clock()

bump_sound = pg.mixer.Sound("bump.wav")
fail_sound = pg.mixer.Sound("fail.wav")

def main():
    display = pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption('PONG')
    start_vector = (choice((-4,4)), choice((-4,4)))
    ball.x_velocity = start_vector[0]
    ball.y_velocity = start_vector[1]
    player_points = 0
    bot_points = 0

    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player_wall.y_velocity = -8
                elif event.key == pg.K_DOWN:
                    player_wall.y_velocity = 8
            if event.type == pg.KEYUP:
                player_wall.y_velocity = 0
                player_wall.x_velocity = 0
        if ball.rect.colliderect(player_wall.rect):
                ball.y_velocity = (ball.rect.y - player_wall.rect.y)/20
                ball.x_velocity *= -1
                bump_sound.play()
        if ball.rect.colliderect(bot_wall.rect):
                ball.y_velocity = (ball.rect.y - bot_wall.rect.y)/20
                ball.x_velocity *= -1
                bump_sound.play()

        bot_wall.rect.y = ball.rect.y / 1.4

        display.fill(BLACK)
        player_wall.update()
        ball.update()
        all_sprites.draw(display)
        if ball.rect.x <= 0:
            bot_points += 1
            fail_sound.play()
        if ball.rect.x >= WIDTH:
            player_points += 1
            fail_sound.play()

        points_label = font.render(f'{player_points}  {bot_points}', False, (255, 255, 255))
        display.blit(points_label, (WIDTH//2-WIDTH//16, 36))
        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
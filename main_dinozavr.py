import random
import pygame
import time


def main():
    FPS = 150
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 800
    global running
    running = True
    score_scale = 1
    speed_scale = 1
    score = 0
    shift = 0

    class MovingObstacle(pygame.sprite.Sprite):
        def __init__(self, sprite: str, pos: str):
            super(MovingObstacle, self).__init__()
            self.surf = pygame.image.load('sprites/%s.png' % sprite)
            self.rect = self.surf.get_rect()
            self.rect.normalize()

            if pos == 'up':
                self.rect.move_ip(SCREEN_WIDTH, SCREEN_HEIGHT // 1.65)
            elif pos == 'down':
                self.rect.move_ip(SCREEN_WIDTH, SCREEN_HEIGHT - self.rect.height - 10)
            elif pos == 'bullet':
                self.rect.move_ip(player.rect.x + 150, player.rect.y)

        def update(self):
            if pygame.sprite.spritecollideany(player, abstr):
                global running
                running = False
            self.rect.move_ip(-4.5 * speed_scale, 0)

    class Bullet(MovingObstacle):
        def __init__(self):
            super(Bullet, self).__init__(sprite='bullet', pos='bullet')

        def update(self):
            if pygame.sprite.spritecollideany(self, abstr):
                for el_id, el in enumerate(abstr):
                    if self.rect.colliderect(el) and not isinstance(el, Bullet):
                        abstr.remove(el)
                        objects.pop(el_id)

                        for el_id_f, el_f in enumerate(objects):
                            if isinstance(el_f, Bullet):
                                abstr.remove(el_f)
                                objects.pop(el_id_f)
                                break
                        break
            self.rect.move_ip(12 * speed_scale, 0)

    class Dino(pygame.sprite.Sprite):
        def __init__(self, name: str):
            super(Dino, self).__init__()
            self.surf = pygame.transform.scale(pygame.image.load('sprites/dino.png'), (135, 165))
            self.rect = self.surf.get_rect()
            self.rect.move_ip(15, SCREEN_HEIGHT - self.rect.height - 10)
            self.name = name
            self.vspeed = 0
            self.last_fire = 0

        def update(self):
            if self.rect.y <= SCREEN_HEIGHT - self.rect.height:
                self.rect.y = min(SCREEN_HEIGHT - self.rect.height - 10, self.rect.y - self.vspeed)
                self.vspeed = self.vspeed - 0.15

        def jump(self):
            self.vspeed = 8.5
            self.rect.y -= self.vspeed

        def shoot(self):
            if time.time() - self.last_fire > 2.5:
                objects.append(Bullet())
                self.last_fire = time.time()

    player = Dino('Player 1')

    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], vsync=True)
    clock = pygame.time.Clock()
    objects: list[MovingObstacle | None] = []
    abstr = pygame.sprite.AbstractGroup()

    while running:
        abstr.add(objects)
        shift += 1
        score += 0.075 * score_scale
        score_scale += 0.0005
        speed_scale = score_scale ** 0.45
        screen.fill((225, 225, 225))
        player.update()

        if shift % 200 == 1:
            objects.append(random.choice((MovingObstacle('cactus', 'down'), MovingObstacle('bird', 'up'))))

        if len(objects) and (objects[0].rect.x < -150 or objects[0].rect.x > SCREEN_WIDTH * 2):
            abstr.remove(objects[0])
            objects.pop(0)

        clock.tick(FPS)

        screen.blit(player.surf, player.rect)
        fnt = pygame.font.Font(None, 40)
        text = fnt.render(str(int(score)), True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH - 100, 15))

        screen.blit(player.surf, player.rect)
        fnt = pygame.font.Font(None, 20)
        text = fnt.render('Created by Gorshipisk', True, (60, 60, 60))
        screen.blit(text, (5, 5))

        for obj in objects:
            screen.blit(obj.surf, obj.rect)
            obj.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                if player.rect.y >= SCREEN_HEIGHT - player.rect.height - 10:
                    player.jump()
            elif pygame.mouse.get_pressed()[0]:
                player.shoot()
        pygame.display.flip()
    time.sleep(3)
    main()


if __name__ == '__main__':
    main()

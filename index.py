import pygame
import math
import random
import time

isDead = False

while not isDead:
    score = 0
    run = True
    begin_game = True
    first_key = False

    difficultyAstroid = 0
    speedAdtroids = 0
    speedBackground = 0

    pygame.init()

    clock = pygame.time.Clock()
    FPS = 60

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Astroids")

    #load images
    bg = pygame.image.load("./Pictures/background.png").convert()
    bg_width = bg.get_width()
    astroidImg = pygame.image.load("./Pictures/astroid.png").convert_alpha()

    #sounds
    playsound = True
    playsound_bullet = True
    bg_music = pygame.mixer.Sound('./sounds/bg_music.mp3')
    death_sound = pygame.mixer.Sound('./sounds/dead.mp3')
    bullet_sound = pygame.mixer.Sound('./sounds/bullet.mp3')
    destroy_astroid = pygame.mixer.Sound('./sounds/astroid_explode.mp3')

    isDead = False
    scroll = 0
    tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1
    x = SCREEN_WIDTH * 0.025
    y = SCREEN_HEIGHT * 0.5
    movementSpeed = 7

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        display.blit(bulletImg, (x, y))

    class Spaceship():
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.image = pygame.image.load("./Pictures/spaceship.png").convert_alpha()
            self.rect_vertical = pygame.Rect(self.x, self.y, self.image.get_width() / 1.5, self.image.get_height())
            self.rect_horizontal = pygame.Rect(self.x, self.y + (self.image.get_height() / 3.75), self.image.get_width(), self.image.get_height() / 2)

        def draw(self):
            display.blit(self.image, (self.x, self.y))

        def update(self):
            self.rect_vertical = pygame.Rect(self.x, self.y, self.image.get_width() / 1.5, self.image.get_height())
            self.rect_horizontal = pygame.Rect(self.x, self.y + (self.image.get_height() / 3), self.image.get_width(), self.image.get_height() / 2.75)

        def showHitbox(self):
            pygame.draw.rect(display, (255,255,255), (self.x, self.y, self.image.get_width() / 1.5, self.image.get_height()), 1)
            pygame.draw.rect(display, (255,255,255), (self.x, self.y + (self.image.get_height() / 3), self.image.get_width(), self.image.get_height() / 2.75), 1)

    class Astroid():
        def __init__(self, x, y, speed):
            self.x = x
            self.y = y
            self.speed = speed
            self.rect = pygame.Rect(self.x, self.y, astroidImg.get_width(), astroidImg.get_height())

        def draw(self):
            display.blit(astroidImg, (self.x, self.y))

        def update(self):
            self.rect = pygame.Rect(self.x + 5, self.y + 5, astroidImg.get_width() - 10, astroidImg.get_height() - 10)

        def showHitbox(self):
            pygame.draw.rect(display, (255,255,255), (self.x + 5, self.y + 5, astroidImg.get_width() - 10, astroidImg.get_height() - 10), 1)

    character = Spaceship(x, y)

    bulletImg = pygame.image.load("./Pictures/bullet.png")
    x_bullet = character.x + character.image.get_width()
    y_bullet = character.y + (character.image.get_height() / 2.25)
    bulletX_change = 15
    bullet_state = "ready"
    bullets_fired = 0
    bullet_rect_active = False

    astroids = []
    amountOfAstroids = 10
    totalAstroids = 0

    while True:
        if totalAstroids < amountOfAstroids:
            astroidx = SCREEN_WIDTH
            astroidy = random.randrange(0, SCREEN_HEIGHT - astroidImg.get_height())
            astroids.append(Astroid(astroidx, astroidy, random.randrange(3, 10)))
            totalAstroids += 1
        else:
            break

    scaleDifficulty = 0
    updateDufficulty = False
    updateScore = 0

    bg_music.play(-1)

    while run:
        clock.tick(FPS)

        if score == updateScore + 600:
            if not score > 5000:
                updateDufficulty = True
                score += 1

        if updateDufficulty:
            difficultyAstroid += 2
            speedAdtroids += 1
            speedBackground += 1
            updateDufficulty = False
            updateScore = score

        if score == 2500:
            movementSpeed += 1

        if difficultyAstroid > scaleDifficulty:
            astroidx = SCREEN_WIDTH
            astroidy = random.randrange(0, SCREEN_HEIGHT - astroidImg.get_height())
            astroids.append(Astroid(astroidx, astroidy, random.randrange(2 + speedAdtroids, 10 + speedAdtroids)))
            scaleDifficulty += 1

        #background
        for i in range(0, tiles):
            display.blit(bg, (i * bg_width + scroll, 0))
    
        if not begin_game:
            for astroid in astroids:
                astroid.draw()
                astroid.update()
                #astroid.showHitbox()
                astroid.x -= astroid.speed
                if astroid.x < -astroidImg.get_width():
                    astroid.y = random.randrange(0, SCREEN_HEIGHT - astroidImg.get_height())
                    astroid.speed = random.randrange(2 + speedAdtroids, 10 + speedAdtroids)
                    astroid.x = SCREEN_WIDTH
                bullet_rect = bulletImg.get_rect(topleft = (x_bullet, y_bullet))
                if character.rect_horizontal.colliderect(astroid.rect) or character.rect_vertical.colliderect(astroid.rect):
                    isDead = True
                    updateDufficulty = False
                    if playsound:
                        death_sound.play(0)
                        playsound = False
                if bullet_rect.colliderect(astroid.rect):
                    if bullet_rect_active:
                        destroy_astroid.play(0)
                        if character.x + character.image.get_width() != astroid.x:
                            if character.y + (character.image.get_height() / 2.25) != astroid.y:
                                astroid.y = random.randrange(0, SCREEN_HEIGHT - astroidImg.get_height())
                                astroid.speed = random.randrange(2 + speedAdtroids, 10 + speedAdtroids)
                                astroid.x = SCREEN_WIDTH
                                score += 3
                        x_bullet = character.x + character.image.get_width()
                        y_bullet = character.y + (character.image.get_height() / 2.25)
                        bullets_fired = 0
                        bullet_state = "ready"
                        bullet_rect_active = False
                        playsound_bullet = True
    
        character.draw()
        #character.showHitbox()

        if begin_game:
            textStart = pygame.font.Font(None, 70)
            startGame = textStart.render("Press any key to get started, ESC to quit", 13, (255, 255, 255))
            rect = startGame.get_rect()
            rect.center = display.get_rect().center
            display.blit(startGame, rect)
    
            textScore = pygame.font.Font(None, 70)
            scoreDisplay = textScore.render("0", 13, (255, 255, 255))
            rect = scoreDisplay.get_rect()
            rect.left = display.get_rect().left + 70
            rect.top = display.get_rect().top + 30
            display.blit(scoreDisplay, rect)
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    isDead = True
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        run = False
                        isDead = True
                    else:
                        run = True
                        begin_game = False
        if not begin_game:
            textRunningScore = pygame.font.Font(None, 70)
            runningScore = textRunningScore.render(str(score), 13, (255, 255, 255))
            rect = runningScore.get_rect()
            rect.left = display.get_rect().left + 70
            rect.top = display.get_rect().top + 30
            display.blit(runningScore, rect)
    
        #scroll background
        if not isDead and not begin_game:
            scroll -= 5 + speedBackground
    
        #reset scroll
        if abs(scroll) > bg_width:
            scroll = 0
            
        for event in pygame.event.get():
            first_key = True
            if event.type == pygame.QUIT:
                run = False
                isDead = True
    
        keys = pygame.key.get_pressed()
        if not isDead and first_key:
            if keys[pygame.K_LEFT]:
                if character.x > 0:
                    character.update()
                    character.x -= movementSpeed
                    score += 1
                    if bullets_fired == 0:
                        x_bullet = character.x + character.image.get_width()
    

            if keys[pygame.K_RIGHT]:
                if character.x < SCREEN_WIDTH - character.image.get_width():
                    character.update()
                    character.x += movementSpeed
                    score += 1
                    if bullets_fired == 0:
                        x_bullet = character.x + character.image.get_width()
    
            if keys[pygame.K_UP]:
                if character.y > 0:
                    character.update()
                    character.y -= movementSpeed
                    score += 1
                    if bullets_fired == 0:
                        y_bullet = character.y + (character.image.get_height() / 2.25)
    
            if keys[pygame.K_DOWN]:
                if character.y < SCREEN_HEIGHT - character.image.get_height():
                    character.update()
                    character.y += movementSpeed
                    score += 1
                    if bullets_fired == 0:
                        y_bullet = character.y + (character.image.get_height() / 2.25)
    
            if keys[pygame.K_SPACE]:
                fire_bullet(x_bullet, y_bullet)
    
            if pygame.KEYUP:
                if bullet_state == "ready":
                    y_bullet = character.y + (character.image.get_height() / 2.25)
                    x_bullet = character.x + character.image.get_width()
                

        if x_bullet >= SCREEN_WIDTH:
            x_bullet = character.x + character.image.get_width()
            y_bullet = character.y + (character.image.get_height() / 2.25)
            bullet_state = "ready"
            playsound_bullet = True
    
        if bullet_state == "fire":
            fire_bullet(x_bullet, y_bullet)
            x_bullet += bulletX_change
            bullet_rect_active = True
            bullets_fired += 1
            if playsound_bullet:
                bullet_sound.set_volume(0.2)
                bullet_sound.play(0)
                playsound_bullet = False
    
        if isDead:
            bg_music.stop()

            text = pygame.font.Font(None, 70)
            gameover = text.render("Game Over. Press R to restart, ESC to quit", 13, (255, 255, 255))
            rect = gameover.get_rect()
            rect.center = display.get_rect().center
            display.blit(gameover, rect)
    
            textFinalScore = pygame.font.Font(None, 70)
            finalScore = textFinalScore.render("Final score: " + str(score), 13, (255, 255, 255))
            rect = finalScore.get_rect()
            rect.center = display.get_rect().center
            rect.top = display.get_rect().top + 600
            display.blit(finalScore, rect)
    
            if keys[pygame.K_r]:
                run = True
                isDead = False
                bg_music.stop()
                break
                
            if keys[pygame.K_ESCAPE]:
                run = False
        
            for astroid in astroids:
                astroid.speed = 0
                            
            scroll -= 0
    
        pygame.display.update()

pygame.quit()
# Import the pygame library and initialise the game engine
import pygame
import sys
import time
from random import randint

from paddle import Paddle
from ball import Ball

# Make sure mixer is set up *before* pygame.init for best results
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Customizable color variables
PLAYER_COLOR = WHITE       # left paddle
AI_COLOR     = WHITE       # right paddle (AI)
BALL_COLOR   = WHITE       # ball
TEXT_COLOR   = WHITE       # all text

# --- Music config ---
MUSIC_VOLUME = 0.4  # 0.0 (mute) to 1.0 (full volume)
MUSIC_PATH   = "assets/lofi_hiphop.mp3"  # change this to your file

music_enabled = False
music_paused  = False

# Try loading and starting background music (looping)
try:
    pygame.mixer.music.load(MUSIC_PATH)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)   # -1 = loop forever
    music_enabled = True
except Exception as e:
    print("Could not load music:", e)
    music_enabled = False

# --- Window setup ---
SIZE = (700, 500)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Pong")

# --- Background image ---
try:
    bg_image = pygame.image.load("assets/bg1.jpg").convert()
    bg_image = pygame.transform.scale(bg_image, SIZE)
except Exception:
    # fallback to solid black if image missing
    bg_image = pygame.Surface(SIZE)
    bg_image.fill(BLACK)

# --- Fonts (blocky arcade-style if you add the ttf; otherwise fallback) ---
def get_font(size):
    try:
        # Drop PressStart2P-Regular.ttf into assets/ to use this
        return pygame.font.Font("assets/PressStart2P-Regular.ttf", size)
    except Exception:
        return pygame.font.SysFont("hooge 05_53", size)

# All sizes reduced by ~15%
title_font = get_font(61)   # was 72
menu_font  = get_font(24)   # was 28
score_font = get_font(54)   # was 64
label_font = get_font(20)   # was 24
timer_font = get_font(24)   # was 28
count_font = get_font(128)  # was 150
end_font   = get_font(40)   # was 48

clock = pygame.time.Clock()

# --- Sprites ---
paddleA = Paddle(PLAYER_COLOR, 10, 100)
paddleA.rect.x = 30
paddleA.rect.y = SIZE[1] // 2 - 50

paddleB = Paddle(AI_COLOR, 10, 100)
paddleB.rect.x = SIZE[0] - 40
paddleB.rect.y = SIZE[1] // 2 - 50

ball = Ball(BALL_COLOR, 20, 20)
ball.rect.center = (SIZE[0] // 2, SIZE[1] // 2)

all_sprites = pygame.sprite.Group()
all_sprites.add(paddleA)
all_sprites.add(paddleB)
all_sprites.add(ball)

# --- Game state ---
scoreA = 0
scoreB = 0

difficulty = "medium"
base_speed = 4  # will be set from difficulty


def reset_ball_towards(loser_side):
    """
    loser_side: 'left' or 'right' (side that was scored on).
    The ball will move toward that side from the center.
    """
    ball.rect.center = (SIZE[0] // 2, SIZE[1] // 2)

    if loser_side == "left":
        # left player lost; ball goes left
        direction = -1
    else:
        direction = 1

    ball.velocity[0] = base_speed * direction
    ball.velocity[1] = randint(-base_speed, base_speed)
    ball.change_color(BALL_COLOR)


def pause():
    global music_paused

    paused = True
    pause_text = end_font.render("PAUSED", True, TEXT_COLOR)
    pause_rect = pause_text.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2))

    info_text = menu_font.render("Press C to continue, X to quit, M to mute", True, TEXT_COLOR)
    info_rect = info_text.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2 + 60))

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_m and music_enabled:
                    if music_paused:
                        pygame.mixer.music.unpause()
                        music_paused = False
                    else:
                        pygame.mixer.music.pause()
                        music_paused = True

        screen.blit(bg_image, (0, 0))
        screen.blit(pause_text, pause_rect)
        screen.blit(info_text, info_rect)
        pygame.display.flip()
        clock.tick(30)


# --- Difficulty menu ---
intro = True
while intro:
    screen.blit(bg_image, (0, 0))

    title_surf = title_font.render("PONG", True, TEXT_COLOR)
    title_rect = title_surf.get_rect(center=(SIZE[0] // 2, 90))
    screen.blit(title_surf, title_rect)

    byline_surf = menu_font.render("Select difficulty:", True, TEXT_COLOR)
    byline_rect = byline_surf.get_rect(center=(SIZE[0] // 2, 170))
    screen.blit(byline_surf, byline_rect)

    easy_surf = menu_font.render("1  EASY", True, TEXT_COLOR)
    med_surf  = menu_font.render("2  MEDIUM", True, TEXT_COLOR)
    hard_surf = menu_font.render("3  HARD", True, TEXT_COLOR)

    easy_rect = easy_surf.get_rect(center=(SIZE[0] // 2, 230))
    med_rect  = med_surf.get_rect(center=(SIZE[0] // 2, 270))
    hard_rect = hard_surf.get_rect(center=(SIZE[0] // 2, 310))

    screen.blit(easy_surf, easy_rect)
    screen.blit(med_surf, med_rect)
    screen.blit(hard_surf, hard_rect)

    info_surf = menu_font.render("P to PAUSE    M to MUTE    X to QUIT", True, TEXT_COLOR)
    info_rect = info_surf.get_rect(center=(SIZE[0] // 2, 380))
    screen.blit(info_surf, info_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_m and music_enabled:
                if music_paused:
                    pygame.mixer.music.unpause()
                    music_paused = False
                else:
                    pygame.mixer.music.pause()
                    music_paused = True
            elif event.key == pygame.K_1:
                difficulty = "easy"
                base_speed = 3      # slower
                intro = False
            elif event.key == pygame.K_2:
                difficulty = "medium"
                base_speed = 4
                intro = False
            elif event.key == pygame.K_3:
                difficulty = "hard"
                base_speed = 6      # fastest
                intro = False

# set initial ball velocity based on difficulty
reset_ball_towards("right")

# --- Countdown screen (3-2-1-GO) ---
counter = 3
text = "3"
pygame.time.set_timer(pygame.USEREVENT, 1000)
counting = True
while counting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            counter -= 1
            if counter > 0:
                text = str(counter)
            elif counter == 0:
                text = "GO!"
            else:
                counting = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m and music_enabled:
            if music_paused:
                pygame.mixer.music.unpause()
                music_paused = False
            else:
                pygame.mixer.music.pause()
                music_paused = True

    screen.blit(bg_image, (0, 0))
    txt_surf = count_font.render(text, True, TEXT_COLOR)
    txt_rect = txt_surf.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2))
    screen.blit(txt_surf, txt_rect)
    pygame.display.flip()
    clock.tick(60)

# --- Main game loop ---
carry_on = True
start_ticks = pygame.time.get_ticks()
TIME_LIMIT = 60  # seconds

while carry_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carry_on = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                carry_on = False
            elif event.key == pygame.K_p:
                pause()
            elif event.key == pygame.K_m and music_enabled:
                if music_paused:
                    pygame.mixer.music.unpause()
                    music_paused = False
                else:
                    pygame.mixer.music.pause()
                    music_paused = True

    # Player paddle movement (left paddle - P1)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(6)
    if keys[pygame.K_s]:
        paddleA.moveDown(6)

    # --- AI paddle movement (right paddle - P2) ---
    if difficulty == "easy":
        ai_speed = 3
        margin = 25   # bigger margin = more error
    elif difficulty == "medium":
        ai_speed = 5
        margin = 15
    else:  # hard
        ai_speed = 7
        margin = 5

    # Only actively track when ball is moving towards the AI
    if ball.velocity[0] > 0:
        if paddleB.rect.centery < ball.rect.centery - margin:
            paddleB.moveDown(ai_speed)
        elif paddleB.rect.centery > ball.rect.centery + margin:
            paddleB.moveUp(ai_speed)

    # Clamp AI paddle to the screen just in case
    if paddleB.rect.top < 0:
        paddleB.rect.top = 0
    if paddleB.rect.bottom > SIZE[1]:
        paddleB.rect.bottom = SIZE[1]

    # Update ball
    ball.update()

    # Bounce off top/bottom
    if ball.rect.top <= 0 or ball.rect.bottom >= SIZE[1]:
        ball.velocity[1] = -ball.velocity[1]
        ball.change_color(BALL_COLOR)

    # Left/right edges -> scoring + reset
    if ball.rect.right >= SIZE[0]:
        scoreA += 1
        reset_ball_towards("right")  # right player got scored on

    if ball.rect.left <= 0:
        scoreB += 1
        reset_ball_towards("left")   # left player got scored on

    # Paddle collisions
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    # Timer logic
    seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, TIME_LIMIT - seconds_passed)
    if time_left <= 0:
        carry_on = False

    # --- Drawing ---
    screen.blit(bg_image, (0, 0))

    # Center net REMOVED to keep middle "transparent" (just background)

    # Draw sprites
    all_sprites.draw(screen)

    # Scores centered-ish at top
    scoreA_surf = score_font.render(str(scoreA), True, TEXT_COLOR)
    scoreB_surf = score_font.render(str(scoreB), True, TEXT_COLOR)

    scoreA_rect = scoreA_surf.get_rect(center=(SIZE[0] // 2 - 80, 40))
    scoreB_rect = scoreB_surf.get_rect(center=(SIZE[0] // 2 + 80, 40))

    screen.blit(scoreA_surf, scoreA_rect)
    screen.blit(scoreB_surf, scoreB_rect)

    # Player labels
    labelA = label_font.render("P1", True, TEXT_COLOR)
    labelB = label_font.render("AI", True, TEXT_COLOR)
    labelA_rect = labelA.get_rect(center=(60, 25))
    labelB_rect = labelB.get_rect(center=(SIZE[0] - 60, 25))
    screen.blit(labelA, labelA_rect)
    screen.blit(labelB, labelB_rect)

    # Timer at top center
    timer_surf = timer_font.render(f"{time_left:02d}", True, TEXT_COLOR)
    timer_rect = timer_surf.get_rect(center=(SIZE[0] // 2, 20))
    screen.blit(timer_surf, timer_rect)

    pygame.display.flip()
    clock.tick(60)

# --- End screen ---
winner_text = "DRAW!"
if scoreA > scoreB:
    winner_text = "PLAYER 1 WINS!"
elif scoreB > scoreA:
    winner_text = "AI WINS!"

end = True
while end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_x, pygame.K_ESCAPE, pygame.K_SPACE):
                end = False
            elif event.key == pygame.K_m and music_enabled:
                if music_paused:
                    pygame.mixer.music.unpause()
                    music_paused = False
                else:
                    pygame.mixer.music.pause()
                    music_paused = True

    screen.blit(bg_image, (0, 0))
    win_surf = end_font.render(winner_text, True, TEXT_COLOR)
    win_rect = win_surf.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2))
    screen.blit(win_surf, win_rect)

    info_surf = menu_font.render("Press SPACE or X to quit   |   M to mute", True, TEXT_COLOR)
    info_rect = info_surf.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2 + 60))
    screen.blit(info_surf, info_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

import pygame
import os
from time import sleep as tsleep
pygame.font.init()
#pygame.mixer.init()


# DISPLAY SETTINGS;
WIDTH, HEIGHT = 1680, 1050
# F11처럼 전체화면
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# PLAYER DATA;
#체급
PLAYER_WIDTH = 100
#키
PlAYER_HEIGHT = 125
PLAYER_VELOCITY = 10
JUMP_VELOCITY = 35 # <-- 점프 초기 속도
PLAYER_GREEN_HEALTH = 3
PLAYER_RED_HEALTH = 3
CENTER_PLAYER_PLACEMENT_WIDTH = (WIDTH//2)-(PLAYER_WIDTH//2)
CENTER_PLAYER_PLACEMENT_HEIGHT = 100
STANDARD_PER_ROUND_HEALTH = 20
GREEN_PEROUND_HEALTH = STANDARD_PER_ROUND_HEALTH
RED_PEROUND_HEALTH = STANDARD_PER_ROUND_HEALTH
GREEN_FACING = "right"
RED_FACING = "left"
STANDARD_BULLET_COUNT = 5
GREEN_BULLET_COUNT = STANDARD_BULLET_COUNT
RED_BULLET_COUNT = STANDARD_BULLET_COUNT
GREEN_RELOAD_TIMER = 0
RED_RELOAD_TIMER = 0

# IMAGE LOADERS;
resource_dir = os.path.dirname(__file__)
def rsrc(path):
    return os.path.join(resource_dir, path)

BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load(rsrc("image_2play/Fighter_Game_BG.png")), (WIDTH, HEIGHT)
)

# GAME SETTINGS;
#중력
GRAVITY = 15
MAX_FPS = 240
#탄속
BULLET_VELOCITY = 8 #40
#넉백
GUN_KNOCKBACK_HORIZONTAL = 30
GUN_KNOCKBACK_VERTICAL = 30 #100

# MAP VALUES;
#장애물 하나하나 크기 바꾸고싶으면 예) "LEFT_BOTTOM_RECT   = pygame.Rect(100, 750, 300, 20)" 가로 300, 세로 20 요런식으로 바꾸세요
# 복잡하고 재미있는 맵 구성용 플랫폼 정의
PLATFORMS = [
    # 바닥 왼쪽 & 오른쪽 큰 발판
    pygame.Rect(100, 950, 400, 40),
    pygame.Rect(1180, 950, 400, 40),

    # 중앙 넓은 중간 발판
    pygame.Rect(WIDTH//2 - 150, 700, 300, 40),

    # 왼쪽 계단식 작은 발판
    pygame.Rect(200, 850, 100, 20),
    pygame.Rect(300, 770, 100, 20),
    pygame.Rect(400, 690, 100, 20),

    # 오른쪽 계단식 작은 발판
    pygame.Rect(1380, 850, 100, 20),
    pygame.Rect(1280, 770, 100, 20),
    pygame.Rect(1180, 690, 100, 20),

    # 중앙 상단의 좁은 발판들 (점프/공중 회피용)
    pygame.Rect(WIDTH//2 - 100, 500, 200, 25),
    pygame.Rect(WIDTH//2 + 200, 400, 100, 25),
    pygame.Rect(WIDTH//2 - 300, 400, 100, 25),
    pygame.Rect(WIDTH//2 - 250, 300, 100, 20),
    pygame.Rect(WIDTH//2 + 170, 270, 100, 20),
]

# COLORS;
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (252, 161, 3)

# RELOADING FLAGS
RED_IS_RELOADING = False
GREEN_IS_RELOADING = False

# 점프 상태와 점프 강도 변수 추가
is_jumping_green = False
green_jump_strength = 0

is_jumping_red = False
red_jump_strength = 0


# Called whenever a heart is lost,
# Takes the name of the heart-looser as a string and verbally says "player has died";
#def playLostHeartAUDIO(whoDied):
#    if whoDied == "red":
#        pygame.mixer.music.load(os.path.join("sound_2play", "red_has_died.mp3"))
 #   else:
#        pygame.mixer.music.load(os.path.join("sound_2play", "green_has_died.mp3"))
  #  pygame.mixer.music.play()


# Checks The map-rectangles for horizontal player collision;
# Takes the playerToCheck as a parameter (eg: red, green);
# If the player doesn't collide returns True, if the player does collide with any rectangle it returns a False;
# This way the lower-movements or gravity know which places to check vertically too for, so based of of that,
# the player is either eligible to sink-lower or not;

   
# If the player doesn't collide with any rectangle vertically, retturns True;
# Otherwise, returns False;
# This function is needed for movement/physics blocking places (eg: platforms);


# Moves the green player;
# Takes the pressed keys of the desired character and runs code based off of that;
def move_player_green(keys_pressed, green):
    global GREEN_FACING
    if keys_pressed[pygame.K_a] and green.x > 0:
        GREEN_FACING = "left"
        green.x -= PLAYER_VELOCITY

    if keys_pressed[pygame.K_d] and green.x < WIDTH - PLAYER_WIDTH:
        GREEN_FACING = "right"
        green.x += PLAYER_VELOCITY

# Moves the red player
def move_player_red(keys_pressed, red):
    global RED_FACING
    if keys_pressed[pygame.K_LEFT] and red.x > 0:
        RED_FACING = "left"
        red.x -= PLAYER_VELOCITY

    if keys_pressed[pygame.K_RIGHT] and red.x < WIDTH - PLAYER_WIDTH:
        RED_FACING = "right"
        red.x += PLAYER_VELOCITY

# This function is responsible for keeping the players from floating;
# Function takes playerToCheck as a parameter, the parameter is the desired player;
# The function then checks if the player is elligible for being lowered via a collision detection;
# If the player is eligible, the player gets lowered by the game gravity count;


# Takes the object of the player and the players name in a string form;
# Checks if the player is lower than the game height, if it is, the player gets respawned and looses one heart;
def checkIfPlayerDead(deadPlayer, deadPlayerSpeaker):
    global PLAYER_RED_HEALTH, PLAYER_GREEN_HEALTH
    if deadPlayer.y + deadPlayer.height > HEIGHT:
#        playLostHeartAUDIO(deadPlayerSpeaker)
        deadPlayer.x = CENTER_PLAYER_PLACEMENT_WIDTH
        deadPlayer.y = CENTER_PLAYER_PLACEMENT_HEIGHT
        if deadPlayerSpeaker == "red":
            PLAYER_RED_HEALTH-=1
        else:
            PLAYER_GREEN_HEALTH-=1
        checkIfWinF()

# Called when a player is hit with a gun, post a collision detection return;
# Parameter is just a string value of the player that has been hit,
# Based off of who the hit player is, the hit player looses one per-round-health, which if gets to 0 causes the player to loose one heart;
def player_hit_with_gun(hitPlayer):
    global RED_PEROUND_HEALTH, GREEN_PEROUND_HEALTH
    if hitPlayer == "red":
        RED_PEROUND_HEALTH-=5
    else:
        GREEN_PEROUND_HEALTH-=5

# This function is called if a win is confirmed, Game freezes and the winner gets displayed on the screen;    
def actualWinF(whoWon):
    WIN.blit(pygame.font.SysFont('Comic Sans MS', 80).render(whoWon + " HAS WON THE GAME!", 1, RED), (200, 400))
    pygame.display.update()
    import subprocess, sys, os
    tsleep(2)
    launcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../my_launcher.py'))
    subprocess.Popen([sys.executable, launcher_path])
    pygame.quit()
    sys.exit()

# Checks if the health of both players are 0, otherwise calls the actualWinF() with the username/display_name as the parameter;    
def checkIfWinF():
    if PLAYER_RED_HEALTH <= 0:
        actualWinF("LUISE")
    if PLAYER_GREEN_HEALTH <= 0:
        actualWinF("MARIO")
       
# If a player looses all their per_round_health, this function is called with the players object in the parameters;
# Then the player is placed far low in the screen which causes the death of the player due to the other bottom-killzone functions;
def killPlayer(playerToKill):
    playerToKill.y = 2000

# Checks if all per_round_health of the desired player is over 0, if it isnt, the player gets killed;
def checkIfAllHeartsGone(playerToCheck, playerName):
    global RED_PEROUND_HEALTH, GREEN_PEROUND_HEALTH, STANDARD_PER_ROUND_HEALTH
    if playerName == "red":
        if RED_PEROUND_HEALTH <= 0:
            killPlayer(playerToCheck)
            RED_PEROUND_HEALTH=STANDARD_PER_ROUND_HEALTH
    else:
        if GREEN_PEROUND_HEALTH <= 0:
            killPlayer(playerToCheck)
            GREEN_PEROUND_HEALTH=STANDARD_PER_ROUND_HEALTH

# This is used to display the health-bar with a valid color;
# username as a string is given to the function;
# based off of the name, the health is checked and the proper display color is returned;
def getValidHealthColorF(playerToCheck):
    if playerToCheck == "red":
        if RED_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//1.5:
            return GREEN
        elif RED_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//4:
            return ORANGE
        else:
            return RED
    else:
        if GREEN_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//2:
            return GREEN
        elif GREEN_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//4:
            return ORANGE
        else:
            return RED

# Rerenders the entire screen;
def reRenderScreenF(green, red, playerHealths, gameFPS, red_bullets, green_bullets):
    global RED_FACING, GREEN_FACING, STANDARD_BULLET_COUNT, RED_IS_RELOADING, GREEN_IS_RELOADING
    # Creating a few fonts that will be needed;
    comicFont = pygame.font.SysFont('Comic Sans MS', 60)
    fpsFont = pygame.font.SysFont('Arial', 30)
    is_reloading_font = pygame.font.SysFont("Comic Sans MS", 25)
   
    # Setting the background to the background-image;
    WIN.blit(BACKGROUND_IMAGE, (0,0))

    # Rendering the map;
    for platform in PLATFORMS:pygame.draw.rect(WIN, WHITE, platform, 7)
    # heart 이미지 로딩
    heart_img = pygame.transform.scale(pygame.image.load(rsrc("image_2play/heart.png")), (50, 50))

    # PLAYER HEALTH/INFO TEXTS
    WIN.blit(comicFont.render("LUISE:", 1, (WHITE)), (20, 10))
    # LUISE 생명 이미지 표시
    for i in range(playerHealths[0]):
        WIN.blit(heart_img, (20 + i * 55, 72))
    pygame.draw.rect(WIN, getValidHealthColorF("green"), pygame.Rect(20, 150, 15*GREEN_PEROUND_HEALTH, 40))

    WIN.blit(comicFont.render("MARIO:", 1, (WHITE)), (1365, 10))
    # MARIO 생명 이미지 표시
    for i in range(playerHealths[1]):
        WIN.blit(heart_img, (1365 + i * 55, 72))
    pygame.draw.rect(WIN, getValidHealthColorF("red"), pygame.Rect(1365, 150, 15*RED_PEROUND_HEALTH, 40))

    # AMMO COUNT
    WIN.blit(comicFont.render(f"{str(GREEN_BULLET_COUNT)}/{str(STANDARD_BULLET_COUNT)}", 1, (WHITE)), (20, 200)) #Green
    WIN.blit(comicFont.render(f"{str(RED_BULLET_COUNT)}/{str(STANDARD_BULLET_COUNT)}", 1, (WHITE)), (1470, 200)) #Red
   
    # Rendering the fps
    WIN.blit(fpsFont.render("FPS: " + str(round(gameFPS, 0)), 1, (WHITE)), (750, 20))

    PLAYER_RED_IMAGE = pygame.transform.scale(pygame.image.load(rsrc(f"image_2play/fighter_weed-red-{RED_FACING}.png")), (PLAYER_WIDTH, PlAYER_HEIGHT))
    PLAYER_GREEN_IMAGE = pygame.transform.scale(pygame.image.load(rsrc(f"image_2play/fighter_weed-green-{GREEN_FACING}.png")), (PLAYER_WIDTH, PlAYER_HEIGHT))
    # Rendering the players;
    WIN.blit(PLAYER_GREEN_IMAGE, (green.x, green.y))
    WIN.blit(PLAYER_RED_IMAGE, (red.x, red.y))

    # Rendering the bullets;
    for bullet in green_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    # 우측 하단에 'Home "M"' 표시 (옛날 게임 느낌)
    font = pygame.font.Font(None, 28)
    text = 'Home "M"'
    txt_surface = font.render(text, True, (40, 40, 40))
    WIN.blit(txt_surface, (WIDTH - txt_surface.get_width() - 10, HEIGHT - txt_surface.get_height() - 8))
    txt_surface = font.render(text, True, (255, 255, 255))
    WIN.blit(txt_surface, (WIDTH - txt_surface.get_width() - 12, HEIGHT - txt_surface.get_height() - 10))
    pygame.display.update()


# Handling the bullets movements/collisions;
def handleBullets(color_bullets, bullet_type, target, hittargetname):
    x = 0
    for bullet in color_bullets:
        if bullet_type[x] == "right":
            bullet.x += BULLET_VELOCITY
        else:
            bullet.x -= BULLET_VELOCITY
        if bullet.colliderect(target):
            target.y -= GUN_KNOCKBACK_VERTICAL
            if bullet_type[x] == "right":
                target.x+=GUN_KNOCKBACK_HORIZONTAL
            else:
                target.x-=GUN_KNOCKBACK_HORIZONTAL
            color_bullets.remove(bullet)
            bullet_type.remove(bullet_type[x])
            player_hit_with_gun(hittargetname)
        x+=1


#def play_gun_fire_audio():
 #   pygame.mixer.music.load(os.path.join("sound_2play", "gun_shot_sound_effect.mp3"))
  #  pygame.mixer.music.set_volume(0.7)
   # pygame.mixer.music.play()

#def play_reload_audio():
 #   pygame.mixer.music.load(os.path.join("sound_2play", "gun_reload.mp3"))
  #  pygame.mixer.music.set_volume(1)
   # pygame.mixer.music.play()


def apply_player_physics(player, player_name):
    global is_jumping_green, green_jump_strength, is_jumping_red, red_jump_strength

    if player_name == 'green':
        is_jumping = is_jumping_green
        jump_strength = green_jump_strength
    else:
        is_jumping = is_jumping_red
        jump_strength = red_jump_strength

    on_ground = False

    # 점프 중이면 위로 이동
    if is_jumping:
        player.y -= jump_strength
        jump_strength -= 1
        if jump_strength < 0:
            is_jumping = False

    # 중력 적용
    player.y += GRAVITY

    # 플랫폼 충돌 처리
    for platform in PLATFORMS:
        if (
            player.y + player.height >= platform.y and
            player.y + player.height - GRAVITY <= platform.y and
            player.x + player.width > platform.x and
            player.x < platform.x + platform.width
        ):
            player.y = platform.y - player.height
            # 점프 중이면 멈추지 않고, 점프가 끝났을 때만 멈춤
            if not is_jumping:
                is_jumping = False
                jump_strength = 0
                on_ground = True
            break

    # 바닥에 닿았을 때
    if player.y + player.height >= HEIGHT:
        player.y = HEIGHT - player.height
        is_jumping = False
        jump_strength = 0
        on_ground = True

    # 값 반영
    if player_name == 'green':
        is_jumping_green = is_jumping
        green_jump_strength = jump_strength
    else:
        is_jumping_red = is_jumping
        red_jump_strength = jump_strength

    return on_ground
def main():
    global RED_FACING, GREEN_FACING, GREEN_BULLET_COUNT, RED_BULLET_COUNT, RED_IS_RELOADING, GREEN_IS_RELOADING
    global is_jumping_green, is_jumping_red
    global green_jump_strength, red_jump_strength

    isRunning = True

    green = pygame.Rect(CENTER_PLAYER_PLACEMENT_WIDTH, CENTER_PLAYER_PLACEMENT_HEIGHT, PLAYER_WIDTH, PlAYER_HEIGHT)
    red = pygame.Rect(CENTER_PLAYER_PLACEMENT_WIDTH, CENTER_PLAYER_PLACEMENT_HEIGHT, PLAYER_WIDTH, PlAYER_HEIGHT)

    green_bullets = []
    green_bullet_types = []
    red_bullets = []
    red_bullet_types = []
   
    # 지상 상태 변수
    green_on_ground = False
    red_on_ground = False

    gameClock = pygame.time.Clock()

    while isRunning:
        gameClock.tick(MAX_FPS)
       
        # -------------------
        # 점프 및 중력 적용 (키보드 이벤트보다 먼저 처리)
        # -------------------
        green_on_ground = apply_player_physics(green, 'green')
        red_on_ground = apply_player_physics(red, 'red')

        # 키보드 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                #esc 로 종료
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                # M 키 누르면 게임런처 실행 후 종료
                elif event.key == pygame.K_m:
                    import subprocess, sys, os
                    launcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../my_launcher.py'))
                    subprocess.Popen([sys.executable, launcher_path])
                    pygame.quit()
                    sys.exit()
                # 점프 시작
                if event.key == pygame.K_w and green_on_ground:
                    is_jumping_green = True
                    green_jump_strength = JUMP_VELOCITY
                if event.key == pygame.K_UP and red_on_ground:
                    is_jumping_red = True
                    red_jump_strength = JUMP_VELOCITY

                # 발사 로직
                if event.key == pygame.K_LCTRL or event.key == pygame.K_SPACE:
                    if GREEN_BULLET_COUNT > 0:
                        GREEN_BULLET_COUNT -= 1
                        bullet = pygame.Rect(green.x, green.y + green.height//2 - 2, 10, 5)
                        green_bullets.append(bullet)
                        green_bullet_types.append(GREEN_FACING)
                        if GREEN_BULLET_COUNT == 0:
                            GREEN_RELOAD_TIMER = pygame.time.get_ticks()

                if event.key == pygame.K_RCTRL or event.key == pygame.K_SLASH:
                    if RED_BULLET_COUNT > 0:
                        RED_BULLET_COUNT -= 1
                        bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)
                        red_bullet_types.append(RED_FACING)
                        if RED_BULLET_COUNT == 0:
                            RED_RELOAD_TIMER = pygame.time.get_ticks()
       
        # 자동 재장전 처리
        if GREEN_BULLET_COUNT == 0 and GREEN_RELOAD_TIMER:
            if pygame.time.get_ticks() - GREEN_RELOAD_TIMER >= 3000:
                GREEN_BULLET_COUNT = STANDARD_BULLET_COUNT
                GREEN_RELOAD_TIMER = 0
        if RED_BULLET_COUNT == 0 and RED_RELOAD_TIMER:
            if pygame.time.get_ticks() - RED_RELOAD_TIMER >= 3000:
                RED_BULLET_COUNT = STANDARD_BULLET_COUNT
                RED_RELOAD_TIMER = 0

        # Handling the bullets
        handleBullets(green_bullets, green_bullet_types, red, "red")
        handleBullets(red_bullets, red_bullet_types, green, "green")

        # Collecting all movements;
        keys_pressed = pygame.key.get_pressed()
        move_player_green(keys_pressed, green) # Player-Green movements;
        move_player_red(keys_pressed, red) # Player-Red movements;

        # Checking if any players lost all their hearts
        checkIfAllHeartsGone(red, "red")
        checkIfAllHeartsGone(green, "green")

        # Checking if any players are under the *DEATH-ZONE*
        checkIfPlayerDead(red, "red")
        checkIfPlayerDead(green, "green")

        # Calling the window update function as the last thing in the loop;
        reRenderScreenF(green, red, [PLAYER_GREEN_HEALTH, PLAYER_RED_HEALTH], gameClock.get_fps(), red_bullets, green_bullets)


if __name__ == "__main__":
    main()
import pygame
import sys
import math
import random
import os
from pygame.locals import *

resource_dir = os.path.dirname(__file__)
def rsrc(path):
    return os.path.join(resource_dir, path)

# 색상 정의
BLACK = (0, 0, 0)
SILVER = (192, 208, 224)
RED = (255, 0, 0)
CYAN = (0, 224, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# 이미지 로딩
try:
    img_galaxy = pygame.image.load(rsrc("image_plane/sky.jpg"))
    img_sship = [
        pygame.image.load(rsrc("image_plane/f-22.png")),
        pygame.image.load(rsrc("image_plane/f-22.png")),
        pygame.image.load(rsrc("image_plane/f-22.png")),
        pygame.image.load(rsrc("image_plane/starship_burner.png"))
    ]
    img_sship[0] = pygame.transform.scale(img_sship[0], (75, 100))
    img_sship[0] = pygame.transform.rotate(img_sship[0], 0)
    img_sship[1] = pygame.transform.scale(img_sship[1], (75, 100))
    img_sship[1] = pygame.transform.rotate(img_sship[1], 30)
    img_sship[2] = pygame.transform.scale(img_sship[1], (75, 100))
    img_sship[2] = pygame.transform.rotate(img_sship[2], -30)
    img_weapon = pygame.image.load(rsrc("image_plane/missile.png"))
    img_weapon = pygame.transform.scale(img_weapon, (50, 125))
    img_shield = pygame.image.load(rsrc("image_plane/shield.png"))
    img_enemy = [
        pygame.image.load(rsrc("image_plane/enemy0.png")),
        pygame.image.load(rsrc("image_plane/enemy1.png")),
        pygame.image.load(rsrc("image_plane/enemy2.png")),
        pygame.image.load(rsrc("image_plane/enemy3.png")),
        pygame.image.load(rsrc("image_plane/enemy4.png")),
        pygame.image.load(rsrc("image_plane/enemy_boss.png")),
        pygame.image.load(rsrc("image_plane/enemy_boss_f.png"))
    ]
    img_explode = [
        None,
        pygame.image.load(rsrc("image_plane/explosion1.png")),
        pygame.image.load(rsrc("image_plane/explosion2.png")),
        pygame.image.load(rsrc("image_plane/explosion3.png")),
        pygame.image.load(rsrc("image_plane/explosion4.png")),
        pygame.image.load(rsrc("image_plane/explosion5.png"))
    ]
    img_title = [
        pygame.image.load(rsrc("image_plane/nebula.png")),
        pygame.image.load(rsrc("image_plane/logo.png"))
    ]
except Exception as e:
    print(f"이미지 로드 오류: {e}")
    sys.exit(1)

# SE 로딩 변수
se_damage = None
se_explosion = None
se_shot = None

# 게임 상태 변수
idx = 0
tmr = 0
score = 0
hisco = 10000
new_record = False
bg_y = 0
ss_x = 0
ss_y = 0
ss_d = 0
ss_shield = 0
ss_muteki = 0
key_spc = 0
MISSILE_MAX = 200
msl_no = 0
msl_f = [False] * MISSILE_MAX
msl_x = [0] * MISSILE_MAX
msl_y = [0] * MISSILE_MAX
msl_a = [0] * MISSILE_MAX
ENEMY_MAX = 100
emy_no = 0
emy_f = [False] * ENEMY_MAX
emy_x = [0] * ENEMY_MAX
emy_y = [0] * ENEMY_MAX
emy_a = [0] * ENEMY_MAX
emy_type = [0] * ENEMY_MAX
emy_speed = [0] * ENEMY_MAX
emy_shield = [0] * ENEMY_MAX
emy_count = [0] * ENEMY_MAX
enemy_kill_count = 0
EMY_BULLET = 0
EMY_ZAKO = 1
EMY_BOSS = 5
LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040
EFFECT_MAX = 100
eff_no = 0
eff_p = [0] * EFFECT_MAX
eff_x = [0] * EFFECT_MAX
eff_y = [0] * EFFECT_MAX

def get_dis(x1, y1, x2, y2):
    return ((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

def draw_text(scrn, txt, x, y, siz, col):
    try:
        fnt = pygame.font.Font(None, siz)
        cr = int(col[0] / 2)
        cg = int(col[1] / 2)
        cb = int(col[2] / 2)
        sur = fnt.render(txt, True, (cr, cg, cb))
        x = x - sur.get_width() / 2
        y = y - sur.get_height() / 2
        scrn.blit(sur, [x + 1, y + 1])
        cr = min(col[0] + 128, 255)
        cg = min(col[1] + 128, 255)
        cb = min(col[2] + 128, 255)
        sur = fnt.render(txt, True, (cr, cg, cb))
        scrn.blit(sur, [x - 1, y - 1])
        sur = fnt.render(txt, True, col)
        scrn.blit(sur, [x, y])
    except Exception as e:
        print(f"텍스트 렌더링 오류: {e}")

def move_starship(scrn, key):
    global idx, tmr, ss_x, ss_y, ss_d, ss_shield, ss_muteki, key_spc
    mouse_x, mouse_y = pygame.mouse.get_pos()
    direction_threshold = 10
    ss_d = 0
    if mouse_x > ss_x + direction_threshold:
        ss_d = 2
    elif mouse_x < ss_x - direction_threshold:
        ss_d = 1
    ss_x = mouse_x
    ss_y = mouse_y
    if ss_x < 40:
        ss_x = 40
    if ss_x > 920:
        ss_x = 920
    if ss_y < 80:
        ss_y = 80
    if ss_y > 640:
        ss_y = 640
    key_spc = (key_spc + 1) * key[K_SPACE]
    if key_spc % 5 == 1:
        set_missile(0)
        if se_shot:
            se_shot.play()
    if ss_muteki % 2 == 0:
        if mouse_x > ss_x + direction_threshold:
            scrn.blit(img_sship[3], [ss_x - 8, ss_y + 30 + (tmr % 3) * 2])
        elif mouse_x < ss_x - direction_threshold:
            scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2])
        else:
            scrn.blit(img_sship[3], [ss_x - 8, ss_y + 40 + (tmr % 3) * 2])
        scrn.blit(img_sship[ss_d], [ss_x - 37, ss_y - 48])
    if ss_muteki > 0:
        ss_muteki -= 1
        return
    if idx == 1:
        for i in range(ENEMY_MAX):
            if emy_f[i]:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w + h) / 4 + (img_sship[0].get_width() + img_sship[0].get_height()) / 4)
                if get_dis(emy_x[i], emy_y[i], ss_x, ss_y) < r * r:
                    set_effect(ss_x, ss_y)
                    ss_shield -= 10
                    if ss_shield <= 0:
                        ss_shield = 0
                        idx = 2
                        tmr = 0
                    if ss_muteki == 0:
                        ss_muteki = 40
                        if se_damage:
                            se_damage.play()
                    if emy_type[i] < EMY_BOSS:
                        emy_f[i] = False

def set_missile(typ):
    global msl_no
    if typ == 0:
        msl_f[msl_no] = True
        msl_x[msl_no] = ss_x
        msl_y[msl_no] = ss_y - 50
        msl_a[msl_no] = 270
        msl_no = (msl_no + 1) % MISSILE_MAX

def move_missile(scrn):
    movement_angle = 270
    move_speed = 36
    for i in range(MISSILE_MAX):
        if msl_f[i]:
            dx = move_speed * math.cos(math.radians(movement_angle))
            dy = move_speed * math.sin(math.radians(movement_angle))
            msl_x[i] += dx
            msl_y[i] += dy
            rotation_angle = -90 - movement_angle
            img_rz = pygame.transform.rotozoom(img_weapon, rotation_angle, 1.0)
            scrn.blit(img_rz, [msl_x[i] - img_rz.get_width() / 2, msl_y[i] - img_rz.get_height() / 2])
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:
                msl_f[i] = False

def bring_enemy():
    sec = tmr / 30
    if 0 < sec < 25:
        if tmr % 15 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)
    if 30 < sec < 55:
        if tmr % 10 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO + 1, 12, 1)
    if 60 < sec < 85:
        if tmr % 15 == 0:
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)
    if 90 < sec < 115:
        if tmr % 20 == 0:
            set_enemy(random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2)
    if 120 < sec < 145:
        if tmr % 20 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)
    if 150 < sec < 175:
        if tmr % 20 == 0:
            set_enemy(random.randint(20, 940), LINE_B, 270, EMY_ZAKO, 8, 1)
            set_enemy(random.randint(20, 940), LINE_T, random.randint(70, 110), EMY_ZAKO + 1, 12, 1)
    if 180 < sec < 205:
        if tmr % 20 == 0:
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)
            set_enemy(random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2)
    if 210 < sec < 235:
        if tmr % 20 == 0:
            set_enemy(LINE_L, random.randint(40, 680), 0, EMY_ZAKO, 12, 1)
            set_enemy(LINE_R, random.randint(40, 680), 180, EMY_ZAKO + 1, 18, 1)
    if 240 < sec < 265:
        if tmr % 30 == 0:
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1)
            set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO + 1, 12, 1)
            set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO + 2, 6, 3)
            set_enemy(random.randint(100, 860), LINE_T, 90, EMY_ZAKO + 3, 12, 2)
    if tmr == 30 * 270:
        set_enemy(480, -210, 90, EMY_BOSS, 4, 200)

def set_enemy(x, y, a, ty, sp, sh):
    global emy_no
    while True:
        if not emy_f[emy_no]:
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            emy_shield[emy_no] = sh
            emy_count[emy_no] = 0
            break
        emy_no = (emy_no + 1) % ENEMY_MAX

def move_enemy(scrn):
    global idx, tmr, score, hisco, new_record, ss_shield, enemy_kill_count
    for i in range(ENEMY_MAX):
        if emy_f[i]:
            ang = -90 - emy_a[i]
            png = emy_type[i]
            if emy_type[i] < EMY_BOSS:
                emy_x[i] += emy_speed[i] * math.cos(math.radians(emy_a[i]))
                emy_y[i] += emy_speed[i] * math.sin(math.radians(emy_a[i]))
                if emy_type[i] == 4:
                    emy_count[i] += 1
                    ang = emy_count[i] * 10
                    if emy_y[i] > 240 and emy_a[i] == 90:
                        emy_a[i] = random.choice([50, 70, 110, 130])
                        set_enemy(emy_x[i], emy_y[i], 90, EMY_BULLET, 6, 0)
                if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:
                    emy_f[i] = False
            else:
                if emy_count[i] == 0:
                    emy_y[i] += 2
                    if emy_y[i] >= 200:
                        emy_count[i] = 1
                elif emy_count[i] == 1:
                    emy_x[i] -= emy_speed[i]
                    if emy_x[i] < 200:
                        for j in range(0, 10):
                            set_enemy(emy_x[i], emy_y[i] + 80, j * 20, EMY_BULLET, 6, 0)
                        emy_count[i] = 2
                else:
                    emy_x[i] += emy_speed[i]
                    if emy_x[i] > 760:
                        for j in range(0, 10):
                            set_enemy(emy_x[i], emy_y[i] + 80, j * 20, EMY_BULLET, 6, 0)
                        emy_count[i] = 1
                if emy_shield[i] < 100 and tmr % 30 == 0:
                    set_enemy(emy_x[i], emy_y[i] + 80, random.randint(60, 120), EMY_BULLET, 6, 0)
            if emy_type[i] != EMY_BULLET:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w + h) / 4) + 12
                er = int((w + h) / 4)
                for n in range(MISSILE_MAX):
                    if msl_f[n] and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r * r:
                        msl_f[n] = False
                        set_effect(emy_x[i] + random.randint(-er, er), emy_y[i] + random.randint(-er, er))
                        if emy_type[i] == EMY_BOSS:
                            png = emy_type[i] + 1
                        emy_shield[i] -= 1
                        if emy_shield[i] <= 0:
                            emy_f[i] = False
                            if emy_type[i] != EMY_BOSS:
                                enemy_kill_count += 1
                                if enemy_kill_count >= 10 and ss_shield < 100:
                                    ss_shield = min(ss_shield + 1, 100)  # 적 10명 처치 시 쉴드 1 회복
                                    enemy_kill_count = 0
                                    # 대안 1: 처치 수 증가
                                    # if enemy_kill_count >= 15 and ss_shield < 100:
                                    #     ss_shield = min(ss_shield + 1, 100)
                                    #     enemy_kill_count = 0
                            if emy_type[i] == EMY_ZAKO:
                                score += random.randint(1, 5)
                            elif emy_type[i] == EMY_ZAKO + 1:
                                score += random.randint(6, 10)
                            elif emy_type[i] == EMY_ZAKO + 2:
                                score += random.randint(11, 15)
                            elif emy_type[i] == EMY_ZAKO + 3:
                                score += random.randint(16, 20)
                            elif emy_type[i] == EMY_BOSS:
                                score += 2000
                            if score > hisco:
                                hisco = score
                                new_record = True
                            if emy_type[i] == EMY_BOSS and idx == 1:
                                idx = 3
                                tmr = 0
                                for j in range(10):
                                    set_effect(emy_x[i] + random.randint(-er, er), emy_y[i] + random.randint(-er, er))
                                if se_explosion:
                                    se_explosion.play()
            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)
            scrn.blit(img_rz, [emy_x[i] - img_rz.get_width() / 2, emy_y[i] - img_rz.get_height() / 2])

def set_effect(x, y):
    global eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no + 1) % EFFECT_MAX

def draw_effect(scrn):
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            scrn.blit(img_explode[eff_p[i]], [eff_x[i] - 48, eff_y[i] - 48])
            eff_p[i] += 1
            if eff_p[i] == 6:
                eff_p[i] = 0

def main():
    global idx, tmr, score, new_record, bg_y, ss_x, ss_y, ss_d, ss_shield, ss_muteki, se_damage, se_explosion, se_shot
    pygame.init()
    pygame.display.set_caption("Galaxy Lancer")
    screen = pygame.display.set_mode((960, 720), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    try:
        se_damage = pygame.mixer.Sound(rsrc("sound_plane/damage.ogg"))
        se_explosion = pygame.mixer.Sound(rsrc("sound_plane/explosion.ogg"))
        se_shot = pygame.mixer.Sound(rsrc("sound_plane/shot.ogg"))
        pygame.mixer.music.load(rsrc("sound_plane/bgm.ogg"))
    except Exception as e:
        print(f"사운드 로드 오류: {e}")
    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.quit()
                pygame.font.quit()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.quit()
                    pygame.font.quit()
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.key == K_m:
                    pygame.mixer.quit()
                    pygame.font.quit()
                    pygame.display.quit()
                    pygame.quit()
                    try:
                        import subprocess
                        launcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../my_launcher.py'))
                        subprocess.Popen([sys.executable, launcher_path])
                        sys.exit()
                    except Exception as e:
                        print(f"런처 실행 오류: {e}")
                        sys.exit(1)
        bg_y = (bg_y + 16) % 720
        screen.blit(img_galaxy, [0, bg_y - 720])
        screen.blit(img_galaxy, [0, bg_y])
        key = pygame.key.get_pressed()
        if idx == 0:
            img_rz = pygame.transform.rotozoom(img_title[0], -tmr % 360, 1.0)
            screen.blit(img_rz, [480 - img_rz.get_width() / 2, 280 - img_rz.get_height() / 2])
            screen.blit(img_title[1], [70, 160])
            draw_text(screen, "Press [SPACE] to start!", 480, 600, 50, SILVER)
            if key[K_SPACE]:
                idx = 1
                tmr = 0
                score = 0
                new_record = False
                ss_x = 480
                ss_y = 600
                ss_d = 0
                ss_shield = 100
                ss_muteki = 0
                enemy_kill_count = 0
                for i in range(ENEMY_MAX):
                    emy_f[i] = False
                for i in range(MISSILE_MAX):
                    msl_f[i] = False
                try:
                    pygame.mixer.music.play(-1)
                except Exception as e:
                    print(f"BGM 재생 오류: {e}")
        if idx == 1:
            pygame.mouse.set_visible(False)
            move_starship(screen, key)
            move_missile(screen)
            bring_enemy()
            move_enemy(screen)
        else:
            pygame.mouse.set_visible(True)
        if idx in [2, 3]:
            if idx == 2:
                move_missile(screen)
                move_enemy(screen)
                pygame.mixer.music.stop()
                draw_text(screen, "GAME OVER", 480, 300, 80, RED)
                if new_record:
                    draw_text(screen, "NEW RECORD " + str(hisco), 480, 400, 60, CYAN)
            elif idx == 3:
                move_starship(screen, key)
                move_missile(screen)
                pygame.mixer.music.stop()
                draw_text(screen, "GAME CLEAR", 480, 300, 80, SILVER)
                if new_record:
                    draw_text(screen, "NEW RECORD " + str(hisco), 480, 400, 60, CYAN)
            pygame.display.update()
            if tmr >= 117:
                pygame.mixer.quit()
                pygame.font.quit()
                pygame.display.quit()
                pygame.quit()
                import tkinter as tk
                from tkinter import messagebox
                def send_to_server(name):
                    try:
                        import socket
                        HOST = '10.116.0.70' #10.116.0.70
                        PORT = 50007
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                            sock.settimeout(5)
                            sock.connect((HOST, PORT))
                            send_data = f"{name},plane,{score}"
                            sock.sendall(send_data.encode('utf-8'))
                    except Exception as e:
                        print(f"서버 전송 오류: {e}")
                        with open(os.path.join(resource_dir, "scores.txt"), "a") as f:
                            f.write(f"{name},plane,{score}\n")
                        messagebox.showerror("서버 오류", f"서버 전송 실패: {e}. 점수가 로컬에 저장됨.")
                def on_submit():
                    name = entry_name.get()
                    if not name:
                        messagebox.showerror("입력 오류", "학번 이름을 입력하세요.")
                        return
                    send_to_server(name)
                    root.destroy()
                    try:
                        import subprocess
                        launcher_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../my_launcher.py'))
                        subprocess.Popen([sys.executable, launcher_path])
                        sys.exit()
                    except Exception as e:
                        print(f"런처 실행 오류: {e}")
                        sys.exit(1)
                root = tk.Tk()
                root.title("GAME LAUNCHER - 기록 입력")
                root.configure(bg="#1e1e1e")
                root.attributes('-fullscreen', True)
                root.overrideredirect(True)
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                title = tk.Label(root, text="기록 전송", font=("malgungothic", int(screen_height*0.05), "bold"), fg="#00bfff", bg="#1e1e1e")
                title.pack(pady=(int(screen_height*0.08), int(screen_height*0.03)))
                info = tk.Label(root, text="학번 이름을 입력하세요.", font=("malgungothic", int(screen_height*0.03)), fg="#fff", bg="#1e1e1e")
                info.pack(pady=(0, int(screen_height*0.02)))
                entry_name = tk.Entry(root, font=("malgungothic", int(screen_height*0.04)), justify='center', fg="#fff", bg="#333", insertbackground="#fff", relief="flat")
                entry_name.pack(ipady=int(screen_height*0.015), ipadx=int(screen_width*0.05), pady=(0, int(screen_height*0.04)))
                def on_enter(e):
                    btn.config(bg="#00bfff", fg="#fff")
                def on_leave(e):
                    btn.config(bg="#323232", fg="#fff")
                btn = tk.Button(root, text="기록 입력", font=("malgungothic", int(screen_height*0.035), "bold"), bg="#323232", fg="#fff", activebackground="#00bfff", activeforeground="#fff", relief="flat", command=on_submit)
                btn.pack(ipady=int(screen_height*0.015), ipadx=int(screen_width*0.03))
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                entry_name.bind('<Return>', lambda event: on_submit())
                root.mainloop()
                return
        draw_effect(screen)
        draw_text(screen, "SCORE " + str(score), 200, 30, 50, SILVER)
        if idx != 0:
            screen.blit(img_shield, [40, 680])
            pygame.draw.rect(screen, (192, 0, 0), [40, 680, ss_shield * 4, 32])
            pygame.draw.rect(screen, (64, 32, 32), [40 + ss_shield * 4, 680, (100 - ss_shield) * 4, 32])
        font = pygame.font.Font(None, 28)
        text = 'Home "M"'
        txt_surface = font.render(text, True, (40, 40, 40))
        screen.blit(txt_surface, (960 - txt_surface.get_width() - 18, 720 - txt_surface.get_height() - 12))
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (960 - txt_surface.get_width() - 20, 720 - txt_surface.get_height() - 14))
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()

import pygame
import sys
import os
import subprocess

pygame.init()
pygame.font.init()

# 게임 목록 설정
games_root = os.path.join(os.path.dirname(__file__), "games")  # 현재 파일 기준 games 폴더
game_files = [
    ("2인 게임", os.path.join(games_root, "DuelOfRespect", "2play.py")),
    ("비행기 게임", os.path.join(games_root, "PLANEGAME", "fight_plane.py")),
    ("레이싱 게임", os.path.join(games_root, "RACE", "socket_race_client.py")),
]

GAMES_CONFIG = {name: path for name, path in game_files if os.path.exists(path)}

# ------------------------------------------------------------------
# 화면 설정: 전체화면(F11 모드)
# ------------------------------------------------------------------
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("🎮 게임 런처")

# 배경 이미지 로딩
bg_img = pygame.transform.scale(pygame.image.load("haha.png"), (WIDTH, HEIGHT))

# 색상 정의
BG_COLOR = (30, 30, 30)       # 어두운 배경
BTN_COLOR = (255, 220, 0)      # 버튼 기본
BTN_HOVER = (255, 204, 51)      # 버튼 호버
TEXT_COLOR = (255, 255, 255)  # 흰색
TITLE_COLOR = (0, 191, 255)   # Deep Sky Blue
STATUS_COLOR = (255, 255, 0)  # 노랑

# 폰트 설정
title_font = pygame.font.SysFont("malgungothic", 64, bold=True)
button_font = pygame.font.SysFont("malgungothic", 36, bold=True)
status_font = pygame.font.SysFont("malgungothic", 28, italic=True)

# 버튼 정보
buttons = []
btn_width, btn_height = 400, 80
gap = 30
start_y = HEIGHT // 3

for i, (game_name, path) in enumerate(GAMES_CONFIG.items()):
    x = (WIDTH - btn_width) // 2
    y = start_y + i * (btn_height + gap)
    rect = pygame.Rect(x, y, btn_width, btn_height)
    buttons.append((rect, game_name, path))

status_msg = "실행할 게임을 선택하세요."


def draw():
    WIN.blit(bg_img, (0, 0))

    # 타이틀
    title_surface = title_font.render("HOME", True, TITLE_COLOR)
    WIN.blit(title_surface, ((WIDTH - title_surface.get_width()) // 2, 80))

    # 버튼
    mouse_pos = pygame.mouse.get_pos()
    for rect, game_name, path in buttons:
        if rect.collidepoint(mouse_pos):
            color = BTN_HOVER
        else:
            color = BTN_COLOR
        pygame.draw.rect(WIN, color, rect, border_radius=15)
        text_surf = button_font.render(game_name, True, TEXT_COLOR)
        WIN.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2,
                             rect.y + (rect.height - text_surf.get_height()) // 2))

    # 상태 메시지
    status_surface = status_font.render(status_msg, True, STATUS_COLOR)
    WIN.blit(status_surface, ((WIDTH - status_surface.get_width()) // 2, HEIGHT - 100))

    pygame.display.update()


def run_game(path):
    try:
        subprocess.Popen([sys.executable, path])
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"게임 실행 오류: {e}")


# 메인 루프
running = True
while running:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # ESC로 종료
                running = False
            elif event.key == pygame.K_m:
                # M 키로 런처 재실행 (자기 자신이므로 무시)
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 클릭
                for rect, game_name, path in buttons:
                    if rect.collidepoint(event.pos):
                        status_msg = f"'{game_name}' 실행 중..."
                        run_game(path)

pygame.quit()
sys.exit()

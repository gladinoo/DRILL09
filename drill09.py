"""Drill #9: 소년 상하 좌우 이동 및 방향 바꾸기

요구사항:
1. 상하좌우 방향키를 이용한 소년 이동
2. IDLE 상태에서는 제자리 대기 애니메이션 재생
3. 이동 시 해당 방향 이동 애니메이션, 위아래 이동 시 기존 좌우 방향 유지
4. 화면 경계면(1280x1024)을 벗어나지 않도록 좌표 제한
"""

from pico2d import *

# 화면 및 캐릭터 규격 상수
TUK_WIDTH, TUK_HEIGHT = 1280, 1024
BOY_WIDTH, BOY_HEIGHT = 100, 100
BOY_SPEED = 5

open_canvas(TUK_WIDTH, TUK_HEIGHT)

# 리소스 로드
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

# 게임 상태 변수
running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x = 0
dir_y = 0
face_dir = 1  # 바라보는 방향: 1 = 오른쪽, -1 = 왼쪽


def handle_events():
    """키보드 및 윈도우 이벤트 처리"""
    global running, dir_x, dir_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1


def update():
    """소년의 위치 이동, 방향 갱신, 경계면 검사 및 프레임 갱신"""
    global x, y, frame, face_dir

    # 좌/우 이동 중일 때만 바라보는 방향 변경 (위/아래 이동 시에는 기존 방향 유지)
    if dir_x > 0:
        face_dir = 1
    elif dir_x < 0:
        face_dir = -1

    # 화면 경계를 벗어나지 않도록 좌표 제한 (1280x1024 캔버스 내부 유지)
    half_w = BOY_WIDTH // 2
    half_h = BOY_HEIGHT // 2
    x = clamp(half_w, x + dir_x * BOY_SPEED, TUK_WIDTH - half_w)
    y = clamp(half_h, y + dir_y * BOY_SPEED, TUK_HEIGHT - half_h)

    # 8개 프레임 순환
    frame = (frame + 1) % 8


def render():
    """배경 및 소년 스프라이트 애니메이션 렌더링"""
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    # 스프라이트 시트 행(row) 매핑:
    # row 3: 우측 IDLE / row 2: 좌측 IDLE / row 1: 우측 RUN / row 0: 좌측 RUN
    is_moving = (dir_x != 0 or dir_y != 0)
    if is_moving:
        row = 1 if face_dir == 1 else 0
    else:
        row = 3 if face_dir == 1 else 2

    character.clip_draw(frame * 100, row * 100, BOY_WIDTH, BOY_HEIGHT, x, y)
    update_canvas()


while running:
    handle_events()
    update()
    render()
    delay(0.05)

close_canvas()

from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x = 0
dir_y = 0
face_dir = 1  # 1: 우측, -1: 좌측


def handle_events():
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


while running:
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    # 이동 상태 및 방향에 따른 애니메이션 행(row) 결정
    is_moving = (dir_x != 0 or dir_y != 0)
    if is_moving:
        # RUN 상태: 우측 1, 좌측 0
        row = 1 if face_dir == 1 else 0
    else:
        # IDLE 상태: 우측 3, 좌측 2
        row = 3 if face_dir == 1 else 2

    character.clip_draw(frame * 100, row * 100, 100, 100, x, y)
    update_canvas()
    handle_events()

    # 좌/우 이동 중일 때만 바라보는 방향 변경 (위/아래 이동 시에는 기존 방향 유지)
    if dir_x > 0:
        face_dir = 1
    elif dir_x < 0:
        face_dir = -1

    # 화면 경계를 벗어나지 않도록 좌표 제한 (캐릭터 크기: 100x100)
    x = clamp(50, x + dir_x * 5, TUK_WIDTH - 50)
    y = clamp(50, y + dir_y * 5, TUK_HEIGHT - 50)

    frame = (frame + 1) % 8
    delay(0.05)

close_canvas()

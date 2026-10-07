from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
BOY_WIDTH, BOY_HEIGHT = 100, 100
BOY_SPEED = 5

open_canvas(TUK_WIDTH, TUK_HEIGHT)

tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x = 0
dir_y = 0
face_dir = 1  # 1: 오른쪽 바라봄, -1: 왼쪽 바라봄


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


def update():
    global x, y, frame, face_dir

    # 좌/우 이동 중일 때만 바라보는 방향 변경 (위/아래 이동 시에는 기존 방향 유지)
    if dir_x > 0:
        face_dir = 1
    elif dir_x < 0:
        face_dir = -1

    # 화면 경계를 벗어나지 않도록 좌표 제한
    half_w = BOY_WIDTH // 2
    half_h = BOY_HEIGHT // 2
    x = clamp(half_w, x + dir_x * BOY_SPEED, TUK_WIDTH - half_w)
    y = clamp(half_h, y + dir_y * BOY_SPEED, TUK_HEIGHT - half_h)

    frame = (frame + 1) % 8


def render():
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    # 이동 상태 및 방향에 따른 애니메이션 행(row) 결정
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

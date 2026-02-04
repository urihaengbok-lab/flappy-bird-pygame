import pygame
import random

# 초기화
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 32)

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BIRD_COLOR = (255, 200, 0)
PIPE_COLOR = (0, 200, 0)

# 새 설정
bird_x = 50
bird_y = HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.5
jump_power = -8

# 파이프 설정
pipe_width = 60
pipe_gap = 150
pipe_speed = 3
pipes = []

def create_pipe():
    top = random.randint(50, HEIGHT - pipe_gap - 50)
    return [WIDTH, top]

score = 0
running = True
game_over = False

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = jump_power
        if game_over and event.type == pygame.KEYDOWN:
            # 게임 리셋
            bird_y = HEIGHT // 2
            bird_velocity = 0
            pipes = []
            score = 0
            game_over = False

    if not game_over:
        # 새 물리
        bird_velocity += gravity
        bird_y += bird_velocity

        # 파이프 생성
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            pipes.append(create_pipe())

        # 파이프 이동 및 충돌 체크
        for pipe in pipes:
            pipe[0] -= pipe_speed
        pipes = [p for p in pipes if p[0] > -pipe_width]

        for pipe in pipes:
            # 파이프 그리기
            pygame.draw.rect(screen, PIPE_COLOR, (pipe[0], 0, pipe_width, pipe[1]))
            pygame.draw.rect(screen, PIPE_COLOR, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT - pipe[1] - pipe_gap))
            # 충돌 체크
            if bird_x + bird_radius > pipe[0] and bird_x - bird_radius < pipe[0] + pipe_width:
                if bird_y - bird_radius < pipe[1] or bird_y + bird_radius > pipe[1] + pipe_gap:
                    game_over = True
            # 점수 체크
            if pipe[0] + pipe_width < bird_x and not hasattr(pipe, 'scored'):
                score += 1
                pipe.append('scored')

        # 바닥, 천장 충돌 체크
        if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
            game_over = True

    # 새 그리기
    pygame.draw.circle(screen, BIRD_COLOR, (bird_x, int(bird_y)), bird_radius)

    # 점수 표시
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = FONT.render("Game Over! Press any key.", True, BLACK)
        screen.blit(over_text, (40, HEIGHT // 2 - 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

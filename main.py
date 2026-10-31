
import pygame
import random
import sys
import math

pygame.init()

# Window
WIDTH, HEIGHT = 640, 720
SIZE = 8
CELL = 70
BOARD_SIZE = CELL * SIZE
OX = (WIDTH - BOARD_SIZE) // 2
OY = 140

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("REVERSI AI")

clock = pygame.time.Clock()

WHITE = (245, 245, 245)
BLACK = (15, 15, 20)
GREEN = (8, 115, 78)
DARK = (12, 20, 28)
CYAN = (70, 245, 195)
GRAY = (150, 160, 170)

font = pygame.font.SysFont("Arial", 25)
bigfont = pygame.font.SysFont("Arial", 36, bold=True)

# Board
board = [[0 for _ in range(8)] for _ in range(8)]

board[3][3] = 2
board[3][4] = 1
board[4][3] = 1
board[4][4] = 2

player = 1
game_over = False
thinking = False
difficulty = "Medium"

DIRECTIONS = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),           (0,1),
    (1,-1),  (1,0),   (1,1)
]

WEIGHTS = [
    [100,-25,10,5,5,10,-25,100],
    [-25,-45,-5,-5,-5,-5,-45,-25],
    [10,-5,5,2,2,5,-5,10],
    [5,-5,2,1,1,2,-5,5],
    [5,-5,2,1,1,2,-5,5],
    [10,-5,5,2,2,5,-5,10],
    [-25,-45,-5,-5,-5,-5,-45,-25],
    [100,-25,10,5,5,10,-25,100]
]


def inside(r, c):
    return 0 <= r < 8 and 0 <= c < 8


def get_flips(b, r, c, p):
    if not inside(r, c) or b[r][c] != 0:
        return []

    result = []

    for dr, dc in DIRECTIONS:
        rr, cc = r + dr, c + dc
        line = []

        while inside(rr, cc) and b[rr][cc] == 3-p:
            line.append((rr, cc))
            rr += dr
            cc += dc

        if line and inside(rr, cc) and b[rr][cc] == p:
            result.extend(line)

    return result


def get_moves(b, p):
    moves = []

    for r in range(8):
        for c in range(8):
            flips = get_flips(b, r, c, p)

            if flips:
                moves.append((r, c, flips))

    return moves


def make_move(b, move, p):
    r, c, flips = move
    new = [row[:] for row in b]

    new[r][c] = p

    for rr, cc in flips:
        new[rr][cc] = p

    return new


def count(b, p):
    return sum(row.count(p) for row in b)


def evaluate(b):
    score = 0

    for r in range(8):
        for c in range(8):
            if b[r][c] == 2:
                score += WEIGHTS[r][c]
            elif b[r][c] == 1:
                score -= WEIGHTS[r][c]

    score += 8 * (
        len(get_moves(b, 2)) -
        len(get_moves(b, 1))
    )

    occupied = count(b, 1) + count(b, 2)

    if occupied > 45:
        score += 3 * (count(b, 2) - count(b, 1))

    return score


def minimax(b, depth, alpha, beta, p):
    available = get_moves(b, p)
    opponent = get_moves(b, 3-p)

    if depth == 0 or (not available and not opponent):
        return evaluate(b)

    if not available:
        return minimax(b, depth-1, alpha, beta, 3-p)

    if p == 2:
        best = -math.inf

        for move in available:
            value = minimax(
                make_move(b, move, p),
                depth-1, alpha, beta, 1
            )

            best = max(best, value)
            alpha = max(alpha, best)

            if beta <= alpha:
                break

        return best

    else:
        best = math.inf

        for move in available:
            value = minimax(
                make_move(b, move, p),
                depth-1, alpha, beta, 2
            )

            best = min(best, value)
            beta = min(beta, best)

            if beta <= alpha:
                break

        return best


def ai_move():
    available = get_moves(board, 2)

    if not available:
        return None

    if difficulty == "Easy":
        return random.choice(available)

    depth = 2 if difficulty == "Medium" else 4

    best = -math.inf
    choices = []

    for move in available:
        value = minimax(
            make_move(board, move, 2),
            depth-1,
            -math.inf,
            math.inf,
            1
        )

        if value > best:
            best = value
            choices = [move]

        elif value == best:
            choices.append(move)

    return random.choice(choices)


def draw_text(text, x, y, color=WHITE, f=font):
    image = f.render(text, True, color)
    screen.blit(image, (x, y))


def draw():
    screen.fill(DARK)

    draw_text("REVERSI AI", 220, 25, CYAN, bigfont)

    draw_text(
        f"YOU (BLACK): {count(board, 1)}",
        90, 85
    )

    draw_text(
        f"AI (WHITE): {count(board, 2)}",
        360, 85
    )

    legal = get_moves(board, 1) if player == 1 and not game_over else []

    for r in range(8):
        for c in range(8):
            x = OX + c * CELL
            y = OY + r * CELL

            pygame.draw.rect(
                screen, GREEN,
                (x, y, CELL-2, CELL-2)
            )

            if board[r][c] == 1:
                pygame.draw.circle(
                    screen, BLACK,
                    (x+CELL//2, y+CELL//2),
                    CELL//2-7
                )

            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen, WHITE,
                    (x+CELL//2, y+CELL//2),
                    CELL//2-7
                )

            if any(m[0] == r and m[1] == c for m in legal):
                pygame.draw.circle(
                    screen, CYAN,
                    (x+CELL//2, y+CELL//2),
                    6
                )

    if game_over:
        a, b = count(board, 1), count(board, 2)

        result = (
            "YOU WIN!" if a > b else
            "AI WINS!" if b > a else
            "DRAW!"
        )

        draw_text(result, 255, 720-100, CYAN, bigfont)

    elif thinking:
        draw_text("AI THINKING...", 235, 720-100, CYAN)

    else:
        draw_text(
            "YOUR TURN" if player == 1 else "AI TURN",
            250, 720-100, CYAN
        )

    draw_text(
        f"Difficulty: {difficulty}",
        25, 720-45, GRAY
    )

    draw_text(
        "R: Restart    1: Easy    2: Medium    3: Hard",
        25, 720-20, GRAY
    )

    pygame.display.flip()


def advance_turn():
    global player, game_over, thinking

    if not get_moves(board, player):
        if not get_moves(board, 3-player):
            game_over = True
            thinking = False
            return

        player = 3-player

    if player == 2:
        thinking = True
    else:
        thinking = False


def restart():
    global board, player, game_over, thinking

    board = [[0 for _ in range(8)] for _ in range(8)]
    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2

    player = 1
    game_over = False
    thinking = False


# Main loop
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                restart()

            elif event.key == pygame.K_1:
                difficulty = "Easy"

            elif event.key == pygame.K_2:
                difficulty = "Medium"

            elif event.key == pygame.K_3:
                difficulty = "Hard"

        if event.type == pygame.MOUSEBUTTONDOWN:

            if player == 1 and not game_over and not thinking:
                mx, my = event.pos

                c = (mx-OX)//CELL
                r = (my-OY)//CELL

                if inside(r, c):
                    move = next(
                        (
                            m for m in get_moves(board, 1)
                            if m[0] == r and m[1] == c
                        ),
                        None
                    )

                    if move:
                        board = make_move(board, move, 1)
                        player = 2
                        advance_turn()

    if thinking and not game_over:
        move = ai_move()

        if move:
            board = make_move(board, move, 2)

        player = 1
        advance_turn()

    draw()
    clock.tick(60)

pygame.quit()
sys.exit()

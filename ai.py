import math
import random

BLACK = 1
WHITE = 2

board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        # 相手の石を挟めるかどうかチェック
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if board[ny][nx] == opponent:
                found_opponent = True
                nx += dx
                ny += dy
            else:
                break

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if board[ny][nx] == stone:
                return True

    return False

def simulate_board(board, stone, x, y):
    new_board = [row[:] for row in board]
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    # 実際に石を置く
    new_board[y][x] = stone

    # 挟めるところをひっくり返す
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flip_positions = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
            if new_board[ny][nx] == opponent:
                flip_positions.append((nx, ny))
            elif new_board[ny][nx] == stone:
                # 相手の石をひっくり返す
                for fx, fy in flip_positions:
                    new_board[fy][fx] = stone
                break
            else:
                break

            nx += dx
            ny += dy

    return new_board

SCORE_MAP = [
    [100, -20,  10,  10, -20, 100],
    [-20, -50,   1,   1, -50, -20],
    [ 10,   1,   5,   5,   1,  10],
    [ 10,   1,   5,   5,   1,  10],
    [-20, -50,   1,   1, -50, -20],
    [100, -20,  10,  10, -20, 100],
]

def evaluate_board_by_position(board, stone):
    score = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += SCORE_MAP[y][x]
            elif board[y][x] == (3 - stone):
                score -= SCORE_MAP[y][x]
    return score

def count_stable_discs(board, stone):
    """単純化した安定石判定（実際はもっと複雑なケースがある）"""
    stable_count = 0
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]

    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                is_stable = True
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                        if board[ny][nx] != stone:
                            is_stable = False
                            break
                        nx += dx
                        ny += dy
                    if not is_stable:
                        break
                if is_stable:
                    stable_count += 1
    return stable_count

def calculate_mobility(board, stone):
    mobility = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                mobility += 1
    return mobility

def count_stones(board, stone):
    return sum(row.count(stone) for row in board)

def evaluate_board(board, stone, game_stage):
    """ゲームの進行度に応じた評価関数"""
    if game_stage == "early":
        # 序盤は位置や手数の多さを重視
        return (
            evaluate_board_by_position(board, stone) * 10 +
            calculate_mobility(board, stone) * 5
        )
    elif game_stage == "late":
        # 終盤は安定石数や石数そのものを重視
        return (
            count_stable_discs(board, stone) * 10 +
            count_stones(board, stone) * 5
        )

def evaluate_future(board, stone, depth, alpha=-math.inf, beta=math.inf):
    """ネガアルファ法によるミニマックス検索"""
    if depth == 0:
        return evaluate_board(board, stone, "late")

    opponent = 3 - stone

    # すべての配置可能手を試す
    placed = False
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                placed = True
                new_board = simulate_board(board, stone, x, y)
                score = -evaluate_future(new_board, opponent, depth - 1, -beta, -alpha)
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    return alpha
    # 置ける場所が一切ない場合はパスして次へ
    if not placed:
        return -evaluate_future(board, opponent, depth - 1, -beta, -alpha)

    return alpha

def improved_place(board, stone):
    """置き場所の中で最も評価値が高い手を返す"""
    best_score = -math.inf
    best_move = None

    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                new_board = simulate_board(board, stone, x, y)
                # 相手番でのスコアを負にして比較（ネガアルファ）
                score = -evaluate_future(new_board, 3 - stone, depth=5)
                if score > best_score:
                    best_score = score
                    best_move = (x, y)

    return best_move

class macaronAI:
    def face(self):
        return "🍬"

    def place(self, board, stone):
        # クラス内の can_place メソッドを使う
        if not self.can_place(board, stone):
            print("No valid moves available. Passing turn.")
            return  # パス

        x, y = improved_place(board, stone)
        return x, y

    def can_place(self, board, stone):
        """石を置ける場所があるか判定"""
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    return True
        return False

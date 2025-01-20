import math
import time
import hashlib

BLACK = 1
WHITE = 2

class macaronAI:
    def __init__(self):
        # 反復深化の最大深度
        self.MAX_DEPTH = 7
        # 反復深化にかける最大思考時間 [秒]
        self.TIME_LIMIT = 5.0
        # 置換表（探索済みの盤面を保存）
        self.transposition_table = {}

    def face(self):
        return "🍬"

    # -----------------------------------------
    # 盤面をハッシュ化 (置換表用)
    # -----------------------------------------
    def hash_board(self, board):
        return hashlib.md5(str(board).encode()).hexdigest()

    # -----------------------------------------
    # (x, y) に石を置けるか判定
    # -----------------------------------------
    def can_place_x_y(self, board, stone, x, y):
        if board[y][x] != 0:
            return False
        opponent = 3 - stone
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                if board[ny][nx] == opponent:
                    found_opponent = True
                    nx += dx
                    ny += dy
                else:
                    break
            if found_opponent:
                if 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                    if board[ny][nx] == stone:
                        return True
        return False

    # -----------------------------------------
    # 盤面のどこかに石を置ける場所があるか判定
    # -----------------------------------------
    def can_place(self, board, stone):
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    return True
        return False

    # -----------------------------------------
    # (x, y) に石を置いた盤面を返す
    # -----------------------------------------
    def simulate_board(self, board, stone, x, y):
        new_board = [row[:] for row in board]
        new_board[y][x] = stone
        opponent = 3 - stone

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            flip_positions = []
            while 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board):
                if new_board[ny][nx] == opponent:
                    flip_positions.append((nx, ny))
                    nx += dx
                    ny += dy
                elif new_board[ny][nx] == stone:
                    for fx, fy in flip_positions:
                        new_board[fy][fx] = stone
                    break
                else:
                    break
        return new_board

    # -----------------------------------------
    # 評価関数 (X-square, C-square を考慮)
    # -----------------------------------------
    POSITION_MAP = [
        [100, -20,  10,  10, -20, 100],
        [-20, -50,   1,   1, -50, -20],
        [ 10,   1,   5,   5,   1,  10],
        [ 10,   1,   5,   5,   1,  10],
        [-20, -50,   1,   1, -50, -20],
        [100, -20,  10,  10, -20, 100],
    ]

    def evaluate(self, board, stone):
        score = 0
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += self.POSITION_MAP[y][x]
                elif board[y][x] == (3 - stone):
                    score -= self.POSITION_MAP[y][x]
        return score

    # -----------------------------------------
    # ネガスコア(negamax)によるαβ探索
    # -----------------------------------------
    def negamax(self, board, stone, depth, alpha, beta):
        board_hash = self.hash_board(board)
        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash]

        if depth == 0 or not self.can_place(board, stone):
            return self.evaluate(board, stone)

        best_score = -math.inf
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    new_board = self.simulate_board(board, stone, x, y)
                    score = -self.negamax(new_board, 3 - stone, depth - 1, -beta, -alpha)
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break  # 枝刈り
        self.transposition_table[board_hash] = best_score
        return best_score

    # -----------------------------------------
    # 反復深化
    # -----------------------------------------
    def iterative_deepening(self, board, stone):
        best_move = None
        start_time = time.time()

        for depth in range(1, self.MAX_DEPTH + 1):
            if time.time() - start_time > self.TIME_LIMIT:
                break

            best_score = -math.inf
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if self.can_place_x_y(board, stone, x, y):
                        new_board = self.simulate_board(board, stone, x, y)
                        score = -self.negamax(new_board, 3 - stone, depth - 1, -math.inf, math.inf)
                        if score > best_score:
                            best_score = score
                            best_move = (x, y)

        return best_move

    # -----------------------------------------
    # 石を置く手を決定 (エントリーポイント)
    # -----------------------------------------
    def place(self, board, stone):
        if not self.can_place(board, stone):
            print("No valid moves available. Passing turn.")
            return
        return self.iterative_deepening(board, stone)


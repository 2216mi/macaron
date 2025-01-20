import math
import time

BLACK = 1
WHITE = 2

class macaronAI:
    def __init__(self):
        # 反復深化の最大深度（必要に応じて調整）
        self.MAX_DEPTH = 8
        # 反復深化にかける最大思考時間 [秒]
        self.TIME_LIMIT = 5.0

    def face(self):
        return "🍬"

    # -----------------------------------------
    # 盤面をコピーする便利関数
    # -----------------------------------------
    def copy_board(self, board):
        return [row[:] for row in board]

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
        new_board = self.copy_board(board)
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
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                if new_board[ny][nx] == opponent:
                    flip_positions.append((nx, ny))
                    nx += dx
                    ny += dy
                elif new_board[ny][nx] == stone:
                    # 挟んだ相手の石をすべてひっくり返す
                    for fx, fy in flip_positions:
                        new_board[fy][fx] = stone
                    break
                else:
                    break
        return new_board

    # -----------------------------------------
    # 評価の補助関数群
    # -----------------------------------------

    # 位置評価用マップ(6×6)
    POSITION_MAP = [
        [100, -20,  10,  10, -20, 100],
        [-20, -50,   1,   1, -50, -20],
        [ 10,   1,   5,   5,   1,  10],
        [ 10,   1,   5,   5,   1,  10],
        [-20, -50,   1,   1, -50, -20],
        [100, -20,  10,  10, -20, 100],
    ]

    def count_empty_cells(self, board):
        """空きマス数"""
        return sum(row.count(0) for row in board)

    def get_position_score(self, board, stone):
        """単純な位置スコア計算 (POSITION_MAP を使用)"""
        score = 0
        opponent = 3 - stone
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += self.POSITION_MAP[y][x]
                elif board[y][x] == opponent:
                    score -= self.POSITION_MAP[y][x]
        return score

    def get_mobility_score(self, board, stone):
        """モビリティ(手数)の差 [自分 - 相手]"""
        my_moves = 0
        op_moves = 0
        opponent = 3 - stone
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    my_moves += 1
                if self.can_place_x_y(board, opponent, x, y):
                    op_moves += 1
        return (my_moves - op_moves) * 5

    def get_stone_diff_score(self, board, stone):
        """石数の差 [自分 - 相手]"""
        my_stones = 0
        op_stones = 0
        opponent = 3 - stone
        for row in board:
            for cell in row:
                if cell == stone:
                    my_stones += 1
                elif cell == opponent:
                    op_stones += 1
        return (my_stones - op_stones) * 2

    def get_stable_corners(self, board, stone):
        """
        コーナーにある自分の石を簡易的に安定石とみなす(1個につき+10)。
        本来はもっと複雑な安定石判定が必要だが、例として簡単に実装。
        """
        corners = [(0,0), (0,5), (5,0), (5,5)]
        stable = 0
        for (cx, cy) in corners:
            if board[cy][cx] == stone:
                stable += 10
        return stable

    def evaluate(self, board, stone):
        """
        空きマス数に応じて評価のウェイトを変える。
        [序盤] 位置評価 + モビリティ
        [中盤] 位置評価 + モビリティ + コーナー安定石
        [終盤] コーナー安定石 + 石数差
        """
        empty = self.count_empty_cells(board)
        # 大まかに3段階に分ける
        if empty > 20:
            # 序盤
            return self.get_position_score(board, stone) \



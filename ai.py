import math

BLACK = 1
WHITE = 2

SCORE_MAP = [
    [100, -20,  10,  10, -20, 100],
    [-20, -50,   1,   1, -50, -20],
    [ 10,   1,   5,   5,   1,  10],
    [ 10,   1,   5,   5,   1,  10],
    [-20, -50,   1,   1, -50, -20],
    [100, -20,  10,  10, -20, 100],
]

class macaronAI:
    def __init__(self):
        pass

    def face(self):
        return "🍬"

    # ------------------------------------------------------
    # 石が置けるかどうか判定するメソッド
    # ------------------------------------------------------
    def can_place_x_y(self, board, stone, x, y):
        """(x, y) に stone を置けるかどうか判定"""
        if board[y][x] != 0:
            return False  # 既に石がある場合

        opponent = 3 - stone
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        # 8方向のどこかで相手の石をはさんで自分の石に到達できればOK
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

            if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                if board[ny][nx] == stone:
                    return True

        return False

    def can_place(self, board, stone):
        """盤上のどこかに石を置ける場所があるか判定"""
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    return True
        return False

    # ------------------------------------------------------
    # 石を置いたときの盤面を返すメソッド
    # ------------------------------------------------------
    def simulate_board(self, board, stone, x, y):
        """(x, y) に stone を置いてひっくり返したあとの新しい盤を返す"""
        new_board = [row[:] for row in board]
        new_board[y][x] = stone
        opponent = 3 - stone

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dx, dy in directions:
            flip_positions = []
            nx, ny = x + dx, y + dy
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                if new_board[ny][nx] == opponent:
                    flip_positions.append((nx, ny))
                elif new_board[ny][nx] == stone:
                    # 挟んでいる相手の石をすべてひっくり返す
                    for fx, fy in flip_positions:
                        new_board[fy][fx] = stone
                    break
                else:
                    break
                nx += dx
                ny += dy

        return new_board

    # ------------------------------------------------------
    # 評価関数
    # ------------------------------------------------------
    def evaluate_board(self, board, stone):
        """単純に SCORE_MAP に基づいてスコアを計算する例"""
        score = 0
        opponent = 3 - stone
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += SCORE_MAP[y][x]
                elif board[y][x] == opponent:
                    score -= SCORE_MAP[y][x]
        return score

    # ------------------------------------------------------
    # ミニマックス＋αβ法 (再帰)
    # ------------------------------------------------------
    def minimax(self, board, stone, depth, maximizing, alpha, beta):
        """
        depth: 検索の深さ
        maximizing: True なら自分の最大化フェーズ、Falseなら相手の最大化フェーズ
        alpha, beta: α-βカットの値
        """
        if depth == 0:
            # 評価値を返す
            return self.evaluate_board(board, stone)

        moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    moves.append((x, y))

        # 置ける手がない場合はパス
        if not moves:
            # 相手に交代して次の深さを検索
            return self.minimax(board, 3 - stone, depth - 1, not maximizing, alpha, beta)

        if maximizing:
            value = -math.inf
            for (x, y) in moves:
                new_board = self.simulate_board(board, stone, x, y)
                # 相手の番で minimax 再帰
                score = self.minimax(new_board, 3 - stone, depth - 1, False, alpha, beta)
                value = max(value, score)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for (x, y) in moves:
                new_board = self.simulate_board(board, stone, x, y)
                # 相手の番で minimax 再帰
                score = self.minimax(new_board, 3 - stone, depth - 1, True, alpha, beta)
                value = min(value, score)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    # ------------------------------------------------------
    # 実際に石を置く手を決定するメソッド
    # ------------------------------------------------------
    def place(self, board, stone):
        """思考ルーチンの入口。ここで最終的に (x, y) を返す。"""
        # 置ける手がない場合はパス
        if not self.can_place(board, stone):
            print("No valid moves available. Passing turn.")
            return

        best_score = -math.inf
        best_move = None
        depth = 3  # 探索の深さ（例として 3 に設定）

        # すべての置ける手を試して最大スコアを選ぶ
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    new_board = self.simulate_board(board, stone, x, y)
                    # minimax で相手ターンを評価
                    score = self.minimax(new_board, 3 - stone, depth - 1,
                                         maximizing=False,
                                         alpha=-math.inf, beta=math.inf)
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        if best_move is None:
            # 理論上起きにくいが、一応置ける手がない(二重パス)ならパス
            return

        return best_move


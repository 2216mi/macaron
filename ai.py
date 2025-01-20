import math

BLACK = 1
WHITE = 2

class macaronAI:
    def __init__(self):
        pass

    def face(self):
        return "🍬"

    # -----------------------------------------
    # 盤面をコピーする便利関数
    # -----------------------------------------
    def copy_board(self, board):
        return [row[:] for row in board]

    # -----------------------------------------
    # (x, y)に石を置けるか判定する
    # -----------------------------------------
    def can_place_x_y(self, board, stone, x, y):
        """(x, y) に stone を置けるかどうか"""
        # 既に石がある
        if board[y][x] != 0:
            return False

        opponent = 3 - stone
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            has_opponent = False

            # 相手の石が連続するか探す
            while 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                if board[ny][nx] == opponent:
                    has_opponent = True
                    nx += dx
                    ny += dy
                else:
                    break

            # 一度でも相手の石を見つけ、最後に自分の石があるか
            if has_opponent:
                if 0 <= nx < len(board[0]) and 0 <= ny < len(board):
                    if board[ny][nx] == stone:
                        return True

        return False

    # -----------------------------------------
    # 盤面のどこかに石を置ける場所があるか判定
    # -----------------------------------------
    def can_place(self, board, stone):
        """stone を置ける場所が1つでもあるか"""
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    return True
        return False

    # -----------------------------------------
    # (x, y) に石を置いたときの盤面を返す
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

            while 0 <= nx < len(new_board[0]) and 0 <= ny < len(new_board):
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
    # 初歩的な評価関数 (SCORE_MAP)
    # -----------------------------------------
    SCORE_MAP = [
        [100, -20,  10,  10, -20, 100],
        [-20, -50,   1,   1, -50, -20],
        [ 10,   1,   5,   5,   1,  10],
        [ 10,   1,   5,   5,   1,  10],
        [-20, -50,   1,   1, -50, -20],
        [100, -20,  10,  10, -20, 100],
    ]

    def evaluate_board(self, board, stone):
        """シンプルに SCORE_MAP に基づく評価"""
        score = 0
        opponent = 3 - stone
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == stone:
                    score += self.SCORE_MAP[y][x]
                elif board[y][x] == opponent:
                    score -= self.SCORE_MAP[y][x]
        return score

    # -----------------------------------------
    # ミニマックス(αβ法)
    # -----------------------------------------
    def minimax(self, board, stone, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.evaluate_board(board, stone)

        moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    moves.append((x, y))

        # パス判定（置ける場所がない）
        if not moves:
            # 相手に手番を渡して、深さを1減らす
            return self.minimax(board, 3 - stone, depth - 1, alpha, beta, not maximizing)

        if maximizing:
            value = -math.inf
            for (mx, my) in moves:
                new_board = self.simulate_board(board, stone, mx, my)
                # 相手ターンを評価
                score = self.minimax(new_board, 3 - stone, depth - 1, alpha, beta, False)
                value = max(value, score)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for (mx, my) in moves:
                new_board = self.simulate_board(board, stone, mx, my)
                # 相手ターンを評価
                score = self.minimax(new_board, 3 - stone, depth - 1, alpha, beta, True)
                value = min(value, score)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    # -----------------------------------------
    # 実際に石を置く手を決定する
    # -----------------------------------------
    def place(self, board, stone):
        """思考ルーチン入口。ここで(x, y)を返す。"""
        # 置ける手がないならパス
        if not self.can_place(board, stone):
            print("No valid moves available. Passing turn.")
            return

        best_score = -math.inf
        best_move = None
        depth = 3  # 探索深さ(例)

        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    # その手を打った場合の盤面
                    new_board = self.simulate_board(board, stone, x, y)
                    # minimax で相手番を評価
                    score = self.minimax(
                        board=new_board,
                        stone=3 - stone,
                        depth=depth - 1,
                        alpha=-math.inf,
                        beta=math.inf,
                        maximizing=False
                    )
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        return best_move


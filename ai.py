import math

BLACK = 1
WHITE = 2

class macaronAI:
    def __init__(self):
        pass

    def face(self):
        return "🍬"

    def copy_board(self, board):
        return [row[:] for row in board]

    # (x, y)に石を置けるか判定
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

    # 石を置ける場所があるか
    def can_place(self, board, stone):
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    return True
        return False

    # (x, y) に石を置いた盤面を返す
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
                    for fx, fy in flip_positions:
                        new_board[fy][fx] = stone
                    break
                else:
                    break

        return new_board

    # -----------------------------------------------
    # 評価の補助関数いくつか定義
    # -----------------------------------------------

    # 位置評価用マップ(6×6)
    POSITION_MAP = [
        [100, -20,  10,  10, -20, 100],
        [-20, -50,   1,   1, -50, -20],
        [ 10,   1,   5,   5,   1,  10],
        [ 10,   1,   5,   5,   1,  10],
        [-20, -50,   1,   1, -50, -20],
        [100, -20,  10,  10, -20, 100],
    ]

    def get_position_score(self, board, stone):
        """POSITION_MAP に基づいてスコアを計算"""
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
        """モビリティ (置ける手数の差)"""
        my_moves = 0
        op_moves = 0
        opponent = 3 - stone

        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    my_moves += 1
                if self.can_place_x_y(board, opponent, x, y):
                    op_moves += 1
        # 自分 - 相手 の差
        return (my_moves - op_moves) * 5

    def get_stable_discs(self, board, stone):
        """
        簡易的な安定石数を数える。
        本来はもっと複雑な判定が必要だが、ここでは簡単に上下左右端にくっついている連続石などを
        調べる程度に留める(例として)。
        """
        stable = 0
        # 端にある自分の石で、周囲(端の方向)がすべて自分の石なら安定とみなす…などの簡易実装
        # ここでは厳密な実装はせず、例として corners, edges を優遇するイメージ
        # コーナーにある自分の石を+10点
        corners = [(0, 0), (0, 5), (5, 0), (5, 5)]
        for (cx, cy) in corners:
            if board[cy][cx] == stone:
                stable += 10

        return stable

    def get_stone_count_score(self, board, stone):
        """盤上の石数の差"""
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

    def count_empty_cells(self, board):
        """空きマスの数"""
        empty = 0
        for row in board:
            empty += row.count(0)
        return empty

    def evaluate(self, board, stone):
        """
        盤面評価を複合的に行う。
        残り空きマス数に応じて序盤・中盤・終盤でウェイトを変えてみる例。
        """
        empty_cells = self.count_empty_cells(board)
        # 大雑把なステージ判定
        if empty_cells > 20:
            # 序盤：位置評価、モビリティをやや重視
            pos_score = self.get_position_score(board, stone)
            mob_score = self.get_mobility_score(board, stone)
            return pos_score + mob_score
        elif empty_cells > 10:
            # 中盤：位置評価 + モビリティ + 安定石
            pos_score = self.get_position_score(board, stone)
            mob_score = self.get_mobility_score(board, stone)
            stable_score = self.get_stable_discs(board, stone) * 5
            return pos_score + mob_score + stable_score
        else:
            # 終盤：安定石 + 石数差 を重視
            stable_score = self.get_stable_discs(board, stone) * 8
            stone_score = self.get_stone_count_score(board, stone) * 2
            return stable_score + stone_score

    # -----------------------------------------------
    # ミニマックス(αβ法)
    # -----------------------------------------------
    def minimax(self, board, stone, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.evaluate(board, stone)

        moves = []
        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    moves.append((x, y))

        # パス判定（置ける場所がない）
        if not moves:
            # 相手に手番を渡して深さを1減らす
            return self.minimax(board, 3 - stone, depth - 1, alpha, beta, not maximizing)

        if maximizing:
            value = -math.inf
            for (mx, my) in moves:
                new_board = self.simulate_board(board, stone, mx, my)
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
                score = self.minimax(new_board, 3 - stone, depth - 1, alpha, beta, True)
                value = min(value, score)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    # -----------------------------------------------
    # 実際に石を置く手を決定する
    # -----------------------------------------------
    def place(self, board, stone):
        """思考ルーチン入口。ここで(x, y)を返す。"""
        # 置ける手がないならパス
        if not self.can_place(board, stone):
            print("No valid moves available. Passing turn.")
            return

        best_score = -math.inf
        best_move = None
        # 探索深さを少し上げる (6×6なら4~6程度にしても試せる)
        depth = 5

        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    new_board = self.simulate_board(board, stone, x, y)
                    # 相手番として評価
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


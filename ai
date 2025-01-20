import random
import copy

BLACK = 1
WHITE = 2

class macaronAI:
    def face(self):
        """ AI の顔文字を返す """
        return "🍬"

    def place(self, board, stone):
        """ AI が最適な手を選ぶ """
        empty_cells = sum(row.count(0) for row in board)

        if empty_cells <= 10:
            # 終盤はミニマックス法で最適な手を選ぶ
            return self.best_move_minimax(board, stone, depth=4)

        # 通常の手選び（リスク管理付き）
        return self.best_place_with_risk_management(board, stone)

    def best_place_with_risk_management(self, board, stone):
        """ リスク管理付きの最適な手を選ぶ """
        corners = [(0, 0), (0, 5), (5, 0), (5, 5)]
        x_squares = [(0, 1), (1, 0), (1, 1), (0, 4), (1, 5), (1, 4),
                     (4, 0), (5, 1), (4, 1), (4, 5), (5, 4), (4, 4)]

        best_score = -float('inf')
        best_move = None

        for y in range(len(board)):
            for x in range(len(board[0])):
                if not self.can_place_x_y(board, stone, x, y):
                    continue

                if (x, y) in corners:
                    return (x, y)  # 角は最優先

                score = self.count_flippable_stones(board, stone, x, y)

                if (x, y) in x_squares:
                    score -= 100  # X-square は避ける

                if score > best_score:
                    best_score = score
                    best_move = (x, y)

        return best_move

    def best_move_minimax(self, board, stone, depth=4):
        """ ミニマックス法 + アルファベータ枝刈りで最適な手を選ぶ """
        opponent = 3 - stone
        best_move = None
        best_score = -float('inf')

        for y in range(len(board)):
            for x in range(len(board[0])):
                if self.can_place_x_y(board, stone, x, y):
                    new_board = self.make_move(board, stone, x, y)
                    eval = self.minimax(new_board, opponent, depth - 1, False, float('-inf'), float('inf'))
                    if eval > best_score:
                        best_score = eval
                        best_move = (x, y)

        return best_move

    def minimax(self, board, stone, depth, maximizing, alpha, beta):
        """ ミニマックス法 + アルファベータ枝刈り """
        opponent = 3 - stone

        if depth == 0 or not self.can_place(board, stone) and not self.can_place(board, opponent):
            return self.evaluate_board(board, stone)

        if maximizing:
            max_eval = -float('inf')
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if self.can_place_x_y(board, stone, x, y):
                        new_board = self.make_move(board, stone, x, y)
                        eval = self.minimax(new_board, opponent, depth - 1, False, alpha, beta)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for y in range(len(board)):
                for x in range(len(board[0])):
                    if self.can_place_x_y(board, opponent, x, y):
                        new_board = self.make_move(board, opponent, x, y)
                        eval = self.minimax(new_board, stone, depth - 1, True, alpha, beta)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def count_flippable_stones(self, board, stone, x, y):
        """ 置いた時にひっくり返せる石の数を計算 """
        if board[y][x] != 0:
            return 0

        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        total_flipped = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            flipped = 0

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                flipped += 1
                nx += dx
                ny += dy

            if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                total_flipped += flipped

        return total_flipped

    def can_place_x_y(self, board, stone, x, y):
        """ (x, y) に石を置けるかチェック """
        if board[y][x] != 0:
            return False

        opponent = 3 - stone
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False

            while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
                found_opponent = True
                nx += dx
                ny += dy

            if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
                return True

        return False

    def make_move(self, board, stone, x, y):
        """ 石を置く """
        new_board = [row[:] for row in board]
        new_board[y][x] = stone
        return new_board

    def evaluate_board(self, board, stone):
        """ 盤面評価 """
        score = sum(row.count(stone) - row.count(3 - stone) for row in board)
        return score

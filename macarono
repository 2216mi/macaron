import random
import copy

class macaron:
    def __init__(self, color):
        self.color = color  # 1 for black, -1 for white
    
    def get_move(self, board):
        """
        攻略型AI: ミニマックス法 + アルファベータ枝刈り + 盤面評価
        """
        valid_moves = self.get_valid_moves(board)
        if not valid_moves:
            return None
        
        best_move = None
        best_score = float('-inf')
        
        for move in valid_moves:
            new_board = self.make_move(copy.deepcopy(board), move)
            score = self.minimax(new_board, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing=False)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def minimax(self, board, depth, alpha, beta, maximizing):
        """
        ミニマックス法 + アルファベータ枝刈り
        """
        if depth == 0:
            return self.evaluate_board(board)
        
        valid_moves = self.get_valid_moves(board)
        if not valid_moves:
            return self.evaluate_board(board)
        
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = self.make_move(copy.deepcopy(board), move)
                eval = self.minimax(new_board, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = self.make_move(copy.deepcopy(board), move)
                eval = self.minimax(new_board, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def get_valid_moves(self, board):
        """
        盤面上の有効な手をリストで返す
        """
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(board, row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def is_valid_move(self, board, row, col):
        """
        与えられた位置 (row, col) が有効な手かどうかを判定
        """
        if board[row][col] != 0:
            return False
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in directions:
            if self.check_direction(board, row, col, dr, dc):
                return True
        return False
    
    def check_direction(self, board, row, col, dr, dc):
        """
        ある方向に相手の石が挟めるか確認
        """
        x, y = row + dr, col + dc
        opponent = -self.color
        found_opponent = False
        while 0 <= x < 8 and 0 <= y < 8:
            if board[x][y] == opponent:
                found_opponent = True
            elif board[x][y] == self.color:
                return found_opponent
            else:
                return False
            x += dr
            y += dc
        return False
    
    def make_move(self, board, move):
        """
        指定された手を盤面に適用
        """
        row, col = move
        board[row][col] = self.color
        return board
    
    def evaluate_board(self, board):
        """
        盤面評価: 角を優先し、相手の手数を減らす
        """
        score = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == self.color:
                    score += self.get_position_value(row, col)
        return score
    
    def get_position_value(self, row, col):
        """
        盤面の重要度を考慮したスコア
        """
        corner_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
        if (row, col) in corner_positions:
            return 10  # 角を取るのは非常に有利
        return 1  # 通常のマスは1点

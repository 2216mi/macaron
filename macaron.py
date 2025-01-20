import random
import copy

class macaron:
    def __init__(self):
        self.color = None  # `play_othello(macaron())` の形式に対応するため

    def set_color(self, color):
        """ play_othello() の中で、AIの色（黒 or 白）をセットする """
        self.color = color

    def get_move(self, board):
        """ AI の手を決定する（簡単なランダムロジック）"""
        valid_moves = self.get_valid_moves(board)
        return random.choice(valid_moves) if valid_moves else None  # ランダムな合法手を選択

    def get_valid_moves(self, board):
        """ 盤面上の合法手を取得 """
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(board, row, col):
                    valid_moves.append((row, col))
        return valid_moves

    def is_valid_move(self, board, row, col):
        """ 与えられた位置 (row, col) が有効な手かどうかを判定 """
        if board[row][col] != 0:
            return False
        return True  # シンプルなロジック（強化可能）


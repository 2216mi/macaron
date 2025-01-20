# まず、修正した macaron クラスを定義する
import random
import copy

class macaron:
    def __init__(self):
        self.color = None  # 初期値を None にする

    def set_color(self, color):
        """ play_othello() の中で、AI の色（黒 or 白）をセットする """
        self.color = color

    def get_move(self, board):
        """ AI の手を決定する（ランダム）"""
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

# ダミーの play_othello() 関数を定義してテストする
def play_othello(ai1, ai2):
    """
    簡易版のオセロ対戦関数。エラーが出ないか確認するためのテスト
    """
    board = [[0] * 8 for _ in range(8)]
    board[3][3], board[3][4], board[4][3], board[4][4] = -1, 1, 1, -1

    turn = 1  # 先手（黒）
    for _ in range(10):  # 10手だけ試す
        ai = ai1 if turn == 1 else ai2
        move = ai.get_move(board)
        if move is None:
            break  # 合法手なしなら終了
        row, col = move
        board[row][col] = turn
        turn = -turn  # 手番交代

    return "テスト実行完了（エラーなし）"

# エラーチェックのために、テスト実行
test_result = play_othello(macaron(), macaron())
test_result

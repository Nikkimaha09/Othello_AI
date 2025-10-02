import tkinter as tk
from tkinter import messagebox

def find_valid_moves(board, player_symbol, opponent_symbol):
    valid_moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for row in range(8):
        for col in range(8):
            if board[row][col] == '.':
                for dr, dc in directions:
                    r, c = row + dr, col + dc
                    sequence = []
                    while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent_symbol:
                        sequence.append((r, c))
                        r += dr
                        c += dc
                    if sequence and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player_symbol:
                        valid_moves.append((row, col))
                        break
    return valid_moves

def make_move(board, row, col, player_symbol, opponent_symbol):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    board[row][col] = player_symbol
    for dr, dc in directions:
        r, c = row + dr, col + dc
        sequence = []
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent_symbol:
            sequence.append((r, c))
            r += dr
            c += dc
        if sequence and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player_symbol:
            for sr, sc in sequence:
                board[sr][sc] = player_symbol

class OthelloGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Othello Game")
        self.board = [['.'] * 8 for _ in range(8)]
        self.board[3][3], self.board[3][4] = 'X', 'O'
        self.board[4][3], self.board[4][4] = 'O', 'X'
        self.player_symbol = 'O'
        self.opponent_symbol = 'X'

        self.canvas = tk.Canvas(root, width=400, height=400, bg="green")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.player_move)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x1, y1 = j * 50, i * 50
                x2, y2 = x1 + 50, y1 + 50
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green")
                if self.board[i][j] == 'O':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="white")
                elif self.board[i][j] == 'X':
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="black")

    def player_move(self, event):
        x, y = event.x // 50, event.y // 50
        valid_moves = find_valid_moves(self.board, self.player_symbol, self.opponent_symbol)
        if (y, x) in valid_moves:
            make_move(self.board, y, x, self.player_symbol, self.opponent_symbol)
            self.draw_board()
            self.ai_move()
        else:
            messagebox.showinfo("Invalid Move", "Choose a valid move.")

    def ai_move(self):
        valid_moves = find_valid_moves(self.board, self.opponent_symbol, self.player_symbol)
        if valid_moves:
            ai_move = valid_moves[0]  # simple AI: picks first valid move
            make_move(self.board, ai_move[0], ai_move[1], self.opponent_symbol, self.player_symbol)
            self.draw_board()
            self.check_game_over()
        else:
            self.check_game_over()

    def check_game_over(self):
        player_moves = find_valid_moves(self.board, self.player_symbol, self.opponent_symbol)
        ai_moves = find_valid_moves(self.board, self.opponent_symbol, self.player_symbol)

        if not player_moves and not ai_moves:
            player_score = sum(row.count(self.player_symbol) for row in self.board)
            ai_score = sum(row.count(self.opponent_symbol) for row in self.board)
            message = f"Game Over!\nPlayer O: {player_score} - AI X: {ai_score}"
            if player_score > ai_score:
                message += "\nPlayer O wins!"
            elif ai_score > player_score:
                message += "\nAI X wins!"
            else:
                message += "\nIt's a tie!"
            messagebox.showinfo("Game Over", message)
            self.root.quit()
        elif not player_moves:
            messagebox.showinfo("Player Passes Turn", "Player O has no valid moves. AI's turn.")
            self.ai_move()
        elif not ai_moves:
            messagebox.showinfo("AI Passes Turn", "AI has no valid moves. Player's turn.")

if __name__ == "__main__":
    root = tk.Tk()
    game = OthelloGame(root)
    root.mainloop()

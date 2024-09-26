import codecs
import csv


class Board:
    def read_sudoku_csv(self, file_path):
        with codecs.open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            sudoku = []  # 2D list
            for row in reader:
                sudoku_row = [0 if value == 'X' else int(
                    value) for value in row]
                sudoku.append(sudoku_row)
        return sudoku

    def display_board(self, board):
        for i in range(len(board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")

            for j in range(len(board[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                # Print an empty space for 0, otherwise print the number
                cell_value = '*' if board[i][j] == 0 else str(board[i][j])

                if j == 8:
                    print(cell_value)
                else:
                    print(cell_value + " ", end="")


import pygame, sys
from pygame.locals import *
import os

pygame.font.init()

# === COLORS ===
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
HIGH = (160, 190, 255)

# === DIRECTIONS ===
NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST = "northwest", "northeast", "southwest", "southeast"

# === Resource Paths ===

BOARD_IMAGE = os.path.join("Checkersgame/assets/board.png")
RED_PIECE_IMAGE = os.path.join("Checkersgame/assets/red_piece.png")
BLUE_PIECE_IMAGE = os.path.join("Checkersgame/assets/blue_piece.png")
RED_KING_IMAGE = os.path.join("Checkersgame/assets/red_king.png")
BLUE_KING_IMAGE = os.path.join("Checkersgame/assets/blue_king.png")


class Game:
    def __init__(self):
        self.graphics = Graphics()
        self.board = Board()
        self.turn = BLUE
        self.selected_piece = None
        self.hop = False
        self.selected_legal_moves = []

    def setup(self):
        self.graphics.setup_window()

    def event_loop(self):
        self.mouse_pos = self.graphics.board_coords(pygame.mouse.get_pos())
        if self.selected_piece:
            self.selected_legal_moves = self.board.legal_moves(self.selected_piece, self.hop)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate_game()

            elif event.type == MOUSEBUTTONDOWN:
                if not self.hop:
                    loc = self.board.location(self.mouse_pos)
                    if loc.occupant and loc.occupant.color == self.turn:
                        self.selected_piece = self.mouse_pos
                    elif self.selected_piece and self.mouse_pos in self.board.legal_moves(self.selected_piece):
                        self.board.move_piece(self.selected_piece, self.mouse_pos)
                        if self.mouse_pos not in self.board.adjacent(self.selected_piece):
                            mid = tuple((a + b) >> 1 for a, b in zip(self.selected_piece, self.mouse_pos))
                            self.board.remove_piece(mid)
                            self.hop = True
                            self.selected_piece = self.mouse_pos
                        else:
                            self.end_turn()
                else:
                    if self.selected_piece and self.mouse_pos in self.board.legal_moves(self.selected_piece, self.hop):
                        self.board.move_piece(self.selected_piece, self.mouse_pos)
                        mid = tuple((a + b) >> 1 for a, b in zip(self.selected_piece, self.mouse_pos))
                        self.board.remove_piece(mid)

                    if not self.board.legal_moves(self.mouse_pos, self.hop):
                        self.end_turn()
                    else:
                        self.selected_piece = self.mouse_pos

    def update(self):
        self.graphics.update_display(self.board, self.selected_legal_moves, self.selected_piece)

    def terminate_game(self):
        pygame.quit()
        sys.exit()

    def main(self):
        self.setup()
        while True:
            self.event_loop()
            self.update()

    def end_turn(self):
        self.turn = RED if self.turn == BLUE else BLUE
        self.selected_piece = None
        self.selected_legal_moves = []
        self.hop = False

        if self.check_for_endgame():
            winner = "CATS" if self.turn == BLUE else "SPIDERS"
            self.graphics.draw_message(f"{winner} WINS!")

    def check_for_endgame(self):
        for x in range(8):
            for y in range(8):
                loc = self.board.location((x, y))
                if loc.color == BLACK and loc.occupant and loc.occupant.color == self.turn:
                    if self.board.legal_moves((x, y)):
                        return False
        return True


class Graphics:
    def __init__(self):
        self.caption = "Checkers"
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.window_size = 600
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.background = pygame.image.load(BOARD_IMAGE)
        self.square_size = self.window_size >> 3
        self.piece_size = self.square_size >> 1
        self.message = False

        # Load piece images with king versions
        self.red_piece_img = pygame.transform.scale(pygame.image.load(RED_PIECE_IMAGE), (self.square_size, self.square_size))
        self.blue_piece_img = pygame.transform.scale(pygame.image.load(BLUE_PIECE_IMAGE), (self.square_size, self.square_size))
        self.red_king_img = pygame.transform.scale(pygame.image.load(RED_KING_IMAGE), (self.square_size, self.square_size))
        self.blue_king_img = pygame.transform.scale(pygame.image.load(BLUE_KING_IMAGE), (self.square_size, self.square_size))

    def setup_window(self):
        pygame.init()
        pygame.display.set_caption(self.caption)

    def update_display(self, board, legal_moves, selected_piece):
        self.screen.blit(self.background, (0, 0))
        self.highlight_squares(legal_moves, selected_piece)
        self.draw_board_pieces(board)
        if self.message:
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)
        pygame.display.update()
        self.clock.tick(self.fps)

    def draw_board_pieces(self, board):
        for x in range(8):
            for y in range(8):
                occupant = board.matrix[x][y].occupant
                if occupant:
                    if occupant.color == RED:
                        img = self.red_king_img if occupant.king else self.red_piece_img
                    else:
                        img = self.blue_king_img if occupant.king else self.blue_piece_img
                    self.screen.blit(img, (x * self.square_size, y * self.square_size))

    def pixel_coords(self, board_coords):
        return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)

    def board_coords(self, pixel):
        return (pixel[0] // self.square_size, pixel[1] // self.square_size)

    def highlight_squares(self, squares, origin):
        for square in squares:
            pygame.draw.rect(self.screen, HIGH, (square[0] * self.square_size, square[1] * self.square_size, self.square_size, self.square_size))
        if origin:
            pygame.draw.rect(self.screen, HIGH, (origin[0] * self.square_size, origin[1] * self.square_size, self.square_size, self.square_size))

    def draw_message(self, message):
        self.message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
        self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.window_size >> 1, self.window_size >> 1)

class Piece:
    def __init__(self, color, king=False):
        self.color = color
        self.king = king


class Square:
    def __init__(self, color, occupant=None):
        self.color = color
        self.occupant = occupant


class Board:
    def __init__(self):
        self.matrix = self.new_board()

    def new_board(self):
        matrix = [[None] * 8 for _ in range(8)]
        for x in range(8):
            for y in range(8):
                color = BLACK if (x + y) % 2 == 0 else WHITE
                matrix[x][y] = Square(color)

        for x in range(8):
            for y in range(3):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(RED)
            for y in range(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(BLUE)

        return matrix

    def location(self, pos):
        x, y = pos
        return self.matrix[x][y]

    def on_board(self, pos):
        x, y = pos
        return 0 <= x < 8 and 0 <= y < 8

    def adjacent(self, pos):
        x, y = pos
        return [
            (x - 1, y - 1), (x + 1, y - 1),
            (x - 1, y + 1), (x + 1, y + 1)
        ]

    def blind_legal_moves(self, pos):
        x, y = pos
        piece = self.matrix[x][y].occupant
        if not piece:
            return []
        directions = []
        if piece.king:
            directions = self.adjacent(pos)
        elif piece.color == BLUE:
            directions = [(x - 1, y - 1), (x + 1, y - 1)]
        else:
            directions = [(x - 1, y + 1), (x + 1, y + 1)]
        return directions

    def legal_moves(self, pos, hop=False):
        x, y = pos
        piece = self.matrix[x][y].occupant
        if not piece:
            return []

        legal = []
        for dx, dy in self.blind_legal_moves(pos):
            if self.on_board((dx, dy)):
                target = self.matrix[dx][dy].occupant
                if not hop and not target:
                    legal.append((dx, dy))
                elif target and target.color != piece.color:
                    jump_x = dx + (dx - x)
                    jump_y = dy + (dy - y)
                    if self.on_board((jump_x, jump_y)) and not self.matrix[jump_x][jump_y].occupant:
                        legal.append((jump_x, jump_y))
        return legal

    def remove_piece(self, pos):
        x, y = pos
        self.matrix[x][y].occupant = None

    def move_piece(self, start, end):
        sx, sy = start
        ex, ey = end
        self.matrix[ex][ey].occupant = self.matrix[sx][sy].occupant
        self.remove_piece(start)
        self.king((ex, ey))

    def king(self, pos):
        x, y = pos
        piece = self.matrix[x][y].occupant
        if piece and ((piece.color == BLUE and y == 0) or (piece.color == RED and y == 7)):
            piece.king = True



def main():
	game = Game()
	game.main()

if __name__ == "__main__":
	main()
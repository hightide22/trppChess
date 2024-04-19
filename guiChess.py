import pygame as pg
from packageChess import boardChess123 as boardChess
from packageChess import piecesChess123 as piecesChess

screen = pg.display.set_mode((640, 640))

pg.display.set_caption("Chess")

boardIMG = pg.image.load(r"packageChess/sprites/chessBoard.jpg")
boardRect = boardIMG.get_rect(bottomright=(640, 640))
screen.blit(boardIMG, boardRect)

gameBoard = boardChess.Board()
gameBoard.setStandartBoard()

print(gameBoard.board[0][0])



notSelected = True
turns = []

while True:
    screen.blit(boardIMG, boardRect)

    for i in range(8):
        for j in range(8):
            pieceIMG = pg.image.load(r"packageChess/sprites/" + str(gameBoard.board[i][j]) + ".png")
            pieceRect = pieceIMG.get_rect(center=(40 + 80 * j, 40 + 80 * i))
            screen.blit(pieceIMG, pieceRect)
    if len(turns):
        for i in turns[0]:
            webImg = pg.image.load(r"packageChess/sprites/pos.png")
            webRec = webImg.get_rect(center=(40 + 80 * i[0], 40 + 80 * i[1]))
            screen.blit(webImg, webRec)
        for i in turns[1]:
            webImg = pg.image.load(r"packageChess/sprites/kill.png")
            webRec = webImg.get_rect(center=(40 + 80 * i[0], 40 + 80 * i[1]))
            screen.blit(webImg, webRec)

    for event in pg.event.get():
        ID_event = event.type
        if ID_event == 1025:
            if notSelected:
                x, y = event.pos
                x = x // 80
                y = y // 80
                print(x, y)
                turns = gameBoard.selectPiece(x, y)
                notSelected = not(len(turns[0]) or len(turns[1]))
                if not notSelected:
                    selectedPiece = (x, y)
            else:
                x, y = event.pos
                x = x // 80
                y = y // 80
                click = (x, y)
                if click in turns[0] or click in turns[1]:
                    gameBoard.movePiece(selectedPiece[0], selectedPiece[1], click[0], click[1])
                    gameBoard.turn *= -1

                turns = []
                notSelected = True
    pg.display.flip()

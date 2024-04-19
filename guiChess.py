import pygame as pg

screen = pg.display.set_mode((640, 700))
pg.display.set_caption("Chess")

boardIMG = pg.image.load(r"sprites\chessBoard.jpg")
boardRect = boardIMG.get_rect(bottomright=(640, 640))
screen.blit(boardIMG, boardRect)
while True:
    for event in pg.event.get():
        ID_event = pg.event.EventType
    pg.display.flip()

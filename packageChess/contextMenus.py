import pygame as pg


class Menu:
    def pawnTransormationWhite(self) -> "rkqb":
        sc = pg.display.set_mode((320, 80))
        sc.fill("white")
        pg.display.set_caption("Выберите фигуру:")

        while True:
            pieceIMG1 = pg.image.load(r"packageChess\sprites\1r.png")
            pieceRect1 = pieceIMG1.get_rect(center=(40 + 80 * 0, 40 ))
            sc.blit(pieceIMG1, pieceRect1)
            pieceIMG2 = pg.image.load(r"packageChess\sprites\1k.png")
            pieceRect2 = pieceIMG2.get_rect(center=(40 + 80 * 1, 40 ))
            sc.blit(pieceIMG2, pieceRect2)
            pieceIMG3 = pg.image.load(r"packageChess\sprites\1q.png")
            pieceRect3 = pieceIMG3.get_rect(center=(40 + 80 * 2, 40 ))
            sc.blit(pieceIMG3, pieceRect3)
            pieceIMG4 = pg.image.load(r"packageChess/sprites/1b.png")
            pieceRect4 = pieceIMG4.get_rect(center=(40 + 80 * 3, 40))
            sc.blit(pieceIMG4, pieceRect4)
            for event in pg.event.get():
                ID_event = event.type
                if ID_event == 1025:
                    x, y = event.pos
                    x = x // 80
                    print(x)
                    if x == 0: return "1r"
                    if x == 1: return "1k"
                    if x == 2: return "1q"
                    if x == 3: return "1b"

            pg.display.flip()

    def pawnTransormationBlack(self) -> "rkqb":
        sc = pg.display.set_mode((320, 80))
        sc.fill("white")
        pg.display.set_caption("Выберите фигуру:")

        while True:
            pieceIMG1 = pg.image.load(r"packageChess\sprites\-1r.png")
            pieceRect1 = pieceIMG1.get_rect(center=(40 + 80 * 0, 40 ))
            sc.blit(pieceIMG1, pieceRect1)
            pieceIMG2 = pg.image.load(r"packageChess\sprites\-1k.png")
            pieceRect2 = pieceIMG2.get_rect(center=(40 + 80 * 1, 40 ))
            sc.blit(pieceIMG2, pieceRect2)
            pieceIMG3 = pg.image.load(r"packageChess\sprites\-1q.png")
            pieceRect3 = pieceIMG3.get_rect(center=(40 + 80 * 2, 40 ))
            sc.blit(pieceIMG3, pieceRect3)
            pieceIMG4 = pg.image.load(r"packageChess/sprites/-1b.png")
            pieceRect4 = pieceIMG4.get_rect(center=(40 + 80 * 3, 40))
            sc.blit(pieceIMG4, pieceRect4)
            for event in pg.event.get():
                ID_event = event.type
                if ID_event == 1025:
                    x, y = event.pos
                    x = x // 80
                    print(x)
                    if x == 0: return "-1r"
                    if x == 1: return "-1k"
                    if x == 2: return "-1q"
                    if x == 3: return "-1b"

            pg.display.flip()

    def startMenu(self) -> '"standard" | "random" | "standardTimed" | "randomTimed"':
        sc = pg.display.set_mode((245, 240))
        sc.fill("white")
        pg.display.set_caption("Выберите Режим:")

        while True:
            startIMG = pg.image.load(r"packageChess\sprites\startSecret.png")
            startRect = startIMG.get_rect(topleft=(0, 0))
            sc.blit(startIMG, startRect)

            for event in pg.event.get():
                ID_event = event.type
                if ID_event == pg.QUIT:
                    exit()
                if ID_event == 1025:
                    x, y = event.pos
                    if 10 < x < 185:
                        if 15 < y < 70: return "standard"
                        if 90 < y < 145: return "random"
                        if 165 < y < 215: return "secret"
                    if 190 < x < 230:
                        if 15 < y < 70: return "standardTimed"
                        if 90 < y < 145: return "randomTimed"
                        if 165 < y < 215: return "secretTimed"

            pg.display.flip()
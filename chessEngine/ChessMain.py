import pygame as p
import ChessEngine, SmartMoveFinder, util
from multiprocessing import Queue, Process

p.init()
width = height = 512
dimension = 8
sq_size = width // dimension
max_fps = 15
images = {}

# initialize a global dictionary of images
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp" ,"wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load('images/{}.png'.format(piece)), (sq_size, sq_size))

def main():
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelected = () # keeps track of square selected
    playerClicks = []
    col = -1
    row = -1
    animate = False
    gameOver = False
    playerOne = False
    playerTwo = True
    AIThinking = False

    nextWhiteHumanPawnBiasScore = SmartMoveFinder.whiteHumanPawnBiasScore.copy()
    nextWhiteHumanRookBiasScore = SmartMoveFinder.whiteHumanRookBiasScore.copy()
    nextWhiteHumanKnightBiasScore = SmartMoveFinder.whiteHumanKnightBiasScore.copy()
    nextWhiteHumanBishopBiasScore = SmartMoveFinder.whiteHumanBishopBiasScore.copy()
    nextWhiteHumanQueenBiasScore = SmartMoveFinder.whiteHumanQueenBiasScore.copy()
    nextWhiteHumanKingBiasScore = SmartMoveFinder.whiteHumanKingBiasScore.copy()

    nextBlackHumanPawnBiasScore = SmartMoveFinder.blackHumanPawnBiasScore.copy()
    nextBlackHumanRookBiasScore = SmartMoveFinder.blackHumanRookBiasScore.copy()
    nextBlackHumanKnightBiasScore = SmartMoveFinder.blackHumanKnightBiasScore.copy()
    nextBlackHumanBishopBiasScore = SmartMoveFinder.blackHumanBishopBiasScore.copy()
    nextBlackHumanQueenBiasScore = SmartMoveFinder.blackHumanQueenBiasScore.copy()
    nextBlackHumanKingBiasScore = SmartMoveFinder.blackHumanKingBiasScore.copy()

    HumanPiecePositionScores = {
        "wK":nextWhiteHumanKingBiasScore,
        "wQ":nextWhiteHumanQueenBiasScore,
        "wR":nextWhiteHumanRookBiasScore,
        "wB":nextWhiteHumanBishopBiasScore,
        "wN":nextWhiteHumanKnightBiasScore,
        'wp':nextWhiteHumanPawnBiasScore,
        "bK":nextBlackHumanKingBiasScore,
        "bQ":nextBlackHumanQueenBiasScore,
        "bR":nextBlackHumanRookBiasScore,
        "bB":nextBlackHumanBishopBiasScore,
        "bN":nextBlackHumanKnightBiasScore,
        'bp':nextBlackHumanPawnBiasScore,
    }

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:

                    location = p.mouse.get_pos() # gets (x, y) location of mouse
                    col = location[0] // sq_size
                    row = location[1] // sq_size

                    if sqSelected == (row, col): # if player selects the same square twice reset sqselected and playerclicks
                        sqSelected = ()
                        playerClicks = []
                    else :
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and humanTurn:

                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())

                        for i in range(0, len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(move)
                                moveMade = True
                                sqSelected = ()
                                playerClicks = []
                                animate = True
                                # Update Human Bias
                                HumanPiecePositionScores[move.pieceMoved][move.endRow][move.endCol] += 1

                        if not moveMade:
                            playerClicks = [sqSelected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    validMoves = gs.getValidMoves()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    AIThinking = False
                    humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
                    returnQueue = Queue()
                    if playerOne:
                        util.write_list_to_csv('./humanBiasScores/white/humanPawnBiasScore.csv', nextWhiteHumanPawnBiasScore)
                        util.write_list_to_csv('./humanBiasScores/white/humanRookBiasScore.csv', nextWhiteHumanRookBiasScore)
                        util.write_list_to_csv('./humanBiasScores/white/humanBishopBiasScore.csv', nextWhiteHumanBishopBiasScore)
                        util.write_list_to_csv('./humanBiasScores/white/humanKnightBiasScore.csv', nextWhiteHumanKnightBiasScore)
                        util.write_list_to_csv('./humanBiasScores/white/humanQueenBiasScore.csv', nextWhiteHumanQueenBiasScore)
                    if playerTwo:
                        util.write_list_to_csv('./humanBiasScores/black/humanPawnBiasScore.csv', nextBlackHumanPawnBiasScore)
                        util.write_list_to_csv('./humanBiasScores/black/humanRookBiasScore.csv', nextBlackHumanRookBiasScore)
                        util.write_list_to_csv('./humanBiasScores/black/humanBishopBiasScore.csv', nextBlackHumanBishopBiasScore)
                        util.write_list_to_csv('./humanBiasScores/black/humanKnightBiasScore.csv', nextBlackHumanKnightBiasScore)
                        util.write_list_to_csv('./humanBiasScores/black/humanQueenBiasScore.csv', nextBlackHumanQueenBiasScore)


        if not gameOver and not humanTurn:
            if not AIThinking:
                AIThinking = True
                print("THINKING")
                returnQueue = Queue()
                myPocess = Process(target=SmartMoveFinder.findBestMoveNegaMax, args=(gs, validMoves, returnQueue))
                myPocess.start()


            if not myPocess.is_alive():
                print("DONE THINKING")
                AImove = returnQueue.get()
                if AImove is None:
                    AImove = SmartMoveFinder.randomMove(validMoves)
                gs.makeMove(AImove)
                moveMade = True
                animate = True
                AIThinking = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black Wins by Checkmate")
            if not gs.whiteToMove:
                drawText(screen, "White Wins by Checkmate")
        elif gs.stalemate:
            gameOver = True
            drawText(screen, "Stalemate!")

        clock.tick(max_fps)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # highlight selected square
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*sq_size, r*sq_size))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))



def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != '--':
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def animateMove(move, screen, board, clock):
    global colors
    coords = [] # list of coordinates that the animation moves through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frames in range(frameCount + 1):
        r, c = (move.startRow + dR * (frames / frameCount), move.startCol + dC * (frames / frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        #erase piece moved from its ending square
        color = colors[((move.endRow + move.endCol) % 2)]
        endSquare = p.Rect(move.endCol*sq_size, move.endRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(images[move.pieceCaptured], endSquare)
        screen.blit(images[move.pieceMoved], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(180)

def drawText(screen, text):
    font = p.font.SysFont("Helvitica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0,0,width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0 , p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == "__main__":
    main()
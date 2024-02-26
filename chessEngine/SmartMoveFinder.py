import random
import util

pieceScores = {
    "K":0,
    "Q":9,
    "R":5,
    "B":3,
    "N":3,
    "p":1
}

normalPiece = [[1,1,1,1,1,1,1,1],
               [1,2,2,2,2,2,2,1],
               [1,2,3,3,3,3,2,1],
               [1,2,3,4,4,3,2,1],
               [1,2,3,4,4,3,2,1],
               [1,2,3,3,3,3,2,1],
               [1,2,2,2,2,2,2,1],
               [1,1,1,1,1,1,1,1]]

blackKingScores = [[0, 0, 0, 0, 1, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ]]

whiteKingScores = [[0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 0, 0, 0, 0 ],
                    [0, 0, 0, 0, 1, 0, 0, 0 ]]


whitePawnScores =   [[9.7, 9.8 , 9.9 , 9.9 , 9.9 , 9.9 , 9.8 , 9.7],
                    [1.6, 2.7 , 2.8 , 2.9 , 2.9 , 2.8 , 2.7 , 1.6],
                    [1.5, 2.6 , 3.7 , 3.8 , 3.8 , 3.7 , 2.6 , 1.5],
                    [1.4, 2.5 , 3.6 , 4.7 , 4.7 , 3.6 , 2.5 , 1.4],
                    [1.3, 2.4 , 4.5 , 4.6 , 4.6 , 4.5 , 2.4 , 1.3],
                    [1.2, 2.3 , 3.4 , 3.5 , 3.5 , 3.4 , 2.3 , 1.2],
                    [1.1, 2.2 , 2.3 , 2.4 , 2.4 , 2.3 , 2.2 , 1.1],
                    [1.1, 1.2 , 1.3 , 1.4 , 1.4 , 1.3 , 1.2 , 1.1]]

blackPawnScores =   [[1.1, 1.2 , 1.3 , 1.4 , 1.4 , 1.3 , 1.2 , 1.1],
                    [1.1, 2.2 , 2.3 , 2.4 , 2.4 , 2.3 , 2.2 , 1.1],
                    [1.2, 2.3 , 3.4 , 3.5 , 3.5 , 3.4 , 2.3 , 1.2],
                    [1.3, 2.4 , 4.5 , 4.6 , 4.6 , 4.5 , 2.4 , 1.3],
                    [1.4, 2.5 , 3.6 , 4.7 , 4.7 , 3.6 , 2.5 , 1.4],
                    [1.5, 2.6 , 3.7 , 3.8 , 3.8 , 3.7 , 2.6 , 1.5],
                    [1.6, 2.7 , 2.8 , 2.9 , 2.9 , 2.8 , 2.7 , 1.6],
                    [9.7, 9.8 , 9.9 , 9.9 , 9.9 , 9.9 , 9.8 , 9.7]]

#TODO clean up this code
whiteHumanPawnBiasScore = util.read_csv_as_list('./humanBiasScores/white/humanPawnBiasScore.csv')
whiteHumanKnightBiasScore = util.read_csv_as_list('./humanBiasScores/white/humanKnightBiasScore.csv')
whiteHumanRookBiasScore = util.read_csv_as_list('./humanBiasScores/white/humanRookBiasScore.csv')
whiteHumanBishopBiasScore = util.read_csv_as_list('./humanBiasScores/white/humanBishopBiasScore.csv')
whiteHumanQueenBiasScore = util.read_csv_as_list('./humanBiasScores/white/humanQueenBiasScore.csv')
whiteHumanKingBiasScore = util.read_csv_as_list('./humanBiasScores/white/humanKingBiasScore.csv')

blackHumanPawnBiasScore = util.read_csv_as_list('./humanBiasScores/black/humanPawnBiasScore.csv')
blackHumanKnightBiasScore = util.read_csv_as_list('./humanBiasScores/black/humanKnightBiasScore.csv')
blackHumanRookBiasScore = util.read_csv_as_list('./humanBiasScores/black/humanRookBiasScore.csv')
blackHumanBishopBiasScore = util.read_csv_as_list('./humanBiasScores/black/humanBishopBiasScore.csv')
blackHumanQueenBiasScore = util.read_csv_as_list('./humanBiasScores/black/humanQueenBiasScore.csv')
blackHumanKingBiasScore = util.read_csv_as_list('./humanBiasScores/black/humanKingBiasScore.csv')

HumanPiecePositionScores = {
    "wQ":whiteHumanQueenBiasScore,
    "wR":whiteHumanRookBiasScore,
    "wB":whiteHumanBishopBiasScore,
    "wN":whiteHumanKnightBiasScore,
    'wp':whiteHumanPawnBiasScore,
    "wK":whiteHumanKingBiasScore,
    "bQ":blackHumanQueenBiasScore,
    "bR":blackHumanRookBiasScore,
    "bB":blackHumanBishopBiasScore,
    "bN":blackHumanKnightBiasScore,
    'bp':blackHumanPawnBiasScore,
    "bK":blackHumanKingBiasScore
}

piecePositionScores = {
    "Q":normalPiece,
    "R":normalPiece,
    "B":normalPiece,
    "N":normalPiece,
    "bK":blackKingScores,
    "wK":whiteKingScores,
    'wp':whitePawnScores,
    'bp':blackPawnScores
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4

def randomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    if validMoves is not None:
        random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.checkmate:
            score = -CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
            if opponentMinMaxScore > opponentMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = playerMove
            gs.undoMove()
    return bestPlayerMove

def findBestMoveMinMax(gs, validMoves):
    global nextMove
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if validMoves is not None:
        random.shuffle(validMoves)
    if depth == 0:
        return scoreBoard(gs)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            opponentMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, opponentMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            opponentMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, opponentMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findBestMoveNegaMax(gs, validMoves, returnQueue):
    global nextMove, counter
    nextMove = None
    # order moves by checks, threats and protects
    counter = 0
    prioritizedMoves = sorted(validMoves, key=lambda x: (x.isMoveCapture, x.threats, x.protects, x.moves), reverse=True)

    findMoveNegaMaxAlphaBeta(gs, prioritizedMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    returnQueue.put(nextMove)

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return (scoreMaterial(gs.board) + scoreBoard(gs)) * turnMultiplier
    if validMoves == None:
        return (scoreMaterial(gs.board) + scoreBoard(gs)) * turnMultiplier

    optimumScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        opponentMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, opponentMoves, depth-1, -turnMultiplier)
        if score > optimumScore:
            optimumScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return optimumScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    opponentMoves = []
    counter += 1
    if depth == 0:
        # game phase logic could go here
        return scoreBoard(gs) * turnMultiplier
    if gs.checkmate:
        CHECKMATE
    if gs.stalemate:
        return 0


    optimumScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        opponentMoves = gs.getValidMoves()
        if opponentMoves is not None:
            prioritizedMoves = sorted(opponentMoves, key=lambda x: (x.isMoveCapture, x.threats, x.protects, x.moves), reverse=True)
            score = -(findMoveNegaMaxAlphaBeta(gs, prioritizedMoves, depth-1, -beta, -alpha, -turnMultiplier))
            if score > optimumScore:
                optimumScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(score, move.getChessNotation())
            gs.undoMove()
            if optimumScore > alpha:
                alpha = optimumScore
            if alpha >= beta:
                break
    return optimumScore

def scoreBoard(gs):
    score = 0

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                #score positionally
                piecePositionScore = 0
                if square[1] == 'p':
                    piecePositionScore = piecePositionScores[square][row][col] * .1
                elif square[1] == 'K':
                    pass
                else:
                    piecePositionScore = piecePositionScores[square[1]][row][col] * .1

                humanBiasScore = HumanPiecePositionScores[square][row][col] * .01

                if square[0] == 'w':
                    score += (pieceScores[square[1]] + piecePositionScore + humanBiasScore)
                elif square[0] == 'b':
                    score -= (pieceScores[square[1]] + piecePositionScore + humanBiasScore)
    #TODO properly score castling
    return round(score, 3)


# score board based on material
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -= pieceScores[square[1]]

    return score
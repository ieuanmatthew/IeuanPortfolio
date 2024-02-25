###
###
###

class GameState():
    def __init__(self):
        # the board is an 8x8 2d list, each element has two letters
        # the first letter determines whether the piece is black or white
        # the second letter determines the piece type
        # -- represents an empty space
        self.board = [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.currentCastleRights = castleRights(True, True, True, True)
        self.castleRightslog = [castleRights(self.currentCastleRights.wks, self.currentCastleRights.bks,
                                             self.currentCastleRights.wqs, self.currentCastleRights.bqs)]
        self.hasWhiteCastled = False
        self.hasBlackCastled = False

        self.captures = []
        self.checks = []

    def getChecksThreatsProtects(self, validMoves):
        checkMoves = []
        captureMoves = []
        pinMoves = []
        threatMoves = []
        for move in validMoves:
            if move.pieceCaptured != '--':
                captureMoves.append(move)
            for pin in self.pins:
                if move.startRow == pin[0] and move.startCol == pin[1]:
                    pinMoves.append(move)
            for check in self.checks:
                if move.startRow == check[0] and move.startCol == check[1]:
                    checkMoves.append(move)


        return checkMoves, captureMoves, pinMoves, threatMoves


    def makeMove(self, move):
        # en passant capture
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = 'wR'
                self.board[move.endRow][move.endCol + 1] = '--'
                self.hasWhiteCastled = True
            elif move.endCol - move.startCol == -2:
                self.board[move.endRow][move.endCol + 1] = 'wR'
                self.board[move.endRow][move.endCol - 2] = '--'
                self.hasWhiteCastled = True
        if move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol - 1] = 'bR'
                self.board[move.endRow][move.endCol + 1] = '--'
                self.hasBlackCaslted = True
            elif move.endCol - move.startCol == - 2:
                self.board[move.endRow][move.endCol + 1] = 'bR'
                self.board[move.endRow][move.endCol - 2] = '--'
                self.hasBlackCaslted = True

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        self.updateCastleRight(move)
        currCastleRights = castleRights(self.currentCastleRights.wks, self.currentCastleRights.bks,
                                             self.currentCastleRights.wqs, self.currentCastleRights.bqs)

        self.castleRightslog.append(currCastleRights)


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            if move.enPassant:
                if self.whiteToMove:
                    self.board[move.startRow][move.endCol] = "bp"
                else:
                    self.board[move.startRow][move.endCol] = "wp"
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured

            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = 'wR'
                    self.board[move.endRow][move.endCol - 1] = '--'
                    self.hasWhiteCastled = False
                elif move.endCol - move.startCol == -2:
                    self.board[move.endRow][move.endCol + 1] = '--'
                    self.board[move.endRow][move.endCol - 2] = 'wR'
                    self.hasWhiteCastled = False
            if move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol + 1] = 'bR'
                    self.board[move.endRow][move.endCol - 1] = '--'
                    self.hasBlackCaslted = False
                elif move.endCol - move.startCol == -2:
                    self.board[move.endRow][move.endCol + 1] = '--'
                    self.board[move.endRow][move.endCol - 2] = 'bR'
                    self.hasBlackCaslted = False
            self.castleRightslog.pop()

            self.currentCastleRights.wks = self.castleRightslog[-1].wks
            self.currentCastleRights.bks = self.castleRightslog[-1].bks
            self.currentCastleRights.wqs = self.castleRightslog[-1].wqs
            self.currentCastleRights.bqs = self.castleRightslog[-1].bqs

            self.whiteToMove = not self.whiteToMove
            self.checkmate = False
            self.stalemate = False

    def updateCastleRight(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        if move.pieceMoved == 'bK':
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        if move.pieceMoved == 'wR':
            if move.startCol == 0:
                self.currentCastleRights.wqs = False
            else:
                self.currentCastleRights.wks = False
        if move.pieceMoved == 'bR':
            if move.startCol == 0:
                self.currentCastleRights.bqs = False
            else:
                self.currentCastleRights.bks = False

    def getValidMoves(self):
        self.inCheck, self.pins, self.checks = self.pinsAndChecks()
        moves = self.getAllPossibleMoves()
        kingLocation = self.blackKingLocation
        if self.whiteToMove:
            kingLocation = self.whiteKingLocation
        validSquares = []
        if self.inCheck:
            if len(self.checks) == 1:
                checks = self.checks[0]
                row = checks[0]
                col = checks[1]
                rowDir = checks[2]
                colDir = checks[3]
                if self.board[row][col][1] == 'N':
                    validSquares = [(row, col)]
                else:
                    for i in range(1, 8):
                        endrow = kingLocation[0] + i * rowDir
                        endcol = kingLocation[1] + i * colDir
                        validSquares.append((endrow, endcol))
                        if endrow == row and endcol == col:
                            break

                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow,  moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
                self.checkEndGame(moves)
                return moves
            else:
                self.checkEndGame(moves)
                return self.getKingMoves(kingLocation[0], kingLocation[1], moves)
        else:
            self.checkEndGame(moves)
            return moves

    def checkEndGame(self, validMoves):
        if len(validMoves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True


    def pinsAndChecks(self):
        inCheck = False
        pins = []
        checks = []
        turn = 'b'
        enemyTurn = 'w'
        kingLocation = self.blackKingLocation
        if self.whiteToMove:
            turn = 'w'
            enemyTurn = 'b'
            kingLocation = self.whiteKingLocation
        directions = [(0,1),(1,0),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
        # For each direction look for a potential pin or check
        for direction in directions:
            potentialPin = ()
            for j in range(1, 8):
                row = kingLocation[0] + direction[0] * j
                col = kingLocation[1] + direction[1] * j
                if row < 8 and row >= 0 and col >= 0 and col < 8:
                    if self.board[row][col].startswith(turn):
                        if potentialPin == ():
                            potentialPin = (row, col, direction[0], direction[1])
                        else:
                            break
                    elif self.board[row][col].startswith(enemyTurn):
                        piece = self.board[row][col][1]
                        if ((piece == 'B' and direction in [(1,1),(-1,1),(-1,-1),(1,-1)]) or
                            (piece == 'R' and direction in [(0,1),(1,0),(-1,0),(0,-1)]) or
                            (piece == 'Q') or
                            (j == 1 and piece == 'p' and turn == 'w' and direction in [(-1,1),(-1,-1)]) or
                            (j == 1 and piece == 'p' and turn == 'b' and direction in [(1,1),(1,-1)]) or
                            (j == 1 and piece == 'K')):
                            if potentialPin == ():
                                inCheck = True
                                checks.append((row, col, direction[0], direction[1]))
                                break
                            else:
                                pins.append(potentialPin)
                                break
                        else:
                            break
                    else:
                        pass
                else:
                    break # off the board

        directions = [(2,1),(2, -1),(-2,1),(-2,-1),(1, 2),(-1, 2),(1, -2), (-1,-2)]
        for direction in directions:
            row = kingLocation[0] + direction[0]
            col = kingLocation[1] + direction[1]
            if row < 8 and row >= 0 and col >= 0 and col < 8:
                if self.board[row][col].startswith(enemyTurn):
                    piece = self.board[row][col][1]
                    if piece == 'N':
                        inCheck = True
                        checks.append((row, col, direction[0], direction[1]))

        return inCheck , pins , checks

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    if piece == 'R':
                        self.getRookMoves(r, c, moves)
                    if piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    if piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    if piece == 'Q':
                        self.getRookMoves(r, c, moves)
                        self.getBishopMoves(r, c, moves)
                    if piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        isPinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                isPinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break
        if self.whiteToMove:
            if self.board[r - 1][c] == '--':
                if not isPinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == '--':
                        moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:
                if not isPinned or pinDirection == (-1, -1):
                    if (self.board[r - 1][c - 1].startswith('b')):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 7:
                if not isPinned or pinDirection == (-1, 1):
                    if (self.board[r - 1][c + 1].startswith('b')):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if len(self.moveLog) > 0:
                if (self.moveLog[-1].startRow == 1 and
                    self.moveLog[-1].endRow == 3 and
                    self.moveLog[-1].pieceMoved == 'bp' and
                    r == self.moveLog[-1].endRow and
                    c + 1 == self.moveLog[-1].endCol):
                    if not isPinned or pinDirection == (-1, 1):
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                if (self.moveLog[-1].startRow == 1 and
                    self.moveLog[-1].endRow == 3 and
                    self.moveLog[-1].pieceMoved == 'bp' and
                    r == self.moveLog[-1].endRow and
                    c - 1 == self.moveLog[-1].endCol):
                    if not isPinned or pinDirection == (-1, -1):
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
        else:
            if self.board[r + 1][c] == '--':
                if not isPinned or pinDirection == (1, 0):
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == '--':
                        moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if not isPinned or pinDirection == (1, -1):
                    if (self.board[r + 1][c - 1].startswith('w')):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 7:
                if not isPinned or pinDirection == (1, 1):
                    if (self.board[r + 1][c + 1].startswith('w')):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
            if len(self.moveLog) > 0:
                if (self.moveLog[-1].startRow == 6 and
                    self.moveLog[-1].endRow == 4 and
                    self.moveLog[-1].pieceMoved == 'wp' and
                    r == self.moveLog[-1].endRow and
                    c - 1 == self.moveLog[-1].endCol):
                    if not isPinned or pinDirection == (1, -1):
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))
                if (self.moveLog[-1].startRow == 6 and
                    self.moveLog[-1].endRow == 4 and
                    self.moveLog[-1].pieceMoved == 'wp' and
                    r == self.moveLog[-1].endRow and
                    c + 1 == self.moveLog[-1].endCol):
                    if not isPinned or pinDirection == (1, 1):
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))
        for i in range(len(moves)-1,-1,-1):
            if moves[i].enPassant:
                self.makeMove(moves[i])
                self.whiteToMove = not self.whiteToMove
                inCheck, pins, checks = self.pinsAndChecks()
                if inCheck:
                    moves.remove(moves[i])
                self.undoMove()
                self.whiteToMove = not self.whiteToMove




    def getRookMoves(self, r, c, moves):
        isPinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                isPinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break

        dircetions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        if self.whiteToMove:
            for direction in dircetions:
                for length in range(1, 8):
                    rowVector = direction[0] * length
                    colVector = direction[1] * length
                    if not isPinned or pinDirection == (direction[0], direction[1]):
                        if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                            if(self.board[r + rowVector][c + colVector].startswith('w')):
                                break
                            elif(self.board[r + rowVector][c + colVector].startswith('b')):
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))
                                break
                            else:
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))
        else:
            for direction in dircetions:
                for length in range(1, 8):
                    rowVector = direction[0] * length
                    colVector = direction[1] * length
                    if not isPinned or pinDirection == (direction[0], direction[1]):
                        if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                            if(self.board[r + rowVector][c + colVector].startswith('b')):
                                break
                            elif(self.board[r + rowVector][c + colVector].startswith('w')):
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))
                                break
                            else:
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))


    def getKnightMoves(self, r, c, moves):
        isPinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                isPinned = True
                break

        directions = [(2,1),(2, -1),(-2,1),(-2,-1),(1, 2),(-1, 2),(1, -2), (-1,-2)]
        if not isPinned:
            if self.whiteToMove:
                for direction in directions:
                    rowEndpoint = r + direction[0]
                    colEndpoint = c + direction[1]
                    if rowEndpoint <= 7 and rowEndpoint >= 0 and colEndpoint <= 7 and colEndpoint >= 0:
                        if (not self.board[rowEndpoint][colEndpoint].startswith('w')):
                            moves.append(Move((r, c), (rowEndpoint, colEndpoint), self.board))

            else:
                for direction in directions:
                    rowEndpoint = r + direction[0]
                    colEndpoint = c + direction[1]
                    if rowEndpoint <= 7 and rowEndpoint >= 0 and colEndpoint <= 7 and colEndpoint >= 0:
                        if (not self.board[rowEndpoint][colEndpoint].startswith('b')):
                            moves.append(Move((r, c), (rowEndpoint, colEndpoint), self.board))




    def getBishopMoves(self, r, c, moves):
        isPinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                isPinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break

        dircetions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        if self.whiteToMove:
            for direction in dircetions:
                for length in range(1, 8):
                    rowVector = direction[0] * length
                    colVector = direction[1] * length
                    if not isPinned or pinDirection == (direction[0], direction[1]):
                        if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                            if(self.board[r + rowVector][c + colVector].startswith('w')):
                                break
                            elif(self.board[r + rowVector][c + colVector].startswith('b')):
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))
                                break
                            else:
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))

        else:
            for direction in dircetions:
                for length in range(1, 8):
                    rowVector = direction[0] * length
                    colVector = direction[1] * length
                    if not isPinned or pinDirection == (direction[0], direction[1]):
                        if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                            if(self.board[r + rowVector][c + colVector].startswith('b')):
                                break
                            elif(self.board[r + rowVector][c + colVector].startswith('w')):
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))
                                break
                            else:
                                moves.append(Move((r, c), (r + rowVector, c + colVector), self.board))

    def getKingMoves(self, r, c, moves):

        dircetions = [(1, 1), (-1, -1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        possibleMoves = []

        if self.whiteToMove:
            for direction in dircetions:
                rowEndpoint = r + direction[0]
                colEndpoint = c + direction[1]
                if rowEndpoint <= 7 and rowEndpoint >= 0 and colEndpoint <= 7 and colEndpoint >= 0:
                    if(self.board[rowEndpoint][colEndpoint].startswith('w')):
                        pass
                    elif(self.board[rowEndpoint][colEndpoint].startswith('b')):
                        possibleMoves.append(Move((r, c), (rowEndpoint, colEndpoint), self.board))
                    else:
                        possibleMoves.append(Move((r, c), (rowEndpoint, colEndpoint), self.board))

        else:
            for direction in dircetions:
                rowEndpoint = r + direction[0]
                colEndpoint = c + direction[1]
                if rowEndpoint <= 7 and rowEndpoint >= 0 and colEndpoint <= 7 and colEndpoint >= 0:
                    if(self.board[rowEndpoint][colEndpoint].startswith('b')):
                        pass
                    elif(self.board[rowEndpoint][colEndpoint].startswith('w')):
                        possibleMoves.append(Move((r, c), (rowEndpoint, colEndpoint), self.board))
                    else:
                        possibleMoves.append(Move((r, c), (rowEndpoint, colEndpoint), self.board))
        self.getCastleMoves(r, c, possibleMoves)
        #TODO check if king move is in check with pinsandchecks
        for move in possibleMoves:
            self.makeMove(move)
            self.whiteToMove = not self.whiteToMove
            inCheck, pins, checks = self.pinsAndChecks()
            if not inCheck:
                moves.append(move)
            self.undoMove()
            self.whiteToMove = not self.whiteToMove

    def getCastleMoves(self, r, c, moves):
        if self.inCheck:
            return
        if self.whiteToMove and self.currentCastleRights.wks:
            self.appendCastleMoves(r, c, moves, 1)
        if self.whiteToMove and self.currentCastleRights.wqs:
            self.appendCastleMoves(r, c, moves, -1)
        if not self.whiteToMove and self.currentCastleRights.bks:
            self.appendCastleMoves(r, c, moves, 1)
        if not self.whiteToMove and self.currentCastleRights.bqs:
            self.appendCastleMoves(r, c, moves, -1)

    def appendCastleMoves(self, r, c, moves, d):
        # check if squares are under attack
        for l in range(1, 2):
            self.makeMove(Move((r,c),(r, c + (d * l)), self.board))
            self.whiteToMove = not self.whiteToMove
            inCheck, pins, checks = self.pinsAndChecks()
            self.undoMove()
            self.whiteToMove = not self.whiteToMove
            if inCheck:
                return 0

        if d == -1:
            if(self.board[r][c + (d)] == '--' and
                self.board[r][c + (d * 2)] == '--' and
                self.board[r][c + (d * 3)] == '--' and
                self.board[r][c + (d * 4)][1] == 'R'):
                moves.append(Move((r,c),(r, c + (d * 2)), self.board))
        else:
            if (self.board[r][c + (d)] == '--' and
                self.board[r][c + (d * 2)] == '--' and
                self.board[r][c + (d * 3)][1] == 'R'):
                moves.append(Move((r,c),(r, c + (d * 2)), self.board))


class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    ranksToRows = {"1":7, "2":6 , "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1 , "c":2, "d":3,
                    "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        self.enPassant = False
        self.threats = 0
        self.protects = 0
        self.moves = 0
        self.isMoveCapture = False

        # Determine if a move is a threat
        if self.pieceMoved[1] == 'B':
            self.threats, self.protects, self.moves = self.getBishopThreats(self.endRow, self.endCol, 'b' if self.pieceMoved[0] == 'w' else 'w', board)
        if self.pieceMoved[1] == 'N':
            self.threats, self.protects, self.moves = self.getKnightThreats(self.endRow, self.endCol, 'b' if self.pieceMoved[0] == 'w' else 'w', board)
        if self.pieceMoved[1] == 'R':
            self.threats, self.protects, self.moves = self.getRookThreats(self.endRow, self.endCol, 'b' if self.pieceMoved[0] == 'w' else 'w', board)
        if self.pieceMoved[1] == 'Q':
            rookThreats, rookProtects, rookMoves = self.getRookThreats(self.endRow, self.endCol, 'b' if self.pieceMoved[0] == 'w' else 'w', board)
            bishopThreats, bishopProtects, bishopMoves = self.getBishopThreats(self.endRow, self.endCol, 'b' if self.pieceMoved[0] == 'w' else 'w', board)
            self.threats = rookThreats + bishopThreats
            self.protects = rookProtects + bishopProtects
            self.moves = bishopMoves + rookMoves
        if self.pieceMoved[1] == 'p':
            self.threats, self.protects, self.moves = self.getPawnThreats(self.endRow, self.endCol, 'b' if self.pieceMoved[0] == 'w' else 'w', board)

        if self.pieceCaptured != '--':
            self.isMoveCapture = True

        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True
        if self.pieceMoved[1] == 'p' and (self.endCol != self.startCol) and board[self.endRow][self.endCol] == "--":
            self.enPassant = True

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol * 1

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    #TODO turn all of these into one function
    def getBishopThreats(self, r, c, turn, board):
        threats = 0
        protects = 0
        moves = 0
        dircetions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for direction in dircetions:
            for length in range(1, 8):
                rowVector = direction[0] * length
                colVector = direction[1] * length
                if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                    if board[r + rowVector][c + colVector] != '--':
                        if board[r + rowVector][c + colVector].startswith(turn):
                            threats += 1
                            moves += 1
                            break
                        else:
                            protects += 1
                            moves += 1
                            break
                    else:
                        moves += 1
        return threats, protects, moves

    def getRookThreats(self, r, c, turn, board):
        threats = 0
        protects = 0
        moves = 0
        dircetions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        for direction in dircetions:
            for length in range(1, 8):
                rowVector = direction[0] * length
                colVector = direction[1] * length
                if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                    if board[r + rowVector][c + colVector] != '--':
                        if board[r + rowVector][c + colVector].startswith(turn):
                            threats += 1
                            moves += 1
                            break
                        else:
                            protects += 1
                            moves += 1
                            break
                    else:
                        moves += 1
        return threats, protects, moves

    def getKnightThreats(self, r, c, turn, board):
        threats = 0
        protects = 0
        moves = 0
        dircetions = [(2, 1),(-2, 1),(2, -1),(-2, -1),(1, 2),(-1, 2),(1, -2),(-1, -2)]
        for direction in dircetions:
            for length in range(1, 8):
                rowVector = direction[0] * length
                colVector = direction[1] * length
                if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                    if board[r + rowVector][c + colVector] != '--':
                        if board[r + rowVector][c + colVector].startswith(turn):
                            threats += 1
                            moves += 1
                            break
                        else:
                            protects += 1
                            moves += 1
                            break
                    else:
                        moves += 1
        return threats, protects, moves

    def getPawnThreats(self, r, c, turn, board):
        threats = 0
        protects = 0
        moves = 0
        dircetions = [(-1, 1),(-1, -1)] if turn == 'b' else [(1, 1),(1, -1)]
        for direction in dircetions:
            for length in range(1, 8):
                rowVector = direction[0] * length
                colVector = direction[1] * length
                if r + rowVector <= 7 and r + rowVector >= 0 and c + colVector <= 7 and c + colVector >= 0:
                    if board[r + rowVector][c + colVector] != '--':
                        if board[r + rowVector][c + colVector].startswith(turn):
                            threats += 1
                            moves += 1
                            break
                        else:
                            protects += 1
                            moves += 1
                            break
                    else:
                        moves += 1
        return threats, protects, moves


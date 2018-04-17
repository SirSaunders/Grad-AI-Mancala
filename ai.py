import copy

board = {
    "board": {
        "space": [{
            "type": "mancala",
            "marbles": 0,
            "space_id": 0,
            "player": 1
        },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 1,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 2,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 3,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 4,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 5,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 6,
                "player": 0
            },
            {
                "type": "mancala",
                "marbles": 0,
                "space_id": 7,
                "player": 0
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 8,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 9,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 10,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 11,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 12,
                "player": 1
            },
            {
                "type": "normal",
                "marbles": 4,
                "space_id": 13,
                "player": 1
            }
        ]
    }
}

boardLength = 14
# AI and Human's mancala positions
mancalaAI = 0
mancalaHuman = 7

def go_again_points(move, board):
    landedSpace = board[move[0]]
    if landedSpace['type'] == 'mancala':
        return 30
    return 0


def empty_space_points(move, board):
    landedSpace = board[move[0]]
    if landedSpace['type'] != 'mancala' and landedSpace['marbles'] == 0:
        accrossSpace = board[int((move[0] + (boardLength / 2)) % boardLength)]
        return accrossSpace['marbles'] * 15
    else:
        return 0


def increment_mancala_points(move):
    return 10 * move[1]

# return the player with the higher mancala score and the score itself
def findWinner(board):
    maxScore = 0
    player1Score = board['space'][mancalaHuman]['marbles']
    player2Score = board['space'][mancalaAI]['marbles']
    if player1Score > player2Score:
        maxScore = player1Score
        winner = "Human"
    elif player2Score > player1Score:
        maxScore = player2Score
        winner = "AI"
    else:
        maxScore = player1Score
        winner = "Tie"
    return maxScore, winner

# based on JSON, range values will be (1, 7) or (8, 13)
def isGameDone(board, rangeStart, rangeEnd):
    for i in range(rangeStart, rangeEnd):
        if board['space'][i]['marbles'] != 0:
            return False
    # at this point one side is empty, so there will be a winner (or a tie)
    return True

def getMove(pos, marbles, player, board):
    updatedBoard = copy.deepcopy(board)
    incrementedMancala = 0
    currentPos = pos
    yourSideScore = 0
    updatedBoard[currentPos]['marbles'] = 0
    winnerDetails = None

    for i in range(marbles):
        currentPos = (currentPos + 1) % boardLength
        space = board[currentPos]
        if space['player'] == player:
            yourSideScore += 1
        if (space['type'] == 'mancala'):
            if space['player'] == player:
                incrementedMancala += 1
                updatedBoard[currentPos]['marbles'] += 1
            else:
                currentPos = (currentPos + 1) % boardLength
        else:
            updatedBoard[currentPos]['marbles'] += 1
    
    if isGameDone(board, 1, 7) or isGameDone(board, 8, 13):
        winnerDetails = findWinner(board)

    return currentPos, incrementedMancala, yourSideScore, updatedBoard, winnerDetails

# get a more accurate score of which player is in a better position to win
# include method to get a better "score" of game: 2 * (marbles in mancala) + sum of marbles on your side
def getBetterScore(board):
    # initialized to current mancala marbles count
    player1Score = board['space'][mancalaHuman]['marbles']
    player2Score = board['space'][mancalaAI]['marbles']
    for space in board:
        if space['player'] == 0:
            player1Score += space['marbles']
        if space['player'] == 1:
            player2Score += space['marbles']
    return player1Score, player2Score

def findPoints(moveFromPos, board):
    # print('board')
    # print(board)
    # print('move from')
    # print(moveFromPos)
    moveSpace = board[moveFromPos]
    marbles = moveSpace['marbles']
    # move = getMove(moveSpace['space_id'], marbles, moveSpace['player'], board)
    move = getMove(moveSpace['space_id'], marbles, 0, board)
    incrementMancalaPoints = increment_mancala_points(move)
    goAgainPoints = go_again_points(move, board)
    emptySpacePoints = empty_space_points(move, board)
    yourSideScore = move[2]
    # print('incrementMancalaPoints')
    # print(incrementMancalaPoints)
    # print('goAgainPoints')
    # print(goAgainPoints)
    # print('emptySpacePoints')
    # print(emptySpacePoints)
    # print('yourSideScore')
    # print(yourSideScore)
    # print('move info')
    # print(move)
    # print('total move score')
    return (incrementMancalaPoints + goAgainPoints + emptySpacePoints + yourSideScore), move[3]


def searchMovePoints(board, cnt, pos):
    (points, updatedboard) = findPoints(pos, board)
    bestPoints = 0
    worstPoints = 999999
    if cnt > -1:
        return points
    else:
        if ((cnt + 1) % 2) == 1: #max
            for i in range(1, 7):
                points = searchMovePoints(updatedboard, cnt + 1, i)
                if points > bestPoints:
                    bestPoints = points
            print('best:max')
            print(bestPoints)
            return points + bestPoints
        else:
            for i in range(8, 13):#min
                points = searchMovePoints(updatedboard, cnt + 1, i)
                if points < worstPoints:
                    worstPoints = points
            print('worst:min')
            print(worstPoints)
            return points + worstPoints


def findMove(board):
    bestPoints = 0
    bestMove = 1
    for i in range(1, 7):
        points = searchMovePoints(board['board']['space'], 0, i)
        if points > bestPoints:
            bestPoints = points
            bestMove = i
    return bestMove, bestPoints


if __name__ == '__main__':
    print(findMove(board))
    # print(searchMovePoints(board['board']['space'], 0, 1))

from chalice import Chalice
cors_config = True

app = Chalice(app_name='game-server')








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


def getMove(pos, marbles, player, board):
    updatedBoard = copy.deepcopy(board)
    incrementedMancala = 0
    currentPos = pos
    yourSideScore = 0
    updatedBoard[currentPos]['marbles'] = 0
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

    return currentPos, incrementedMancala, yourSideScore, updatedBoard


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
    if cnt > 4:
        return points
    else:
        if ((cnt + 1) % 2) == 1:  # max
            for i in range(1, 7):
                points = searchMovePoints(updatedboard, cnt + 1, i)
                if points > bestPoints:
                    bestPoints = points
            print('best:max')
            print(bestPoints)
            return points + bestPoints
        else:
            for i in range(8, 13):  # min
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


@app.route('/update_board', methods=['POST'], cors=cors_config)
def updateBoard():
    app.log.debug('json')

    json = app.current_request.json_body
    app.log.debug(json)
    board = json['board']['space']
    json = getMove(4, 4,1, board)[3]


    return json
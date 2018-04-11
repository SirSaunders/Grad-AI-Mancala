from chalice import Chalice

cors_config = True

app = Chalice(app_name='game-server')

import copy



boardLength = 14


def go_again_points(move, board):
    landedSpace = board[move[0]]
    if landedSpace['type'] == 'mancala':
        return 60
    return 0


def empty_space_points(move, board):
    landedSpace = board[move[0]]
    player=board[move[0]]['player']

    if landedSpace['type'] != 'mancala' and landedSpace['marbles'] == 1 and landedSpace['player'] == player:
        accrossSpace = board[int((move[0] + (boardLength / 2)) % boardLength)]
        return accrossSpace['marbles'] * 30
    else:
        return 0


def increment_mancala_points(move):
    return 10 * move[1]


def getMove(pos, marbles, player, board):
    updatedBoard = copy.deepcopy(board)
    incrementedMancala = 0
    currentPos = pos
    yourSideScore = 0
    player=board[pos]['player']
    updatedBoard[currentPos]['marbles'] = 0
    if marbles == 0:
        return pos, 0, 0, board
    for i in range(marbles):
        currentPos = (currentPos + 1) % boardLength
        space = board[currentPos]
        if space['player'] == player:
            yourSideScore += 1
        if space['type'] == 'mancala':
            if space['player'] == player:
                incrementedMancala += 1
                updatedBoard[currentPos]['marbles'] += 1
            else:
                currentPos = (currentPos + 1) % boardLength
                updatedBoard[currentPos]['marbles'] += 1
        else:
            updatedBoard[currentPos]['marbles'] += 1
        landedSpace = updatedBoard[currentPos]
        print(landedSpace)
    if landedSpace['type'] != 'mancala' and landedSpace['marbles'] == 1 and landedSpace['player'] == player:
        accrossSpace = updatedBoard[int((boardLength - currentPos ) % boardLength)]
        #print(accrossSpace)
        if(player == 0):
            updatedBoard[7]['marbles'] += accrossSpace['marbles'] + 1
        else:
            updatedBoard[0]['marbles'] += accrossSpace['marbles'] + 1
        updatedBoard[accrossSpace['space_id']]['marbles'] = 0
        updatedBoard[currentPos]['marbles'] = 0

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

    return (incrementMancalaPoints + goAgainPoints + yourSideScore + emptySpacePoints), move[3]


def searchMovePoints(board, cnt, pos):
    (points, updatedboard) = findPoints(pos, board)
    bestPoints = 0
    worstPoints = 999999
    if cnt > 2:
        return points
    else:
        if ((cnt + 1) % 2) == 1:  # max
            for i in range(1, 7):
                points = searchMovePoints(updatedboard, cnt + 1, i)
                if points > bestPoints:
                    bestPoints = points
            # print('best:max')
            # print(bestPoints)
            return points + bestPoints
        else:
            for i in range(8, 13):  # min
                points = searchMovePoints(updatedboard, cnt + 1, i)
                if points < worstPoints:
                    worstPoints = points
            # print('worst:min')
            # print(worstPoints)
            return points + worstPoints


def findMove(board):
    bestPoints = 0
    bestMove = 1
    for i in range(1, 7):
        if not (board['board']['space'][i]['marbles'] > 0):
            points = -1
        else:
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
    move = json['move']
    landed = getMove(move, board[move]['marbles'], 1, board)
    json = {"board": {
        "space": landed[3]}}
    go_again = False
    if go_again_points(landed, board) > 0:
        go_again = True
    json['go_again'] = go_again
    return json

@app.route('/get_move', methods=['POST'], cors=cors_config)
def updateBoard():
    app.log.debug('json')
    json = app.current_request.json_body
    board = json['board']['space']
    move = findMove(json)
    movePos = move[0]
    landed = getMove(movePos, board[movePos]['marbles'], 0, board)
    json = {"board": {
        "space": landed[3]}}
    go_again = False
    if go_again_points(landed, board) > 0:
        go_again = True
    json['go_again'] = go_again
    print(move)

    return json

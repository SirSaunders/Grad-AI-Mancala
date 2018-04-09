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
        return accrossSpace['marbles'] * 10
    else:
        return 0


def increment_mancala_points(move):
    return 10 * move[1]


def getMove(pos, marbles, player, board):
    incrementedMancala = 0
    currentPos = pos
    yourSideScore = 0
    for i in range(marbles):
        currentPos = (currentPos + 1) % boardLength
        space = board[currentPos]
        if space['player'] == player:
            yourSideScore += 1
        if (space['type'] == 'mancala'):
            if space['player'] == player:
                incrementedMancala += 1
            else:
                currentPos = (currentPos + 1) % boardLength
    return currentPos, incrementedMancala, yourSideScore


def findPoints(moveFromPos, board):
    moveSpace = board[moveFromPos]
    marbles = moveSpace['marbles']
    move = getMove(moveSpace['space_id'], marbles, moveSpace['player'], board)
    incrementMancalaPoints = increment_mancala_points(move)
    goAgainPoints = go_again_points(move, board)
    emptySpacePoints = empty_space_points(move, board)
    yourSideScore = move[2]
    print(incrementMancalaPoints)
    print(goAgainPoints)
    print(emptySpacePoints)
    print(yourSideScore)
    print(move)
    return incrementMancalaPoints + goAgainPoints + emptySpacePoints + yourSideScore


if __name__ == '__main__':
    print(findPoints(3,board['board']['space']))

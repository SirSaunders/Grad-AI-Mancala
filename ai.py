boardLength = 14

def goAgainPoints(move, board):
	landedSpace = board[move[0]]
	if landedSpace['type'] == 'mancala':
		return 30
	return 0

def emptySpacePoints(move, board):
        landedSpace = board[move[0]]
        if landedSpace['marbles'] == 0:
               	accrossSpace= board[(move[0] + (boardLength / 2)) % boardLength]
		return accrossSpace['marbles'] * 10
	return 0

def incrementMancalaPoints(move, board):
	return 10*move[1]

def findPoints(moveFromPos, board):
        moveSpace = board[moveFromPos]
        marbles = moveSpace['marbles']
        move = getMove(moveSpace['space_id'],marbles,moveSpace['player'],board)
	incrementMancalaPoints = incrementMancalaPoints(move)
	goAgainPoints = goAgainPoints(move,board)
	emptySpacePoints = emptySpacePoints(move,board)
	yourSideScore = move[2]


def getMove(pos, marbles, player, board)
	incrementedMancala = 0
	currentPos = pos
	yourSideScore = 0
	for(i in range(0, marbles):
		currentPos = (currentPos + 1) % boardLength
		space = board[currentPos]
		if space['player'] == player:
			yourSideScore += 1
		if(space['type'] = 'mancala'):
			if space['player'] == player:
				incrementedMancala += 1
			else:
				currentPos = (currentPos + 1) % boardLength
	return (currentPos, incrementedMancala, yourSideScore)

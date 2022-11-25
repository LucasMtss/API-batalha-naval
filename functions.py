import random

ships = {
    'porta-avioes': 5,
    'cruzador': 4,
    'contratorpedeiro': 3,
    'fragata': 2,
    'submarino': 1
}

def getInitialMatrix():
  return [
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
            ['0', '0','0','0','0','0','0','0','0','0'],
        ]

def generateRandomCoord():
    return (random.randint(0,9), random.randint(0,9))

def checkPosition(x, y, matriz):
    if x > 9 or y > 9 or x < 0  or y < 0:
        return False
    return matriz[x][y] == '0'
 

def checkIfIsPossibleCreateSubmarine(x, y, matriz):
    return checkPosition(x,y, matriz)

def checkIfIsPossibleCreateFrigate(x, y, matriz):
    return checkPosition(x,y, matriz) and checkPosition(x,y+1, matriz) 

def checkIfIsPossibleCreateDestroyer(x, y, matriz):
    return checkPosition(x,y, matriz) and checkPosition(x,y+1, matriz) and checkPosition(x,y+2, matriz) 

def checkIfIsPossibleCreateCruiser(x, y, matriz):
    return checkPosition(x,y, matriz) and checkPosition(x,y+1, matriz) and checkPosition(x,y+2, matriz) and checkPosition(x,y+3, matriz) 

def checkIfIsPossibleCreateAircraftCarrier(x, y, matriz):
    return checkPosition(x,y, matriz) and checkPosition(x,y+1, matriz) and checkPosition(x,y+2, matriz) and checkPosition(x+1,y+1, matriz) and checkPosition(x+2,y+1, matriz)

def createBattleshipGame():
    matriz = getInitialMatrix()
    # Porta aviões
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateAircraftCarrier(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeAircraftCarrier(coordX, coordY, matriz)

    # Cruzador
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateCruiser(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeCruiser(coordX, coordY, matriz)

    # Contratorpedeiro
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateDestroyer(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeDestroyer(coordX, coordY, matriz)

    # Fragata
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateFrigate(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeFrigate(coordX, coordY, matriz)

     # Fragata
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateFrigate(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeFrigate(coordX, coordY, matriz)

    # Submarino
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateSubmarine(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeSubmarine(coordX, coordY, matriz)

    # Submarino
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateSubmarine(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeSubmarine(coordX, coordY, matriz)

    # Submarino
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateSubmarine(coordX, coordY, matriz):
        coordX, coordY = generateRandomCoord() 
    writeSubmarine(coordX, coordY, matriz)

    return matriz


def writeSubmarine(x,y, matriz):
    matriz[x][y] = 'S'

def writeFrigate(x,y, matriz):
    matriz[x][y] = 'F'
    matriz[x][y+1] = 'F'

def writeDestroyer(x,y, matriz):
    matriz[x][y] = 'D'
    matriz[x][y+1] = 'D'
    matriz[x][y+2] = 'D'

def writeCruiser(x,y, matriz):
    matriz[x][y] = 'C'
    matriz[x][y+1] = 'C'
    matriz[x][y+2] = 'C'
    matriz[x][y+3] = 'C'

def writeAircraftCarrier(x,y, matriz):
    matriz[x][y] = 'A'
    matriz[x][y+1] = 'A'
    matriz[x][y+2] = 'A'
    matriz[x+1][y+1] = 'A'
    matriz[x+2][y+1] = 'A'

import random

ships = {
    'porta-avioes': 5,
    'cruzador': 4,
    'contratorpedeiro': 3,
    'fragata': 2,
    'submarino': 1
}

matriz = [
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

def checkPosition(x, y):
    if x > 9 or y > 9 or x < 0  or y < 0:
        return False
    return matriz[x][y] == '0'
 

def checkIfIsPossibleCreateSubmarine(x, y):
    return checkPosition(x,y)

def checkIfIsPossibleCreateFrigate(x, y):
    return checkPosition(x,y) and checkPosition(x,y+1) 

def checkIfIsPossibleCreateDestroyer(x, y):
    return checkPosition(x,y) and checkPosition(x,y+1) and checkPosition(x,y+2) 

def checkIfIsPossibleCreateCruiser(x, y):
    return checkPosition(x,y) and checkPosition(x,y+1) and checkPosition(x,y+2) and checkPosition(x,y+3) 

def checkIfIsPossibleCreateAircraftCarrier(x, y):
    return checkPosition(x,y) and checkPosition(x,y+1) and checkPosition(x,y+2) and checkPosition(x+1,y+1) and checkPosition(x+2,y+1)

def createBattleshipGame():
    # Porta aviões
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateAircraftCarrier(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeAircraftCarrier(coordX, coordY)

    # Cruzador
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateCruiser(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeCruiser(coordX, coordY)

    # Contratorpedeiro
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateDestroyer(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeDestroyer(coordX, coordY)

    # Fragata
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateFrigate(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeFrigate(coordX, coordY)

     # Fragata
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateFrigate(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeFrigate(coordX, coordY)

    # Submarino
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateSubmarine(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeSubmarine(coordX, coordY)

    # Submarino
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateSubmarine(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeSubmarine(coordX, coordY)

    # Submarino
    coordX, coordY = generateRandomCoord() 
    while not checkIfIsPossibleCreateSubmarine(coordX, coordY):
        coordX, coordY = generateRandomCoord() 
    writeSubmarine(coordX, coordY)


def writeSubmarine(x,y):
    matriz[x][y] = 'S'

def writeFrigate(x,y):
    matriz[x][y] = 'F'
    matriz[x][y+1] = 'F'

def writeDestroyer(x,y):
    matriz[x][y] = 'D'
    matriz[x][y+1] = 'D'
    matriz[x][y+2] = 'D'

def writeCruiser(x,y):
    matriz[x][y] = 'C'
    matriz[x][y+1] = 'C'
    matriz[x][y+2] = 'C'
    matriz[x][y+3] = 'C'

def writeAircraftCarrier(x,y):
    matriz[x][y] = 'A'
    matriz[x][y+1] = 'A'
    matriz[x][y+2] = 'A'
    matriz[x+1][y+1] = 'A'
    matriz[x+2][y+1] = 'A'

for linha in matriz:
    print(linha)

print('\n\n')
createBattleshipGame()
for linha in matriz:
    print(linha)
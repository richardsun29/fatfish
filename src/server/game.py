INIT_PLAYER_SIZE = 1
LEFT = 0
RIGHT = 1

class Fish:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.image = 0
        
class Player(Fish):
    def __init__(self, x, y, id):
        super(Player, self).__init__(x, y, INIT_PLAYER_SIZE)
        self.id = id
        
    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY
        
class Nonplayer(Fish):
    def __init__(self, y, size, speed, direction):
        if direction == LEFT:
            x = 100
        elif direction == RIGHT:
            x = 0
        super(Nonplayer, self).__init__(x, y, size)
        self.speed = speed
        self.direction = direction
        
    def move(self):
        if self.direction == LEFT:
            self.x -= 1
        elif self.direction == RIGHT:
            self.x += 1
            
class Game:
    def __init__(self):
        self.players = []
        self.nonplayers = []
        self.playerMovements = {}
        
    def create_player(self, x, y, id):
        p = Player(x, y, id)
        self.players.append(p)
        
    def remove_player(self, id):
        for i, player in enumerate(self.players):
            if player.id == id:
                del self.players[i]
                break
                
    def create_nonplayer(self, y, size, speed, direction):
        np = Nonplayer(y, size, speed, direction)
        self.nonplayers.append(np)
        
    def get_fish(self):
        return self.players, self.nonplayers
        
    def move_player(self, id, deltaX, deltaY):
            self.playerMovements[id] = (deltaX, deltaY)

    def move_loop(self):
        for nonplayer in self.nonplayers:
            nonplayer.move()
        self.nonplayers = [nonplayer for nonplayer in self.nonplayers if nonplayer.x >= -50 and nonplayer.x <= 150]
        for player in self.players:
            if player.id in self.playerMovements:
                deltaX = self.playerMovements[player.id][0]
                deltaY = self.playerMovements[player.id][1]
                player.move(deltaX, deltaY)
            #TODO: collision check
        self.playerMovements = {}

def test1():
    g = Game()
    g.create_player(50, 50, 1)
    g.create_player(50, 50, 2)
    g.create_nonplayer(20, 3, 1, LEFT)
    g.move_player(1, 5, 0)
    g.move_player(2, 0, -10)
    for i in range(300):
        g.move_loop()
    players, nonplayers = g.get_fish()
    for player in players:
        print("PLAYER")
        print("x:", player.x)
        print("y:", player.y)
        print("size:", player.size)
        print("id:", player.id)
    for nonplayer in nonplayers:
        print("NONPLAYER")
        print("x:", nonplayer.x)
        print("y:", nonplayer.y)
        print("size:", nonplayer.size)
        print("speed:", nonplayer.speed)
        print("direction:", nonplayer.direction)
        
def test2():
    g = Game()
    g.create_nonplayer(20, 3, 1, LEFT)
    g.create_nonplayer(20, 3, 1, LEFT)
    g.create_nonplayer(20, 2, 1, LEFT)
    g.nonplayers[0].x = -100
    g.nonplayers[1].x = -100
    g.move_loop()
    
#test2()
    
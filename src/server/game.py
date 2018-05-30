INIT_PLAYER_SIZE = 1
PLAYER_SPEED = 5
LEFT = 0
RIGHT = 1

class Fish:
    def __init__(self, id, x, y, size):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.image = 0
        
class Player(Fish):
    def __init__(self, id, name, x, y):
        super(Player, self).__init__(id, x, y, INIT_PLAYER_SIZE)
        self.name = name
        
    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY

    def __repr__(self):
        return 'Player (id = %d, x = %d, y = %d)' % (self.id, self.x, self.y)
        
class Nonplayer(Fish):
    def __init__(self, id, y, size, speed, direction):
        if direction == LEFT:
            x = 800
        elif direction == RIGHT:
            x = 0
        super(Nonplayer, self).__init__(id, x, y, size)
        self.speed = speed
        self.direction = direction
        
    def move(self):
        if self.direction == LEFT:
            self.x -= 1
        elif self.direction == RIGHT:
            self.x += 1

    def __repr__(self):
        return 'Nonplayer (x = %d, y = %d)' % (self.x, self.y)
            
class Game:
    def __init__(self):
        self.players = []
        self.nonplayers = []
        self.playerMovements = {}
        self.next_id = 0

    def get_new_id(self):
        self.next_id += 1
        return self.next_id

    def create_player(self, name, x, y):
        p = Player(self.get_new_id(), name, x, y)
        self.players.append(p)
        return p.id
        
    def remove_player(self, id):
        for i, player in enumerate(self.players):
            if player.id == id:
                del self.players[i]
                break
                
    def create_nonplayer(self, y, size, speed, direction):
        np = Nonplayer(self.get_new_id(), y, size, speed, direction)
        self.nonplayers.append(np)
        
    def get_fish(self):
        return self.players, self.nonplayers
        
    def move_player(self, id, deltaX, deltaY):
            self.playerMovements[id] = (deltaX * PLAYER_SPEED, deltaY * PLAYER_SPEED)

    def move_loop(self):
        for nonplayer in self.nonplayers:
            nonplayer.move()
        self.nonplayers = [nonplayer for nonplayer in self.nonplayers if nonplayer.x >= -400 and nonplayer.x <= 1200]
        for player in self.players:
            if player.id in self.playerMovements:
                deltaX = self.playerMovements[player.id][0]
                deltaY = self.playerMovements[player.id][1]
                player.move(deltaX, deltaY)
            #TODO: collision check

def test1():
    g = Game()
    g.create_player(50, 50)
    g.create_player(50, 50)
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
    

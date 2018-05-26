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
        
    def create_player(self, x, y, id):
        p = Player(x, y, id)
        self.players.append(p)
        
    def remove_player(self, id):
        for i in range(len(self.players)):
            if self.players[i].id == id:
                del self.players[i]
                break
                
    def create_nonplayer(self, y, size, speed, direction):
        np = Nonplayer(y, size, speed, direction)
        self.nonplayers.append(np)
        
    def get_fish(self):
        return self.players, self.nonplayers

    def move_loop(self, playerMovements):
        for nonplayer in self.nonplayers:
            nonplayer.move()
        for player in self.players:
            if player.id in playerMovements:
                deltaX = playerMovements[player.id][0]
                deltaY = playerMovements[player.id][1]
                player.move(deltaX, deltaY)
            #TODO: collision check

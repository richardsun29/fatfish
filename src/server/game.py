INIT_PLAYER_SIZE = 1
LEFT = 0
RIGHT = 1

players = []
nonplayers = []

class Fish:
    def __init__(self, size, x, y):
        self.size = size
        self.x = x
        self.y = y
        self.image = 0
        
    def move(self):
        pass
        
class Player(Fish):
    def __init__(self, x, y):
        super(Player, self).__init__(INIT_PLAYER_SIZE, x, y)
        players.append(self)
        
    def move(self):
        pass
        
class Nonplayer(Fish):
    def __init__(self, size, y, speed, direction):
        if direction == LEFT:
            x = 100
        elif direction == RIGHT:
            x = 0
        super(Nonplayer, self).__init__(size, x, y)
        self.speed = speed
        self.direction = direction
        nonplayers.append(self)
        
    def move(self):
        if self.direction == LEFT:
            self.x -= 1
        elif self.direction == RIGHT:
            self.x += 1

            
def move_loop():
    for nonplayer in nonplayers:
        nonplayer.move()
    for player in players:
        player.move()
        #TODO: collision check

"""        
p = Player(50, 50)
np = Nonplayer(5, 20, 10, LEFT)
print(p.x)
print(p.y)
print(np.x)
print(np.y)
move_loop()
print(p.x)
print(p.y)
print(np.x)
print(np.y)
"""
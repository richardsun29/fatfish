import math
import random

INIT_PLAYER_SIZE = 5
PLAYER_SPEED = 5
LEFT = 0
RIGHT = 1
MAX_NONPLAYERS = 10

#screen size: 800 x 544
SCREEN_X = 800
SCREEN_Y = 544
X_BOUND_MIN = SCREEN_X * -0.5
X_BOUND_MAX = SCREEN_X * 1.5

class Fish:
    def __init__(self, id, x, y, size):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        
    def size_to_length(self):
        return 4 + math.sqrt(self.size) * 3
        
    def size_to_width(self):
        return self.size_to_length() * 3/4
        
    def get_fish_box(self):
        length = self.size_to_length()
        width = self.size_to_width()
        min_x = self.x - length/2
        max_x = self.x + length/2
        min_y = self.y - width/2
        max_y = self.y + width/2
        return (min_x, max_x), (min_y, max_y)
        
    def collision_check(self, fish):
        if self is fish:
            return False
            
        fish_box1 = self.get_fish_box()
        fish_box2 = fish.get_fish_box()
        
        x1 = fish_box1[0][0]
        x2 = fish_box1[0][1]
        x3 = fish_box2[0][0]
        x4 = fish_box2[0][1]
        
        y1 = fish_box1[1][0]
        y2 = fish_box1[1][1]
        y3 = fish_box2[1][0]
        y4 = fish_box2[1][1]
        
        collision = False
        if x1 <= x4 and x3 <= x2 and y1 <= y4 and y3 <= y2:
            collision = True
            
        return collision
        
class Player(Fish):
    def __init__(self, id, name):
        x = random.randint(50, SCREEN_X - 50)
        y = random.randint(50, SCREEN_Y - 50)
        super(Player, self).__init__(id, x, y, INIT_PLAYER_SIZE)
        self.name = name
        self.direction = RIGHT
        self.is_dead = False

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
        if delta_x > 0:
            self.direction = RIGHT
        elif delta_x < 0:
            self.direction = LEFT

    def grow(self, food_size):
        self.size += food_size

    def __repr__(self):
        return 'Player (id = %d, x = %d, y = %d)' % (self.id, self.x, self.y)
        
class Nonplayer(Fish):
    def __init__(self, id):
        y = random.randint(50, SCREEN_Y - 50)
        size = self.rand_size()
        speed = 3 # TODO: make this random?
        direction = random.choice([LEFT, RIGHT])
        if direction == LEFT:
            x = random.randint(SCREEN_X, X_BOUND_MAX)
        elif direction == RIGHT:
            x = random.randint(X_BOUND_MIN, 0)
        super(Nonplayer, self).__init__(id, x, y, size)
        self.speed = speed
        self.direction = direction

    def rand_size(self):
        # TODO: make this better
        if random.random() < 0.3:
            return random.randint(100, 1000)
        else:
            return random.randint(1, 8)
        
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
        self.player_movements = {}    #key: id, value: (delta x, delta y)
        self.player_growths = {}      #key: id, value: size of fish eaten
        #self.player_deaths = set()    #dead player fish IDs
        self.nonplayer_deaths = set() #dead nonplayer fish IDs
        self.next_id = 0

        # generate nonplayer fish
        self.create_nonplayers()

    def get_new_id(self):
        self.next_id += 1
        return self.next_id

    def create_player(self, name):
        p = Player(self.get_new_id(), name)
        self.players.append(p)
        return p.id
        
    def remove_player(self, id):
        for i, player in enumerate(self.players):
            if player.id == id:
                del self.players[i]
                break
                
    def create_nonplayers(self):
        while len(self.nonplayers) < MAX_NONPLAYERS:
            np = Nonplayer(self.get_new_id())
            self.nonplayers.append(np)
        
    def remove_nonplayer(self, id):
        for i, nonplayer in enumerate(self.nonplayers):
            if nonplayer.id == id:
                del self.nonplayers[i]
                break

    def is_player_dead(self, player_id):
        for p in self.players:
            if p.id == player_id:
                return p.is_dead
        return False

    def get_game_state(self, player_id):
        if self.is_player_dead(player_id):
            return {
                'id': player_id,
                'status': 'dead',
                'players': [],
                'nonplayers': [],
            }

        return {
            'id': player_id,
            'status': 'alive',
            'players': [{
                'id': p.id,
                'name': p.name,
                'x': p.x,
                'y':p.y,
                'size': p.size,
                'direction': p.direction,
            } for p in self.players],
            'nonplayers': [{
                'id': p.id,
                'x': p.x,
                'y':p.y,
                'size': p.size,
                'direction': p.direction,
            } for p in self.nonplayers],
        }
        
    def move_player(self, id, delta_x, delta_y):
            self.player_movements[id] = (delta_x * PLAYER_SPEED, delta_y * PLAYER_SPEED)

    def move_loop(self):
        #all nonplayers move
        for nonplayer in self.nonplayers:
            nonplayer.move()
            
        #remove nonplayers that are far off screen
        self.nonplayers = [nonplayer for nonplayer in self.nonplayers if nonplayer.x >= X_BOUND_MIN and nonplayer.x <= X_BOUND_MAX]
        
        #players move
        for player in self.players:
            if not player.is_dead:
                if player.id in self.player_movements:
                    delta_x = self.player_movements[player.id][0]
                    delta_y = self.player_movements[player.id][1]
                    player.move(delta_x, delta_y)
        #self.player_movements = {}
        
        #collision check
        for player in [p for p in self.players if not p.is_dead]:
            for player2 in [p for p in self.players if not p.is_dead]:
                if player.collision_check(player2) and player.size > player2.size:
                    if player.id not in self.player_growths:
                        self.player_growths[player.id] = 0
                    self.player_growths[player.id] += player2.size
                    #self.player_deaths.add(player2.id)
                    player2.is_dead = True
            for nonplayer in self.nonplayers:
                if player.collision_check(nonplayer):
                    if player.size > nonplayer.size:
                        if player.id not in self.player_growths:
                            self.player_growths[player.id] = 0
                        self.player_growths[player.id] += nonplayer.size
                        self.nonplayer_deaths.add(nonplayer.id)
                    elif player.size < nonplayer.size:
                        #self.player_deaths.add(player.id)
                        player.is_dead = True
                        
        #players grow
        for player in self.players:
            if player.id in self.player_growths:
                player.grow(self.player_growths[player.id])
        self.player_growths = {}

        #server.py cleans up players
        #self.players = [player for player in self.players if player.id not in self.player_deaths]
        #self.player_deaths = set()

        #nonplayers die
        self.nonplayers = [nonplayer for nonplayer in self.nonplayers if nonplayer.id not in self.nonplayer_deaths]
        self.nonplayer_deaths = set()

        # respawn nonplayers
        self.create_nonplayers()


def test_collision():
    p1 = Player(1, "kaitlyne", 20, 30)
    p2 = Player(2, "richard", 20, 31)
    print(p1.collision_check(p2)) #true
    p3 = Player(3, "kaitlyne", 50, 50)
    p4 = Player(4, "richard", 500, 500)
    print(p3.collision_check(p4)) #false
    
#test_collision()

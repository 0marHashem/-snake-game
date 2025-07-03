import pygame , sys , random , time
from pygame.math import Vector2
# -------------------------- Game Settings --------------------------
# Grid System
CELL_SIZE = 20 # so number of CELLS is 30
GRID_WIDTH = 30 # 30 row
GRID_HEIGHT = 30 # 30 column
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS =60

# -------------------------- CLASSES --------------------------

# -------------------------- SNAKE --------------------------
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,5) , Vector2(4,5) , Vector2(3,5)]
        self.direction = Vector2(1,0)
    
    def move(self):
        self.new_head = self.direction + self.body[0] # so it will be (6,5)
        self.body.insert(0,self.new_head) # list is [ (6,5) ,(5,5) , (4,5) , (3,5)])
        self.body.pop()
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.new_direction(Vector2(1,0))
        elif keys[pygame.K_LEFT]:
            self.new_direction(Vector2(-1,0))
        elif keys[pygame.K_DOWN]:
            self.new_direction(Vector2(0,1))
        elif keys[pygame.K_UP]:
            self.new_direction(Vector2(0,-1))
    def draw(self , surface):
        for block in self.body:
            block_rect = pygame.Rect(block.x*CELL_SIZE , block.y*CELL_SIZE , CELL_SIZE , CELL_SIZE) # x,y in this way because of grid sys
            pygame.draw.rect(surface , "green" , block_rect)

    def new_direction(self , new_dir):
        '''This function prevents weird movement'''
        if new_dir + self.direction != Vector2(0,0): # (1,0) + (-1,0) NOT ALLOWED TO CHANGE DIR LIKE THIS
            self.direction = new_dir

# -------------------------- FRUIT --------------------------
class FRUIT:
    def __init__(self , snake_body):
        while True:
            pos = Vector2(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                break
        self.position = pos

    def draw(self, surface):
        img = pygame.transform.scale( pygame.image.load("./Graphics/apple.png") , (CELL_SIZE,CELL_SIZE))
        rect = pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        surface.blit(img , rect)


# -------------------------- GAME --------------------------
class GAME:
    def __init__(self):
        # GAME CORE
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        pygame.display.set_caption("Snake Game")
        self.DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()
        self.is_game_over = False
        # Snake Move 
        self.snake_move_timer = 0    
        self.snake_move_delay = 100   

    def reset(self):
        self.snake = SNAKE()
        self.fruits = [FRUIT(self.snake.body) for _ in range(5)] # make 5 fruits
        self.seconds = 0
        self.apples = 0
        # score
        self.start_time = time.time()

    def game_over(self):
        self.is_game_over = True
        gm = self.font.render("GAME OVER", True, "white")
        st = self.font.render("Press SPACE to restart", True, "white")
        self.DISPLAY_SURFACE.blit(gm, (50, 150))
        self.DISPLAY_SURFACE.blit(st, (50, 250))
        
    def eat_check(self):
        for fruit in self.fruits.copy(): 
            if self.snake.body[0] == fruit.position:
                self.snake.body.append(self.snake.body[-1] + Vector2(self.snake.direction))
                self.fruits.remove(fruit)
                self.snake_move_delay = max(50, self.snake_move_delay - 2) # Speed up
                self.apples += 1
                self.fruits.append(FRUIT(self.snake.body)) # new instance to new random position to be drown

    def handle_losing(self):
        head = self.snake.body[0]
        if head.x < 0 or head.x >= GRID_WIDTH or head.y < 0 or head.y >= GRID_HEIGHT:
            self.game_over()
        if head in self.snake.body[1:]:
            self.game_over()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.DISPLAY_SURFACE, (40, 40, 40), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.DISPLAY_SURFACE, (40, 40, 40), (0, y), (SCREEN_WIDTH, y))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if  event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.is_game_over:
                            self.reset()
                            self.is_game_over = False

            self.DISPLAY_SURFACE.fill("black")
            self.draw_grid()
            dt = self.clock.tick(FPS)  
            self.snake_move_timer += dt
            if not self.is_game_over:
                self.time2 = time.time()
                self.seconds = self.time2 - self.start_time
                
                self.snake.handle_input()
                if self.snake_move_timer >= self.snake_move_delay:
                    self.snake.move()
                    self.snake_move_timer = 0

                self.snake.draw(self.DISPLAY_SURFACE)
                for fruit in self.fruits:
                    fruit.draw(self.DISPLAY_SURFACE)    

                self.eat_check()
            
            self.score = self.font.render(f"SCORE : {round(self.seconds)}", True, "white")
            self.apples_score = self.font.render(f"Apples : {self.apples}", True, "white")
            self.handle_losing()
            self.DISPLAY_SURFACE.blit(self.score, (10, 10))
            self.DISPLAY_SURFACE.blit(self.apples_score, (SCREEN_WIDTH-190, 10))
            pygame.display.update()

game = GAME()
if __name__ == '__main__':
    game.run()
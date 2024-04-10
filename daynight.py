import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 600, 600
GRID_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (131, 135, 141)
GRAY = (200, 200, 200)
BLUE = (0, 0, 139)

#creates a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Bounce Game")

#fills grid with arrays of arrays. Each filled with gray
grid = [[GRAY for _ in range(WIDTH // GRID_SIZE)] for _ in range(HEIGHT // GRID_SIZE)]
lines_toggle = False
#we can draw lines across the screen
#size note pumping images in is cool as well :>

#so basically. Make a 2d grid. Lets say each grid is 30x30
#we make our screen, and then we check the point of the ball. We get that value and divide it by 30, on both x and y
#both x and y now fit within 0-29. oh hey, thats our grid. Check if the center value / 30 is in our grid, check its current color
#if its wrong, swap it, and then change the direction of the ball
#done


for y in range(len(grid)):
    for x in range(len(grid[0])):
        if x < len(grid[0]) // 2:
            grid[y][x] = WHITE
        else:
            grid[y][x] = BLACK

ball_radius = 12
ball_white = pygame.Rect(WIDTH // 4, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
ball_black = pygame.Rect(3 * WIDTH // 4, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
ball_white_speed = [random.choice([-4,4]), random.choice([-4,4])]
ball_black_speed = [random.choice([-4,4]), random.choice([-4,4])]

def wall_bounce(ball, speed):
    if ball.left < 0 or ball.right > WIDTH:
        speed[0] *= -1
    if ball.top < 0 or ball.bottom > HEIGHT:
        speed[1] *= -1

def check_square_bounce(ball, speed, colour):
    grid_x = min(max(ball.centerx // GRID_SIZE, 0), len(grid[0]) - 1)
    grid_y = min(max(ball.centery // GRID_SIZE, 0), len(grid[0]) - 1)
    #the math reduces it down to 0-num blocks-1
    #print(white_grid_y)
    if grid[grid_y][grid_x] != colour:
        # the ball has collided with a black square
        # check which side of the square the ball is on
        dx = ball.centerx - grid_x * GRID_SIZE - GRID_SIZE / 2
        dy = ball.centery - grid_y * GRID_SIZE - GRID_SIZE / 2
        if (dx == -GRID_SIZE//2 or dx == GRID_SIZE//2 - 1) and (dy == -GRID_SIZE//2 or dy == GRID_SIZE//2 - 1):
            speed[0] *= -1
            speed[1] *= -1
        elif dx == -GRID_SIZE//2 or dx == GRID_SIZE//2 - 1:
            speed[0] *= -1
        else:
            speed[1] *= -1

        if grid[grid_y][grid_x] == WHITE:
            grid[grid_y][grid_x] = BLACK
        else:
            grid[grid_y][grid_x] = WHITE

#MAIN LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                lines_toggle = not lines_toggle

    ball_white = ball_white.move(ball_white_speed)
    ball_black = ball_black.move(ball_black_speed)

    check_square_bounce(ball_white, ball_white_speed, WHITE)
    check_square_bounce(ball_black, ball_black_speed, BLACK)

    wall_bounce(ball_white, ball_white_speed)
    wall_bounce(ball_black, ball_black_speed)

    screen.fill(GRAY)
    #constantly refresh and redraw screen, vv important
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.circle(screen, BLACK, ball_white.center, ball_radius)
    pygame.draw.circle(screen, WHITE, ball_black.center, ball_radius)

    #draw lines
    #step of tile size, start at tile size

    if lines_toggle:
        for x in range(GRID_SIZE, WIDTH, GRID_SIZE):
            #START POSITION IS COORDS, X,0, THEN END POSITION COORS
            pygame.draw.line(screen, BLUE, (x, 0), (x, HEIGHT))
        for y in range(GRID_SIZE, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, BLUE, (0, y), (WIDTH, y))  
    

    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Day: {sum(row.count(WHITE) for row in grid)} | Night: {sum(row.count(BLACK) for row in grid)}",
                       True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(144)

pygame.quit()
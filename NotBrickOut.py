import pygame, sys
from random import randrange

def player_mov():
    #  Update player/paddle position based on velocity
    player.x += player_vx
    #  Collision constraints to prevent the player form going out of bounds
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_dimx:
        player.right = screen_dimx


def ball_mov():
    global ball_vx, ball_vy, blocks, lives, ball_locked, player_vx
    #  If the spacebar key has not been pressed yet, lock the ball's position
    #  to the paddle's movement
    if ball_locked:
        ball.x = player.x + 50
        ball.y = screen_dimy - 60
    #  code for animating the ball once it has been launched
    else:
        #  If the ball hits the bottom of the screen, subtract a life from the player.
        #  AND: Set ball_locked to true, which locks the bal to the player's position on the next frame.
        #  AND set initial velocity of the ball to 0.
        if ball.bottom >= screen_dimy - 1:
            lives -= 1
            ball_locked = True
            ball_vx = 0
            ball_vy = 0
        #  Check collisions with sides of the screen that aren't in the death plane.
        if ball.top <= 1:
            ball.top = 1
            ball_vy *= -1
        if ball.left <= 1:
            ball_vx *= -1
            ball.x = 2
        if ball.right >= screen_dimx - 1:
            ball.right = screen_dimx - 2
            ball_vx *= -1
        #  If the ball collides with the paddle, reverse the velocity in the y direction.
        if ball.colliderect(player):
            ball_vy *= -1
            ball_vx += (player_vx/4)

        for block in blocks:
            #  Collision checking with each block
            if ball.colliderect(block):
                ball_vy += .2
                ball_vx += .2
                ball_vy *= -1
                ball_vx *= -1
                blocks.remove(block)
        #  Add gravity to force the ball downwards if it hits nothing.
        if ball_vy < 9.8:
            ball_vy += .098
        elif ball_vy > 9.8:
            ball_vy = 9.8
        #  Velocity limiter. Stops the ball from going too fast for the player.
        if ball_vx > 8:
            ball_vx = 8

        #  Update the ball's position in respect to its velocity
        ball.x += ball_vx
        ball.y += ball_vy


pygame.init()

print(pygame.font.get_fonts())
clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 30)
liv_font = pygame.font.SysFont('calibri', 25)

screen_dimx = 720
screen_dimy = 480
screen_leftx = -15
screen_rightx = 15
screen_topy = -15
screen_bottomy = 15
lives = 2


screen = pygame.display.set_mode((screen_dimx, screen_dimy))
pygame.display.set_caption("Bootleg Brickout!")

blocks = []
for j in range(25, screen_dimx, 100):
    for i in range(25, int(screen_dimy/2) - 75, 26):
        blocks.append(pygame.Rect(j, i, 75, 25))

ball = pygame.Rect(screen_dimx/2 - 10, screen_dimy - 60, 20, 20)
player = pygame.Rect(screen_dimx/2 - 60, screen_dimy - 20, 120, 10)

bg_color = pygame.Color('LightSlateGray')

ball_vx = 0
ball_vy = 0
player_vx = 0
ball_locked = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_vx += 8.5
            if event.key == pygame.K_LEFT:
                player_vx -= 8.5
            if event.key == pygame.K_SPACE:
                if ball_locked:
                    ball_locked = False
                    ball_vx = -5
                    ball_vy = -5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_vx -= 8.5
            if event.key == pygame.K_LEFT:
                player_vx += 8.5
    
    
    #  If the game is not over,
    if lives > -1:
        #  Call functions that handle the player and ball's movement.
        ball_mov()
        player_mov()

    #  Fill the screen. "Erase" the last frame.
    screen.fill("black")
    pygame.draw.aaline(screen, pygame.Color("grey"), (0, screen_dimy - 80), (screen_dimx, screen_dimy - 80))
    pygame.draw.rect(screen, bg_color, player)
    #  Draw each existing block.
    for block in blocks:
        pygame.draw.rect(screen, (25, 152, 200), block)
    #  Draw the ball.
    pygame.draw.ellipse(screen, pygame.Color("red"), ball)
    
    #  Display the "start game" text.
    if ball_locked and lives == 2:
        startText = liv_font.render("Press 'spacebar' to start the game!", True, 'white')
        text_rect = startText.get_rect()
        text_x = (screen_dimx - (screen_dimx *.75)) 
        text_y = (screen_dimy - (screen_dimx * .2))
        screen.blit(startText, [text_x, text_y])
    
    #  Display lives remaining.
    text = liv_font.render("Lives: " + str(lives+1), True, 'white')
    text_rect = text.get_rect()
    text_x = (screen_dimx - text_rect.width / 2) - 50
    text_y = (screen_dimy - text_rect.height / 2) - 35
    screen.blit(text, [text_x, text_y])
    
    

    #  If the game over state is triggered, Move the ball off screen and
    #  display the game over, dude text until the game is closed.
    if lives < 0:
        ball.x = -50
        text = font.render("Game Over, Dude!", True, 'white')
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])


    pygame.display.flip()
    clock.tick(60)

# imports
import pygame
import random

# set variables
size = (500, 300)
p1score = p2score = 0

# ball variables
ball_p1_start = ((size[0] / 5 * 3), (size[1] / 2))
ball_p2_start = ((size[0] / 5 * 2), (size[1] / 2))
ball_x_vel = 0
ball_x_acc = 1
ball_y_vel = 0
ball_y_acc = 1
ball_size = (10, 10)
hits = 0

# paddle variables
paddle_size = (10, 40)
paddle1_start = ((size[0] / 9 * 8), (size[1] / 2 - (paddle_size[1] / 2)))
paddle2_start = ((size[0] / 9), (size[1] / 2 - (paddle_size[1] / 2)))
paddle_y_vel = 5

# colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 20)

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyPong")

# font
font = pygame.font.Font(None, 50)
p2_font_pos = ((size[0] / 7) * 2, size[1] / 6)
p1_font_pos = ((size[0] / 7) * 5, size[1] / 6)

# flags
move_ball = False
close_window = False
p1_start = True
move_up_p1 = False
move_down_p1 = False
move_up_p2 = False
move_down_p2 = False
ai_control1 = False
ai_control2 = False

# ball, midline, and paddles
ball = pygame.Rect(ball_p1_start, ball_size) 
paddle1 = pygame.Rect(paddle1_start, paddle_size)
paddle2 = pygame.Rect(paddle2_start, paddle_size)

# sounds
beep1 = pygame.mixer.Sound("Assets\\beep1.wav")
beep2 = pygame.mixer.Sound("Assets\\beep2.wav")
boop1 = pygame.mixer.Sound("Assets\\boop1.wav")
boop2 = pygame.mixer.Sound("Assets\\boop2.wav")

# drawing and event handling
while close_window == False:
	# event processing
	for event in pygame.event.get():
		# close window
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			print("User closed window.")
			close_window = True

		# start moving ball
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and p1_start == True and move_ball == False:
			print("User pressed spacebar, p1 start.")
			ball_x_vel = -3
			ball_y_vel = random.randint(-3, 3)
			move_ball = True
		
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and p1_start == False and move_ball == False:
			print("User pressed spacebar, p2 start.")
			ball_x_vel = 3
			ball_y_vel = random.randint(-3, 3)
			move_ball = True

		# AI control 1
		if ai_control1 == False:
			# start/stop paddle1 moving up
			if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
				print("User pressed up arrow key.")
				move_up_p1 = True
			if event.type == pygame.KEYUP and event.key == pygame.K_UP:
				print("User let go of up arrow key.")
				move_up_p1 = False

			# start/stop paddle1 moving down	
			if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
				print("User pressed down arrow key.")
				move_down_p1 = True
			if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
				print("User let go of down arrow key.")
				move_down_p1 = False

			# start AI
			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
				print("Player 1 started AI Control.")
				ai_control1 = True

		else:
			# stop AI
			if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
				print("Player 1 stopped AI Control.")
				ai_control1 = False
		# AI control 2
		if ai_control2 == False:
			# start/stop paddle2 moving up
			if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
				print("User pressed w key.")
				move_up_p2 = True

			if event.type == pygame.KEYUP and event.key == pygame.K_w:
				print("User pressed w key.")
				move_up_p2 = False


			# start/stop paddle2 moving down
			if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
				print("User pressed s key.")
				move_down_p2 = True

			if event.type == pygame.KEYUP and event.key == pygame.K_s:
				print("User pressed s key.")
				move_down_p2 = False

			# start AI
			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				print("Player 2 started AI Control.")
				ai_control2 = True


		else:
			# stop AI
			if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
				print("Player 2 stopped AI Control.")
				ai_control2 = False
	# game logic
	# ball movement
	if move_ball == True:
		# check top
		if ball.y + ball_y_vel < 0:
			print("Ball collided with top.")
			beep1.play()
			ball_y_vel *= -1

		# check bottom
		if ball.y + ball_y_vel + ball_size[1] > size[1]:
			print("Ball collided with bottom.")
			beep2.play()
			ball_y_vel *= -1

		# check left (p1 scores)
		if ball.x + ball_x_vel < 0:
			print("Ball collided with left, p1 scores.")
			move_ball = False
			p1_start = False
			ball.x, ball.y = ball_p2_start
			p1score += 1
			hits = 0

		# check right (p2 scores)
		if ball.x + ball_x_vel + ball_size[0] > size[0]:
			print("Ball collided with right, p2 scores.")
			move_ball = False
			p1_start = True
			ball.x, ball.y = ball_p1_start
			p2score += 1	
			hits = 0

		# check left paddle (player 2)
		if ball.colliderect(paddle2):
			print ("Ball collided with player 2 paddle.")
			boop1.play()
			if ball.y + ball_y_vel > paddle2.y and ball.y + ball_y_vel < paddle2.y + paddle_size[1]:
				ball_x_vel *= -1
				hits += 1
				if hits % 2 == 0:
					if ball_x_vel < 0:
						ball_x_vel -= ball_x_acc
					else:
						ball_x_vel += ball_x_acc
					if ball_y_vel < 0:
						ball_y_vel -= ball_y_acc
					else:
						ball_y_vel += ball_y_acc
			else:
				ball_y_vel *= -1

		# check right paddle (player 1)
		if ball.colliderect(paddle1):
			print ("Ball collided with player 1 paddle.")
			boop2.play()
			if ball.y + ball_y_vel > paddle1.y and ball.y + ball_y_vel < paddle1.y + paddle_size[1]:
				ball_x_vel *= -1
				hits += 1
				if hits % 2 == 0:
					if ball_x_vel < 0:
						ball_x_vel -= ball_x_acc
					else:
						ball_x_vel += ball_x_acc
					if ball_y_vel < 0:
						ball_y_vel -= ball_y_acc
					else:
						ball_y_vel += ball_y_acc
			else:
				ball_y_vel *= -1

		ball = ball.move(ball_x_vel, ball_y_vel)
		
	# paddle1 movement
	if move_up_p1 == True:
		if paddle1.y > 0:
			paddle1 = paddle1.move(0, -paddle_y_vel)
	if move_down_p1 == True:
		if paddle1.y + paddle_size[1] < size[1]:
			paddle1 = paddle1.move(0, paddle_y_vel)
	# ai movement
	if ai_control1 == True:
		if ball.y < paddle1.y + (paddle_size[1] / 2) and paddle1.y > 0:
			paddle1 = paddle1.move(0, -paddle_y_vel)
		if ball.y > paddle1.y + (paddle_size[1] / 2) and paddle1.y + paddle_size[1] < size[1]:
			paddle1 = paddle1.move(0, paddle_y_vel)

	# paddle2 movement
	if move_up_p2 == True:
		if paddle2.y > 0:
			paddle2 = paddle2.move(0, -paddle_y_vel)
	if move_down_p2 == True:
		if paddle2.y + paddle_size[1] < size[1]:
			paddle2 = paddle2.move(0, paddle_y_vel)
	
	# ai movement
	if ai_control2 == True:
		if ball.y < paddle2.y + (paddle_size[1] / 2) and paddle2.y > 0:
			paddle2 = paddle2.move(0, -paddle_y_vel)
		if ball.y > paddle2.y + (paddle_size[1] / 2) and paddle2.y + paddle_size[1] < size[1]:
			paddle2 = paddle2.move(0, paddle_y_vel)

	# create score text
	score1 = font.render(str(p1score), True, green)
	score2 = font.render(str(p2score), True, green)	

	# drawing code
	# clear screen
	screen.fill(white)

	# draw background
	screen.fill(black)
	pygame.draw.line(screen, green, (size[0] / 2, 0), (size[0] / 2, size[1]))

	# draw ball and paddles
	pygame.draw.rect(screen, white, ball)
	pygame.draw.rect(screen, green, paddle1)
	pygame.draw.rect(screen, green, paddle2)

	# display text
	screen.blit(score1, p1_font_pos)
	screen.blit(score2, p2_font_pos)

	# flip to screen
	pygame.display.flip()

	# timer
	clock.tick(30)

pygame.quit()



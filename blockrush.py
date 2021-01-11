import pygame
import sys
import random

pygame.init()
WIDTH = 800
score = 0
HEIGHT = 600
BASE_SPEED = 5
SPEED = 0
clock = pygame.time.Clock()
player_size = 40
player_pos = [WIDTH/2, HEIGHT-2*player_size]
BACKGROUND_COLOR = (33,32,28)
enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]
myFont = pygame.font.SysFont("Arial", 35)
def set_level(score, SPEED):
	SPEED = (score / 10) + BASE_SPEED
	return SPEED
def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.1:
		x_pos = random.randint(0,WIDTH-enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])
def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score
def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, ENEMYCOLOR, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False
def detect_collision(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]
	e_x = enemy_pos[0]
	e_y = enemy_pos[1]
	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False
ENEMYCOLOR = (252,122,87)
PLAYERCOLOR = (252,215,87)
pygame.display.set_caption("blockrush")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_over = False
while not game_over:
	pressed = pygame.key.get_pressed()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	x = player_pos[0]
	y = player_pos[1]
	if pressed[pygame.K_UP] and y > 0:
		y -= 5
	if pressed[pygame.K_DOWN] and y < HEIGHT - 40:
		y += 5
	if pressed[pygame.K_LEFT] and x > 0:
		x -= 5
	if pressed[pygame.K_RIGHT] and x < WIDTH - 40:
		x += 5
	player_pos = [x, y]
		
	screen.fill(BACKGROUND_COLOR)
	
	if detect_collision(player_pos, enemy_pos):
		game_over = True
	
	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	SPEED = set_level(score, SPEED)
	text = "Score: " + str(score) 
	label = myFont.render(text, 1, (237,227,228))
	if collision_check(enemy_list, player_pos):
		game_over = True
	draw_enemies(enemy_list)
	pygame.draw.rect(screen, PLAYERCOLOR, (player_pos[0], player_pos[1], player_size, player_size))
	scoreval = 140
	inc = 17
	if len(str(score)) >= 2:
		inc += 1
		scoreval = scoreval + (inc * ((len(str(score))) - 1))	
	screen.blit(label, (WIDTH-scoreval, HEIGHT-40))
	
	clock.tick(45)
	pygame.display.update()
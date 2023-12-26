import pygame
from sys import exit
from random import randint


# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
#         player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
#         self.player_walk = [player_walk_1,player_walk_2]
#         self.player_index = 0
#         self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
#         self.image = pygame.image.load('graphics/Player/player_walk_1.png')
#         self.rect = self.image.get_rect(midbottom = (200,300))
#         self.gravity = 0

#     def player_input(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
#             self.gravity = -20

#     def apply_gravity(self):
#         self.gravity += 1
#         self.rect.y += self.gravity
#         if self.rect.bottom >=300:
#             self.rect.bottom = 300

#     def animation_state(self):
#         if self.rect.bottom < 300:
#             self.image = self.player_jump
#         else:
#             self.player_index += 0.1
#             if self.player_index >= len(self.player_walk):self.player_index=0
#             self.image = self.player_walk[int(self.player_index)]

#     def update(self):
#         self.player_input()
#         self.apply_gravity()
#         self.animation_state()




def display_score():
    current_time =round(( pygame.time.get_ticks() - start_time)/1000)
    score_surf = test_font.render(f"Score: {current_time}",False,(64,64,64))
    score_rect = score_surf.get_rect(center=(400,50))
    window.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                window.blit(snail_surface,obstacle_rect)
            else:
                window.blit(fly_surf,obstacle_rect)
        
        for item in obstacle_list:
            if item.x <-100:
                obstacle_list.remove(item)
        return obstacle_list
    else: return []

def collsions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surface,player_index
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >=len(player_walk): player_index= 0
        player_surface = player_walk[int(player_index)]


pygame.init()
WIDTH, HEIGHT = 800, 400
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# test_surface = pygame.Surface((100,200))
# test_surface.fill("Red")

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# score_surface = test_font.render("My Game", False, (64,64,64))
# score_rect = score_surface.get_rect(center=(400,50))


snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()


fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()


player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(80,300))
player_gravity = 0
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))


player = pygame.sprite.GroupSingle()
# player.add(Player())


game_title = test_font.render("PixelRunner", False, (111,196,169))
game_title_rect = game_title.get_rect(center=(410,70))


game_message = test_font.render("Press SPACE to start the game", False, (111,196,169))
game_message_rect = game_message.get_rect(center=(400,340))


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1900)
obstacle_rect_list = []


while True:
    for event in pygame.event.get():
            
        if game_active:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom>=300:
                    player_gravity = -20
                if event.key == pygame.K_a:
                    player_rect.centerx -= 50
                if event.key == pygame.K_d:
                    player_rect.centerx += 50

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900,1100),210)))
                    

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                game_active = True
                player_rect.x = 80
                start_time = pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



    if game_active:
        window.blit(sky_surface,(0,0))
        window.blit(ground_surface,(0,300))

        # pygame.draw.rect(window,"#c0e8ec",score_rect)
        # pygame.draw.rect(window,"#c0e8ec",score_rect,10)
        # window.blit(score_surface, score_rect)
        score = display_score()

        # window.blit(snail_surface, snail_rect)

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        
        player_animation()
        window.blit(player_surface, player_rect)

        # Sprite Class
        # player.draw(window)
        # player.update()

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collisons
        game_active = collsions(player_rect,obstacle_rect_list)

        # if player_rect.colliderect(snail_rect):
        #     game_active = False

    else:
        window.fill((94,129,162))
        window.blit(player_stand,player_stand_rect)

        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        window.blit(game_title,game_title_rect)
        if score == 0:
            window.blit(game_message,game_message_rect)
        else:
            window.blit(score_message,score_message_rect)
    
    pygame.display.update()
    clock.tick(60)
import pygame

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pacman Game")

# Load the images
pacman_image = pygame.image.load("assets/pacman.png")
dot_image = pygame.image.load("assets/dot.png")
ghost_image = pygame.image.load("assets/ghost.png")

# Load the sounds
eat_sound = pygame.mixer.Sound("assets/eat.wav")
collide_sound = pygame.mixer.Sound("assets/collide.wav")

# Set up the game objects
pacman_rect = pacman_image.get_rect()
pacman_rect.x = 400
pacman_rect.y = 300

dots = []
for i in range(10):
    dot_rect = dot_image.get_rect()
    dot_rect.x = i * 80 + 40
    dot_rect.y = 200
    dots.append(dot_rect)

ghosts = []
for i in range(3):
    ghost_rect = ghost_image.get_rect()
    ghost_rect.x = i * 200 + 100
    ghost_rect.y = 300
    ghosts.append(ghost_rect)

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the game loop
clock = pygame.time.Clock()
running = True
game_over = False
play_again = False
game_completed = False
score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (game_over or game_completed):
                play_again = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        pacman_rect.x += 5
    if keys[pygame.K_UP]:
        pacman_rect.y -= 5
    if keys[pygame.K_DOWN]:
        pacman_rect.y += 5

    for dot_rect in dots[:]:
        if pacman_rect.colliderect(dot_rect):
            dots.remove(dot_rect)
            score += 10
            eat_sound.play()

    for ghost_rect in ghosts:
        if pacman_rect.colliderect(ghost_rect):
            game_over = True
            collide_sound.play()

    if len(dots) == 0:
        game_completed = True

    screen.fill((0, 0, 0))
    if not game_over and not game_completed:
        screen.blit(pacman_image, pacman_rect)
        for dot_rect in dots:
            screen.blit(dot_image, dot_rect)
        for ghost_rect in ghosts:
            screen.blit(ghost_image, ghost_rect)
    elif game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (300, 250))
        play_again_text = font.render("Press space to play again", True, (255, 255, 255))
        screen.blit(play_again_text, (250, 300))
    else:
        game_completed_text = font.render("Game Completed!", True, (0, 255, 0))
        screen.blit(game_completed_text, (250, 250))
        play_again_text = font.render("Press space to play again", True, (255, 255, 255))
        screen.blit(play_again_text, (250, 300))

    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

    if play_again:
        dots = []
        for i in range(10):
            dot_rect = dot_image.get_rect()
            dot_rect.x = i * 80 + 40
            dot_rect.y = 200
            dots.append(dot_rect)
        pacman_rect.x = 400
        pacman_rect.y = 300
        score = 0
        game_over = False
        game_completed = False
        play_again = False

    clock.tick(60)

pygame.quit()
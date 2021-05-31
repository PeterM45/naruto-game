import pygame
import os

pygame.font.init()
pygame.mixer.init()
# so font and sound can be used

width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Naruto x Sasuke")
# width and height in pixels, the window (win) is set to the width and height

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 255, 255)
# colour is in rgb form

border = pygame.Rect(width // 2 - 5, 0, 10, height)
# the rectangle in the middle of the screen that the models cannot cross over

jutsuHitSound = pygame.mixer.Sound(
    os.path.join('Assets', 'hit.mp3'))
jutsuSound = pygame.mixer.Sound(
    os.path.join('Assets', 'jutsu.mp3'))
# sound for the attacks and when they hit the opponent

healthFont = pygame.font.SysFont('comicsans', 40)
winnerFont = pygame.font.SysFont('comicsans', 100)
# font for health and when someone wins

FPS = 60
# needed so the game can run
VEL = 5
# speed in which the characters move
JUTSU_VEL = 7
# speed in which the attack move at
CHAKRA = 3
# attacks go 3 at a time
shinobiWidth, shinobiHeight = 50, 70
# character height and width in pixels
sasukeHit = pygame.USEREVENT + 1
narutoHit = pygame.USEREVENT + 2

sasukeImage = pygame.image.load(
    os.path.join('Assets', 'sasuke.png'))
SASUKE = pygame.transform.flip(
    pygame.transform.scale(sasukeImage, (shinobiWidth, shinobiHeight)), True, False)
# loads in character from file path

narutoImage = pygame.image.load(
    os.path.join('Assets', 'naruto.png'))
NARUTO = pygame.transform.scale(narutoImage, (shinobiWidth, shinobiHeight))
# loads in character from file path

finalValley = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'final_valley.png')), (width, height))
# the background loaded in from file path


def draw_window(naruto, sasuke, naruto_jutsu, sasuke_jutsu, naruto_health, sasuke_health):
    win.blit(finalValley, (0, 0))
    pygame.draw.rect(win, black, border)
    # win.blit is what displays something on the screen
    # .draw.rect draws a rectangle when given 3 arguments

    narutoHealthText = healthFont.render("Health: " + str(naruto_health), 1, white)
    sasukeHealthText = healthFont.render("Health: " + str(sasuke_health), 1, white)
    win.blit(narutoHealthText, (width - narutoHealthText.get_width() - 60, 10))
    win.blit(sasukeHealthText, (60, 10))
    # draws the health using the variables made previously that included the font and size
    # using math they are drawn on the same distance from their respective side

    win.blit(SASUKE, (sasuke.x, sasuke.y))
    win.blit(NARUTO, (naruto.x, naruto.y))
    # draws the characters at an x and y position

    for jutsu in naruto_jutsu:
        pygame.draw.rect(win, blue, jutsu)
        # the attack is a rectangle that is colour blue

    for jutsu in sasuke_jutsu:
        pygame.draw.rect(win, red, jutsu)
        # the attack is a rectangle that is colour red

    pygame.display.update()
    # this is extremely important, this makes everything above it draw on the screen at the tick rate


def sasukeMovement(keys_pressed, sasuke):
    if keys_pressed[pygame.K_a] and sasuke.x - VEL > 0:  # LEFT
        sasuke.x -= VEL
    if keys_pressed[pygame.K_d] and sasuke.x + VEL + sasuke.width < border.x:  # RIGHT
        sasuke.x += VEL
    if keys_pressed[pygame.K_w] and sasuke.y - VEL > 0:  # UP
        sasuke.y -= VEL
    if keys_pressed[pygame.K_s] and sasuke.y + VEL + sasuke.height < height - 15:  # DOWN
        sasuke.y += VEL
        # character movement in form WASD, it also makes sure you cant go off screen


def narutoMovement(keys_pressed, naruto):
    if keys_pressed[pygame.K_LEFT] and naruto.x - VEL > border.x + border.width:  # LEFT
        naruto.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and naruto.x + VEL + naruto.width < width:  # RIGHT
        naruto.x += VEL
    if keys_pressed[pygame.K_UP] and naruto.y - VEL > 0:  # UP
        naruto.y -= VEL
    if keys_pressed[pygame.K_DOWN] and naruto.y + VEL + naruto.height < height - 15:  # DOWN
        naruto.y += VEL
        # character movement for arrow keys, it also makes sure you cant go off screen


def handleJutsu(sasuke_jutsu, naruto_jutsu, sasuke, naruto):
    for jutsu in sasuke_jutsu:
        jutsu.x += JUTSU_VEL
        if naruto.colliderect(jutsu):
            pygame.event.post(pygame.event.Event(narutoHit))
            sasuke_jutsu.remove(jutsu)
            # if the attack hits the event is stored and the rectangle is removed from the screen
        elif jutsu.x > width:
            sasuke_jutsu.remove(jutsu)
            # if the attack misses and goes off screen it is removed so it doesnt go on forever

    for jutsu in naruto_jutsu:
        jutsu.x -= JUTSU_VEL
        if sasuke.colliderect(jutsu):
            pygame.event.post(pygame.event.Event(sasukeHit))
            naruto_jutsu.remove(jutsu)
            # if the attack hits the event is stored and the rectangle is removed from the screen
        elif jutsu.x < 0:
            naruto_jutsu.remove(jutsu)
            # if the attack misses and goes off screen it is removed so it doesnt go on forever


def drawWinner(text):
    draw_text = winnerFont.render(text, 1, white)
    win.blit(draw_text, (width / 2 - draw_text.get_width() /
                         2, height / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)
    # function when someone wins, the winner font is drawn on the screen
    # math is used to make sure it is centered, the text is on the screen for 5 seconds until it then resets the game


def main():
    # the main function that everything runs in
    naruto = pygame.Rect(700, 300, shinobiWidth, shinobiHeight)
    sasuke = pygame.Rect(100, 300, shinobiWidth, shinobiHeight)

    narutoJutsu = []
    sasukeJutsu = []
    # attack number is an empty list

    narutoHealth = 10
    sasukeHealth = 10
    # both health is equal to 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        # so game runs at 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                # if you press the x to close the window it closes

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(sasukeJutsu) < CHAKRA:
                    jutsu = pygame.Rect(
                        sasuke.x + sasuke.width, sasuke.y + sasuke.height // 2 - 2, 10, 5)
                    sasukeJutsu.append(jutsu)
                    jutsuSound.play()
                    # lctrl is how you attack on the left side, the sound is played when you attack

                if event.key == pygame.K_SLASH and len(narutoJutsu) < CHAKRA:
                    jutsu = pygame.Rect(
                        naruto.x, naruto.y + naruto.height // 2 - 2, 10, 5)
                    narutoJutsu.append(jutsu)
                    jutsuSound.play()

            if event.type == narutoHit:
                narutoHealth -= 1
                jutsuHitSound.play()

            if event.type == sasukeHit:
                sasukeHealth -= 1
                jutsuHitSound.play()

        winner_text = ""
        if narutoHealth <= 0:
            winner_text = "Sasuke Wins!"

        if sasukeHealth <= 0:
            winner_text = "Naruto Wins!"

        if winner_text != "":
            drawWinner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        sasukeMovement(keys_pressed, sasuke)
        narutoMovement(keys_pressed, naruto)

        handleJutsu(sasukeJutsu, narutoJutsu, sasuke, naruto)

        draw_window(naruto, sasuke, narutoJutsu, sasukeJutsu,
                    narutoHealth, sasukeHealth)
        # calling the functions

    main()


if __name__ == "__main__":
    main()

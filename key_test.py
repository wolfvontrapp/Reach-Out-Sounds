import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    #clock = pygame.time.Clock()

    while True:
        pressed = pygame.key.get_pressed()
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        if ctrl_held:
            print('held')

        for event in pygame.event.get():
            # determin if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                print('QUIT')
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    print('KEY W HELD')

main()

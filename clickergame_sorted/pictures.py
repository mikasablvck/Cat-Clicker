import pygame, sys

def load_images(screen_w: int, screen_h: int) -> dict:
    try:
        images = {}

        images["clicker"] = pygame.transform.scale(
            pygame.image.load("pics/cat_clicker.png").convert_alpha(), (330, 330)
        )

        images["hand"] = pygame.transform.scale(
            pygame.image.load("pics/hand_fin.png").convert_alpha(), (120, 120)
        )

        bg = pygame.image.load("pics/catroom_empty3.png").convert()
        images["background"] = pygame.transform.scale(bg, (screen_w, screen_h))

        shop_img = pygame.image.load("pics/shop.png").convert_alpha()
        shop_img = pygame.transform.scale(shop_img, (100, 100))
        shop_rect = shop_img.get_rect(topright=(screen_w - 20, 20))
        images["shop"] = (shop_img, shop_rect)

        yarn_roll = pygame.image.load("pics/wool.png").convert_alpha()
        images["yarn_roll"] = pygame.transform.smoothscale(yarn_roll, (72, 72))
        images["yarn_icon"] = pygame.transform.smoothscale(images["yarn_roll"], (43, 43))

        sad_cat = pygame.image.load("pics/cat_leaving.png").convert_alpha()
        images["sad_cat"] = pygame.transform.smoothscale(sad_cat, (340, 340))

        gear_img = pygame.image.load("pics/gear.png").convert_alpha()
        gear_img = pygame.transform.scale(gear_img, (80, 80))
        gear_rect = gear_img.get_rect(topright=(shop_rect.left - 20, shop_rect.top + 15))
        images["gear"] = (gear_img, gear_rect)

        return images

    except pygame.error as e:
        print("Fehler beim Laden eines Bildes:", e)
        pygame.quit()
        sys.exit()

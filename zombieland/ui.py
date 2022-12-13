import pygame as pg
from zombieland.settings import WIDTH, HEIGHT, FONT_PATH, TILEWIDTH, CHAR_PATH, CHARACTERS, UI_ASSET_PATH
from zombieland.utils import load_image

Button = pg.Rect

class UI:
    MARGIN = 10

    def __init__(self, game):
        self.game = game
        # Buttons
        self.music_btn: Button = None
        self.sfx_btn: Button = None
        self.right_btn: Button = None
        self.left_btn: Button = None
        self.home_btn: Button = None
        self.shop_btn: Button = None
        self.setting_btn: Button = None
        self.play_btn: Button = None
        self.mode_btn: Button = None
        # Set up
        self.selected_menu = 'home'
        # Images
        self.title_frame = load_image(UI_ASSET_PATH + '/LargeFrame.png', WIDTH - 100, 150)
        self.dark_frame = load_image(UI_ASSET_PATH + '/SmallFrame2.png', 500, 400)
        self.green_frame = load_image(UI_ASSET_PATH + '/FrameGreen.png', WIDTH / 3 + 50, 300)
        self.blue_frame = load_image(UI_ASSET_PATH + '/FrameBlue.png', WIDTH / 3 + 50, 300)
        self.brown_frame = load_image(UI_ASSET_PATH + '/FrameBrown.png', WIDTH / 3, 250)
        self.kill_medal = load_image(UI_ASSET_PATH + '/Medals/SoloKills.png', 100, 100)
        self.heal_medal = load_image(UI_ASSET_PATH + '/Medals/MostHealing.png', 100, 100)
        self.survive_medal = load_image(UI_ASSET_PATH + '/Medals/MostRevives.png', 100, 100)
        self.coin_img = load_image(UI_ASSET_PATH + '/Icons/CoinIcon.png', 40)
        self.btn_img = load_image(UI_ASSET_PATH + '/BtnNormal.png')
        self.btn_hover_img = load_image(UI_ASSET_PATH + '/HoverBtn.png')
        self.btn_b_green = load_image(UI_ASSET_PATH + '/rect_greenline.png')
        self.tab_active_img = load_image(UI_ASSET_PATH + '/SelectedTab.png')
        self.tab_img = load_image(UI_ASSET_PATH + '/UnselectedTab.png')
        self.arrow_l_img = load_image(UI_ASSET_PATH + '/Arrow.png', 50)
        self.arrow_r_img = pg.transform.flip(self.arrow_l_img, flip_x=True, flip_y=False)
        self.tog_on_img = load_image(UI_ASSET_PATH + '/toggleOn.png', 60, 30)
        self.tog_off_img = load_image(UI_ASSET_PATH + '/toggleOff.png', 60, 30)
        self.k_r = load_image(UI_ASSET_PATH + '/Keys/R.png', 40)
        self.k_w = load_image(UI_ASSET_PATH + '/Keys/W.png', 40)
        self.k_s = load_image(UI_ASSET_PATH + '/Keys/S.png', 40)
        self.k_space = load_image(UI_ASSET_PATH + '/Keys/SPACEALTERNATIVE.png', 120, 30)
        self.pointer = pg.sprite.GroupSingle()
        self.pointer.add(Pointer())

    @staticmethod
    def get_text(text, color, size):
        font = pg.font.Font(FONT_PATH, size)
        rendered_txt = font.render(text, True, color)
        txt_rect = rendered_txt.get_rect()
        return rendered_txt, txt_rect

    def write(self, text, color, size, x, y, shadow=False, surface=None, align_left=False):
        rendered_txt, txt_rect = self.get_text(text, color, size)
        if x == 'left':
            x = self.MARGIN + txt_rect.width // 2 + 5
        elif x == 'right':
            x = WIDTH - self.MARGIN * 2 - txt_rect.width // 2
        elif x == 'center':
            x = WIDTH // 2
        if y == 'top':
            y = self.MARGIN + txt_rect.height // 2
        elif y == 'center':
            y = HEIGHT // 2
        if align_left:
            txt_rect.topleft = x, y
        else:
            txt_rect.center = x, y
        if surface is not None:
            bg_img = pg.transform.scale(surface, (txt_rect.width + 20, txt_rect.height + 10))
            bg_rect = bg_img.get_rect(center=txt_rect.center)
            self.game.screen.blit(bg_img, bg_rect)
        if shadow:
            self.write(text, 'black', size, x + 1.5, y + 2)
        self.game.screen.blit(rendered_txt, txt_rect)

    def create_button(self, text, bg_img, size, x, y, pad_x=30, pad_y=5, align_left=False) -> Button:
        if text == '':
            background_img = bg_img
            btn_rect = background_img.get_rect(center=(x, y))
            if align_left:
                btn_rect.topleft = x, y
            self.game.screen.blit(background_img, btn_rect)
        else:
            rendered_text, text_rect = self.get_text(text, 'white', size)
            background_img = pg.transform.scale(bg_img, (text_rect.width + pad_x, text_rect.height + pad_y))
            btn_rect = background_img.get_rect(center=(x, y))
            text_rect.center = x, y
            if align_left:
                text_rect.topleft = x + pad_x / 2, y + pad_y / 2
                btn_rect.topleft = x, y
            self.game.screen.blit(background_img, btn_rect)
            self.game.screen.blit(rendered_text, text_rect)
        return btn_rect

    def display_score(self):
        self.write(f"Kill Count: {self.game.score}", 'white', 40, 'left', 'top', True)
        self.write(f"Survival: {self.game.survial_score}", 'white', 40, 'right', 'top', True)

    def display_shop(self):
        self.shop_btn = self.create_button('Shop', self.tab_active_img, 50, self.MARGIN + self.home_btn.width,
                                           self.MARGIN, align_left=True, pad_x=50)
        # Character Display
        self.write('Select Your Character', 'yellow', 45, 'center', self.MARGIN + self.home_btn.height + 60)
        self.game.screen.blit(self.brown_frame, (
            WIDTH / 2 - self.brown_frame.get_width() / 2, HEIGHT / 2 - self.brown_frame.get_height() / 2))
        current_char = load_image(CHAR_PATH + self.game.selected_char + '_shoot.png', 100)
        char_rect = current_char.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.game.screen.blit(current_char, char_rect)
        self.write(f"{self.game.selected_char.upper()}", 'white', 40, 'center',
                   HEIGHT / 2 + self.brown_frame.get_height() / 2 + 40)
        # Arrow Buttons
        self.left_btn = self.create_button('', self.arrow_l_img, 40,
                                           WIDTH / 2 - self.brown_frame.get_width() / 2 - self.arrow_l_img.get_width() / 2,
                                           HEIGHT / 2 + self.brown_frame.get_height() / 2 + 20, align_left=True)
        self.right_btn = self.create_button('', self.arrow_r_img, 40, WIDTH / 2 + self.brown_frame.get_width() / 2,
                                            HEIGHT / 2 + self.brown_frame.get_height() / 2 + 20, align_left=True)

    def display_home(self):
        self.home_btn = self.create_button('Home', self.tab_active_img, 50, self.MARGIN, self.MARGIN, align_left=True,
                                           pad_x=50)
        # Title
        title_rect = self.title_frame.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 170))
        self.game.screen.blit(self.title_frame, title_rect)
        self.write('ZOMBiELAND', 'white', 100, 'center', title_rect.y + 80)
        # Medals
        self.game.screen.blit(self.blue_frame, (WIDTH / 2 - self.blue_frame.get_width() - 20, HEIGHT / 2 - 80))
        self.game.screen.blit(self.kill_medal, (WIDTH / 2 - self.blue_frame.get_width() + 20, HEIGHT / 2 + 50))
        self.game.screen.blit(self.green_frame, (WIDTH / 2 + 20, HEIGHT / 2 - 80))
        self.game.screen.blit(self.heal_medal, (WIDTH / 2 + 45, HEIGHT / 2 + 50))
        kill_title, kill_rect = self.get_text('Top Kills', 'white', 60)
        kill_rect.topleft = WIDTH / 2 - self.blue_frame.get_width() / 2 - kill_rect.width / 2 - 20, HEIGHT / 2 - 30
        sur_title, sur_rect = self.get_text('Top Survival', 'white', 50)
        sur_rect.topleft = WIDTH / 2 + self.green_frame.get_width() / 2 - sur_rect.width / 2 + 12, HEIGHT / 2 - 30
        self.game.screen.blit(kill_title, kill_rect)
        self.game.screen.blit(sur_title, sur_rect)
        self.write('129', 'white', 70, WIDTH / 2 - self.blue_frame.get_width() / 2 - 50, HEIGHT / 2 + 70, align_left=True)
        self.write('3687.46 s', 'white', 40, WIDTH / 2 + 150, HEIGHT / 2 + 80, align_left=True)

    def display_menu(self):
        self.game.screen.fill("light blue")
        # Tabs
        self.home_btn = self.create_button('Home', self.tab_img, 50, self.MARGIN, self.MARGIN, align_left=True,
                                           pad_x=50)
        self.shop_btn = self.create_button('Shop', self.tab_img, 50, self.MARGIN + self.home_btn.width, self.MARGIN,
                                           align_left=True, pad_x=50)
        self.setting_btn = self.create_button('Setting', self.tab_img, 50,
                                              self.MARGIN + self.home_btn.width + self.shop_btn.width, self.MARGIN,
                                              align_left=True, pad_x=50)
        # Coin
        # pg.draw.rect(self.game.screen, 'white', (WIDTH-180, self.MARGIN, 150, 50))
        self.game.screen.blit(self.coin_img, (WIDTH - 180, self.MARGIN+5))
        self.write('1920', 'black', 35, WIDTH - 140, self.MARGIN+10, align_left=True)
        # Background
        pg.draw.rect(self.game.screen, 'black',
                     (self.MARGIN, self.MARGIN + self.home_btn.height, WIDTH - self.MARGIN * 2, HEIGHT - 150))
        if self.selected_menu == 'home':
            self.display_home()
        elif self.selected_menu == 'shop':
            self.display_shop()
        elif self.selected_menu == 'setting':
            self.display_setting()
        # Footer
        pg.draw.rect(self.game.screen, 'indigo', (0, HEIGHT - 80, WIDTH, 80))
        self.play_btn = self.create_button('New Game', self.btn_img, 50, WIDTH / 2, HEIGHT - 40, pad_x=40, pad_y=20)
        if self.play_btn.collidepoint(pg.mouse.get_pos()):
            self.play_btn = self.create_button('New Game', self.btn_hover_img, 53, WIDTH / 2, HEIGHT - 40, pad_x=40,
                                               pad_y=20)

    def display_setting(self):
        self.setting_btn = self.create_button('Setting', self.tab_active_img, 50,
                                              self.MARGIN + self.home_btn.width + self.shop_btn.width, self.MARGIN,
                                              align_left=True, pad_x=50)
        self.write('Options', 'yellow', 45, self.MARGIN+200, self.MARGIN+self.home_btn.height+80)
        self.write('Game Controls', 'yellow', 45, WIDTH / 2 + 200, self.MARGIN + self.home_btn.height + 80)
        # Settings
        self.write('Difficulty', 'white', 30, self.MARGIN*3, HEIGHT/2-100, align_left=True)
        self.mode_btn = self.create_button(f'{self.game.difficulty.upper()}', self.btn_b_green, 30, WIDTH/2-220, HEIGHT/2-100, align_left=True)
        self.write('Background Music', 'white', 30, self.MARGIN * 3, HEIGHT/2-30, align_left=True)
        self.music_btn = self.create_button('', self.tog_on_img if self.game.music_on else self.tog_off_img, 30,
                                            WIDTH / 2 - self.tog_on_img.get_width() - 80, HEIGHT / 2-30, align_left=True)

        self.write('Sound Effects', 'white', 30, self.MARGIN * 3, HEIGHT / 2 + 40, align_left=True)
        self.sfx_btn = self.create_button('', self.tog_on_img if self.game.sfx_on else self.tog_off_img, 30,
                                          WIDTH / 2 - self.tog_off_img.get_width() - 80, HEIGHT / 2 + 40,
                                          align_left=True)
        # Game control helper
        self.game.screen.blit(self.k_w, (WIDTH / 2, 200))
        self.game.screen.blit(self.k_s, (WIDTH / 2, 250))
        self.game.screen.blit(self.k_r, (WIDTH / 2, 300))
        self.game.screen.blit(self.k_space, (WIDTH / 2, 350))
        self.write("- Move Forward", "light grey", 35, WIDTH / 2 + 50, 200, align_left=True)
        self.write("- Move Backward", "light grey", 35, WIDTH / 2 + 50, 250, align_left=True)
        self.write("- Reload", "light grey", 35, WIDTH / 2 + 50, 300, align_left=True)
        self.write("- Shoot", "light grey", 35, WIDTH / 2 + 130, 350, align_left=True)
        self.write("[ Use POINTER to control direction ]", 'light grey', 25, WIDTH / 2 + 220, 430)

    def display_gameover(self):
        self.game.screen.fill('brown')
        self.game.screen.blit(self.dark_frame, (
            WIDTH / 2 - self.dark_frame.get_width() / 2, HEIGHT / 2 - self.dark_frame.get_height() / 2))
        self.write('Gameover', 'red', 85, 'center', HEIGHT / 2 - 100, True)
        self.write(f"Kill: {self.game.score} zombies", 'white', 40, 'center', 'center')
        self.write(f"Survive: {self.game.survial_score} sec", 'white', 40, 'center', HEIGHT / 2 + 50)
        self.play_btn = self.create_button('Play Again', self.btn_img, 32, WIDTH / 2 - 100, HEIGHT / 2 + 120, pad_y=30)
        self.home_btn = self.create_button('Main Menu', self.btn_img, 32, WIDTH / 2 + 100, HEIGHT / 2 + 120, pad_y=30)

        if self.play_btn.collidepoint(pg.mouse.get_pos()):
            self.play_btn = self.create_button('Play Again', self.btn_hover_img, 35, WIDTH / 2 - 100, HEIGHT / 2 + 120,
                                               pad_y=30)
        if self.home_btn.collidepoint(pg.mouse.get_pos()):
            self.home_btn = self.create_button('Main Menu', self.btn_hover_img, 35, WIDTH / 2 + 100, HEIGHT / 2 + 120,
                                               pad_y=30)

    def draw(self):
        if not self.game.is_running:
            pg.mouse.set_visible(True)
            self.display_menu()
            return
        if self.game.is_gameover:
            pg.mouse.set_visible(True)
            self.display_gameover()
            return
        pg.mouse.set_visible(False)
        self.pointer.draw(self.game.screen)
        self.display_score()

    def get_click(self, mouse_x, mouse_y):
        if self.play_btn and self.play_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            self.game.start_new_game()
        elif self.home_btn and self.home_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            self.game.is_running = False
            self.selected_menu = 'home'
        elif self.shop_btn and self.shop_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            self.selected_menu = 'shop'
        elif self.setting_btn and self.setting_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            self.selected_menu = 'setting'
        elif self.music_btn and self.music_btn.collidepoint(mouse_x, mouse_y):
            self.game.music_on = not self.game.music_on
            self.game.sfx.btn_click.play()
        elif self.sfx_btn and self.sfx_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            self.game.sfx_on = not self.game.sfx_on
        elif self.mode_btn and self.mode_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            if self.game.difficulty == 'newbie':
                self.game.difficulty = 'expert'
            elif self.game.difficulty == 'expert':
                self.game.difficulty = 'legend'
            else:
                self.game.difficulty = 'newbie'
        elif self.left_btn and self.left_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            current_id = CHARACTERS.index(self.game.selected_char)
            prev_id = current_id - 1
            self.game.selected_char = CHARACTERS[prev_id]
        elif self.right_btn and self.right_btn.collidepoint(mouse_x, mouse_y):
            self.game.sfx.btn_click.play()
            current_id = CHARACTERS.index(self.game.selected_char)
            next_id = 0 if current_id + 1 >= len(CHARACTERS) else current_id + 1
            self.game.selected_char = CHARACTERS[next_id]

    def update(self):
        self.pointer.update()


class Pointer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.crosshair_pointer = load_image('./resources/assets/crosshair.png', TILEWIDTH)
        # self.hand_pointer = load_image('assets/hand.png', TILEWIDTH)
        self.image = self.crosshair_pointer
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pg.mouse.get_pos()

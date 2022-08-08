from pygame import mixer

class SFX:
    PATH = 'sfx/'

    def __init__(self):
        mixer.init()
        self.machine_gun = mixer.Sound(self.PATH+'sfx_machinegun.wav')
        self.reload = mixer.Sound(self.PATH + 'sfx_reload.wav')
        self.noammo = mixer.Sound(self.PATH + 'sfx_noammo.wav')
        self.hit = mixer.Sound(self.PATH + 'sfx_hit.wav')
        self.impact = mixer.Sound(self.PATH + 'sfx_impact.wav')
        self.damage = mixer.Sound(self.PATH + 'sfx_damage.wav')
        self.coin = mixer.Sound(self.PATH + 'sfx_coin.wav')
        self.footstep = mixer.Sound(self.PATH + 'sfx_movement.wav')
        self.btn_click = mixer.Sound(self.PATH + 'sfx_select.wav')
        self.gameover = mixer.Sound(self.PATH + 'sfx_gameover.wav')

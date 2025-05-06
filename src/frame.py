import pygame
import win32gui
import win32con
from constants import *

class Frame(pygame.Window):
    def __init__(self, game, attributes = {
        'title': None, #none means dont set it
        'position': pygame.WINDOWPOS_CENTERED,
        'minimum_size': (168, 120),
        'maximum_size': DISPLAY_SIZE,
        'resizable': True
    }):
        super().__init__(size=WINDOW_SIZE)

        self.game = game

        for attr, value in attributes.items():
            if value:
                setattr(self, attr, value)

        self.entities = []

        #link to wnd_proc
        self.hwnd = win32gui.GetForegroundWindow()
        self.old_wnd_proc = win32gui.SetWindowLong(self.hwnd, win32con.GWL_WNDPROC, lambda *args: self.wnd_proc(*args))

        #remove minimize + maximize boxes
        wnd_styles = win32gui.GetWindowLong(self.hwnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            self.hwnd, 
            win32con.GWL_STYLE, 
            wnd_styles & ~win32con.WS_MINIMIZEBOX & ~win32con.WS_MAXIMIZEBOX
        )

    def wnd_proc(self, hwnd, message, wparam, lparam):
        #update during a size / position change
        if message in [win32con.WM_MOVE, win32con.WM_SIZE, win32con.WM_TIMER]:
            #remind game that we actually want to keep looping
            #we want framerate to be uncapped here so waiting for clock to tick doesn't slow moving / resizing down
            self.game.loop(0)
        
        return win32gui.CallWindowProc(self.old_wnd_proc, hwnd, message, wparam, lparam)

    def get_rect(self):
        return pygame.Rect(*self.position,*self.size)

    def handle_event(self, event):
        pass

    def tick(self, dt):
        title_bar_size = 30 #32
        thickness = 4

        self.tiles = [
            pygame.Rect(self.position[0], self.position[1] - title_bar_size, self.size[0], title_bar_size),
            pygame.Rect(self.position[0], self.position[1] + self.size[1], self.size[0], thickness),
            pygame.Rect(self.position[0] - thickness, self.position[1], thickness, self.size[1]),
            pygame.Rect(self.position[0] + self.size[0], self.position[1], thickness, self.size[1])
        ]

        #TODO: clear overlapping rects

    def draw(self, screen):
        screen.fill('black')
        for tile in self.game.get_tiles():
            pygame.draw.rect(screen, (255,0,0), tile.move(-self.position[0], -self.position[1]))

        for entity in self.entities:
            entity.draw(screen, self)
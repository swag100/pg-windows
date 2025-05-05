#Contains frame class isolated, if i ever need it again.

import pygame
import win32gui
import win32con

#display test
from math import sin

WINDOW_SIZE = (320, 240)
FRAMERATE = 60

class Frame(pygame.Window):
    def __init__(self, game, attributes = {
        'title': None, #none means dont set it
        'minimum_size': (168, 120),
        'resizable': True,
        'always_on_top': True
    }):
        super().__init__(size=WINDOW_SIZE)

        self.game = game

        for attr, value in attributes.items():
            if value:
                setattr(self, attr, value)

        #link to wnd_proc
        self.hwnd = win32gui.GetForegroundWindow()
        self.old_wnd_proc = win32gui.SetWindowLong(self.hwnd, win32con.GWL_WNDPROC, lambda *args: self.wnd_proc(*args))

    def wnd_proc(self, hwnd, message, wparam, lparam):
        #update during a size / position change
        if message in [win32con.WM_MOVE, win32con.WM_SIZE, win32con.WM_TIMER]:
            #remind game that we actually want to keep looping
            #we want framerate to be uncapped here so waiting for clock to tick doesn't slow moving / resizing down
            self.game.loop(0)
        
        return win32gui.CallWindowProc(self.old_wnd_proc, hwnd, message, wparam, lparam)

    def handle_event(self, event):
        pass

    def tick(self, dt):
        pass

    def draw(self, screen):
        screen.fill(
            (((sin(pygame.time.get_ticks() / 1000) + 1) / 2) * 255, 0, 0)
        )

class Game:
    def __init__(self):
        self.done = False

        self.clock = pygame.Clock()

        self.frames = [Frame(self)]

        pygame.init()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                if event.window:
                    self.frames.remove(event.window)

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.done = True
                pygame.quit()
                raise SystemExit

            # JUST GOING TO PASS EVENTS TO FOCUSED WINDOW FOR NOW
            # CHANGE LATER IF NECESSARY
            for frame in self.frames: 
                if frame.focused:
                    frame.handle_event(event)

            #test code
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.frames.append(Frame(self))

    def tick(self, dt):
        for frame in self.frames:
            frame.tick(dt)

    def draw(self):
        for frame in self.frames:
            frame.draw(frame.get_surface())
            frame.flip()

    def loop(self, framerate = FRAMERATE):
        dt = self.clock.tick(framerate) / 1000

        self.handle_events()
        self.tick(dt)
        self.draw()

    def run(self):
        while not self.done:
            self.loop()

Game().run()
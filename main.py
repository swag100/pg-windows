import pygame
import win32api
import win32gui
import win32con

DISPLAY_SIZE_REAL = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
DISPLAY_SIZE = ((DISPLAY_SIZE_REAL[1] / 3) * 4, DISPLAY_SIZE_REAL[1])

WINDOW_SIZE = tuple(int(x / 6) for x in DISPLAY_SIZE)
MINIMUM_SIZE = tuple(WINDOW_SIZE[i] / 2 + (8 if i == 0 else 0) for i in range(len(WINDOW_SIZE)))
FRAMERATE = 60

GRAVITY = 3

class Frame(pygame.Window):
    def __init__(self, game, attributes = {
        'title': None, #none means dont set it
        'position': pygame.WINDOWPOS_CENTERED,
        'minimum_size': (168, 120),
        'maximum_size': DISPLAY_SIZE,
        'resizable': True,
        'always_on_top': True
    }):
        super().__init__(size=WINDOW_SIZE)

        self.game = game

        for attr, value in attributes.items():
            if value:
                setattr(self, attr, value)

        self.game.tiles.append(pygame.Rect(*self.position, self.size[0], 16))
        self.game.tiles.append(pygame.Rect(self.position[0], self.position[1] + self.size[1], self.size[0], 16))

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

    def handle_event(self, event):
        pass

    def tick(self, dt):
        pass

    def draw(self, screen):
        screen.fill('black')

class Entity:
    def __init__(self, game, position, size):
        self.game = game
        self.rect = pygame.FRect(*position, *size)

        self.velocity = [0, 0]

    def collision(self, tiles):
        collisions = []

        if self.velocity[1] > 0:
            for tile in tiles:
                if self.rect.colliderect(tile):
                    collisions.append(tile)

        return collisions
    
    def move(self, amount):
        """
        self.rect.x += amount[0]
        for tile in self.collision(self.game.tiles):
            self.velocity[0] = 0

            if amount[0] > 0:
                self.rect.right = tile.left
            if amount[0] < 0:
                self.rect.left = tile.right
        """

        self.rect.y += amount[1]
        for tile in self.collision(self.game.tiles):
            self.velocity[1] = 0

            #if amount[1] < 0: self.rect.top = tile.bottom
            if amount[1] > 0:
                self.rect.bottom = tile.top

    def handle_event(self, event):
        pass

    def tick(self, dt):
        pass

    def draw(self, screen):
        pass

class Player(Entity):
    def __init__(self, game):
        self.game = game

        self.x_speed = 100

        self.frame = None

        super().__init__(game, (0, 0), (16, 16))

    def tick(self, dt):
        keys = pygame.key.get_pressed()

        self.velocity[0] += (keys[pygame.K_d] - keys[pygame.K_a]) * self.x_speed * dt
        self.velocity[1] += GRAVITY * dt

        self.move(self.velocity)

        #TODO: find the frame we draw ourselves in based on position

    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)

class Game:
    def __init__(self):
        pygame.init()

        self.done = False
        self.clock = pygame.Clock()

        self.tiles = []
        self.frames = [Frame(self)]
        self.entities = [Player(self)]


        print(self.tiles)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.WINDOWCLOSE:
                if event.window:
                    self.frames.remove(event.window)
                    event.window.destroy() 

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

        for entity in self.entities:
            entity.tick(dt)

    def draw(self):
        for frame in self.frames:
            frame.draw(frame.get_surface())
            frame.flip()

        for entity in self.entities:
            goodframe = None
            for frame in self.frames:
                if frame.focused:
                    goodframe = frame
            if goodframe:
                entity.draw(goodframe.get_surface())
                goodframe.flip()
            #TODO: find CORRECT window to draw on!
            #entity.draw()

    def loop(self, framerate = FRAMERATE):
        dt = self.clock.tick(framerate) / 1000

        self.handle_events()
        self.tick(dt)
        self.draw()

    def run(self):
        while not self.done:
            self.loop()

Game().run()

"""
frame.position = (
    (((math.sin(pygame.time.get_ticks() / 1000) + 1) / 2) * (win32api.GetSystemMetrics(0) - 100 - WINDOW_SIZE[0])) + 100,
    (((math.cos(pygame.time.get_ticks() / 1000) + 1) / 2) * (win32api.GetSystemMetrics(1) - 100 - WINDOW_SIZE[1])) + 100
)

frame.opacity = ((math.sin(time.time()) + 1) / 2)
"""

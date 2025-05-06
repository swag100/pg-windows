
import win32api

DISPLAY_SIZE_REAL = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
DISPLAY_SIZE = ((DISPLAY_SIZE_REAL[1] / 3) * 4, DISPLAY_SIZE_REAL[1])

WINDOW_SIZE = tuple(int(x / 6) for x in DISPLAY_SIZE)
MINIMUM_SIZE = tuple(WINDOW_SIZE[i] / 2 + (8 if i == 0 else 0) for i in range(len(WINDOW_SIZE)))
FRAMERATE = 60

GRAVITY = 16
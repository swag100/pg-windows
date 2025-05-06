import pygame
import win32api

DISPLAY_SIZE_REAL = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
DISPLAY_SIZE = ((DISPLAY_SIZE_REAL[1] / 3) * 4, DISPLAY_SIZE_REAL[1])

WINDOW_SIZE = tuple(int(x / 6) for x in DISPLAY_SIZE)
MINIMUM_SIZE = tuple(WINDOW_SIZE[i] / 2 + (8 if i == 0 else 0) for i in range(len(WINDOW_SIZE)))
FRAMERATE = 60

GRAVITY = 16

def sub_rect(r1, r2):
    """remove the area of r2 from r1"""
    if not r1.colliderect(r2):
        return [r1]

    clip = r2.clip(r1)

    #first we have to see if there is a complete rect to each side of the removing rect
    need_com_left = False
    need_com_right = False
    need_com_top = False
    need_com_bottom = False

    if clip.left > r1.left:
        need_com_left = True
    if clip.right < r1.right:
        need_com_right = True
    if clip.top > r1.top:
        need_com_top = True
    if clip.bottom < r1.bottom:
        need_com_bottom = True

    left = None
    right = None
    top = None
    bottom = None

    if need_com_left: #ok, we also need to check top and bottom here...
        t = r1.top
        b = r1.bottom - r1.top
        l = r1.left
        r = clip.left - r1.left
        if need_com_top: #we need to cut a bit off the top of this
            t = clip.top
        if need_com_bottom:
            b = clip.bottom - t

        left = pygame.Rect(l, t, r, b)
    if need_com_right:
        t = r1.top
        b = r1.bottom - r1.top
        l = clip.right
        r = r1.right - clip.right
        if need_com_top:
            t = clip.top
        if need_com_bottom:
            b = clip.bottom - t

        right = pygame.Rect(l, t, r, b)
    if need_com_top:
        top = pygame.Rect(r1.left, r1.top, r1.width, clip.top-r1.top)
    if need_com_bottom:
        bottom = pygame.Rect(r1.left, clip.bottom, r1.width, r1.bottom-clip.bottom)

    ret = []
    for i in [left, right, top, bottom]:
        if i: ret.append(i)

    return ret

def sub_rect_list(r1, rl):
    dirty = [r1]
    for i in rl:
        new = []
        for x in dirty:
            new.extend(sub_rect(x, i))
        dirty = new
    return dirty
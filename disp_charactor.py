import sys
import random

import pygame
from pygame.locals import *

#画面サイズ
SCREEN_SIZE = (600, 500)

#渡されたrgbカラーを、変更して返す
def colorChange():
    r_color = [ColorInt(),ColorInt(),ColorInt()]
    return r_color

def ColorInt():
    n = random.randint(0,255)
    return  n

def main():
    #pygameの初期化
    pygame.init()
    clock = pygame.time.Clock()

    #タイトルバーの設定(大きさ)
    screen = pygame.display.set_mode(SCREEN_SIZE)

    #タイトルバーのテキスト
    # pygame.display.set_caption("Test")
    pygame.display.set_caption("Game")

    # 背景色
    color_random = [0,0,0]

    while True:
        
        #画面の背景色を変更する
        color_random = colorChange()
        screen.fill(color_random)

        #画面を更新
        pygame.display.update()

        #イベント処理
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == QUIT:
                pygame.quit() #Pygame の終了(画面閉じられる)
                sys.exit()

        delta = clock.tick(5) # 60fps → 5fps

if __name__ == "__main__":
    main()
import sys
import pygame
from pygame.locals import *

#画面サイズ
SCREEN_SIZE = (600, 500)

def main():
    #pygameの初期化
    pygame.init()

    #タイトルバーの設定(大きさ)
    screeen = pygame.display.set_mode(SCREEN_SIZE)

    #タイトルバーのテキスト
    # pygame.display.set_caption("Test")
    pygame.display.set_caption("Game")

    while True:
        #画面を黒色に塗りつぶし
        screeen.fill((0,255,0))

        #画面を更新
        pygame.display.update()

        #イベント処理
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == QUIT:
                pygame.quit() #Pygame の終了(画面閉じられる)
                set.exit()

if __name__ == "__main__":
    main()
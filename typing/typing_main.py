import sys
import random

import pygame
from pygame.locals import *

#画面サイズ
SCREEN_SIZE = (1280, 720)

#プレイヤー画像のファイルパス
PLAYER_IMG_PATH = "/Users/hs_ji/Documents/GitHub/SimpleGamePython/images/enaga.png"

class Player(pygame.sprite.Sprite):
    print("test")


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
    color = [50,50,50]

    # フォントの設定
    font = pygame.font.Font(None, 55)

    # 描画する文字列の設定
    question = "SELECT"
        
    #ユーザー入力変数
    user_input = ""


    # プレイヤー画像の取得
    player = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
    player = pygame.transform.scale(player, (32,32))
    player_rect = player.get_rect()

    # プレイヤー画像の初期位置
    player_rect.center = (300, 250)

    running = True  # ループ処理の実行を継続するフラグ

    while running:
        
        # #画面の背景色を変更する
        screen.fill(color)
        # キャラクターの表示
        screen.blit(player, player_rect)

        #イベント処理
        for event in pygame.event.get():
            #閉じるボタンが押されたら終了
            if event.type == QUIT:
                pygame.quit() #Pygame の終了(画面閉じられる)
                sys.exit()
            if event.type == KEYDOWN:
                print(user_input)
                if event.key == K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == K_RETURN:
                    if user_input == question:
                        print("正解！")
                        # 新しい問題に切り替え
                        user_input = ""
                        question = random.choice(["SELECT", "FROM", "WHERE"])
                    else:
                        print("不正解")
                else:
                    user_input += event.unicode

            # 文字の描画
            text_question = font.render(question, True, (255,255,255))
            text_input = font.render(user_input, True, (0, 255, 0))

            screen.blit(text_question, [20, 100])
            screen.blit(text_input, (20, 200))

            #画面を更新
            pygame.display.update()

            delta = clock.tick(60) # 60fps → 5fps

if __name__ == "__main__":
    main()
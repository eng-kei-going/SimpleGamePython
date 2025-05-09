import sys
import random
from pathlib import Path
from enum import Enum

import pygame
from pygame.locals import *

class GameState(Enum):
    TITLE = 1
    PLAYING = 2
    RESULT = 3

# ----------------------------
# 環境設定
# ----------------------------
DEBUG_MODE = False
BASE_DIR = Path(__file__).parent
PLAYER_IMG_PATH = BASE_DIR / "images" / "enaga.png"

# ----------------------------
# 定数
# ----------------------------
SCREEN_SIZE = (1280, 720)
BG_COLOR = (50,50,50)
FONT_SIZE = 55
PLAYER_SIZE = (32, 32)
WORD_LIST = ["SELECT", "FROM", "WHERE", "JOIN", "UPDATE"]
TIME_LIMIT = 10

# ----------------------------
# プレイヤー画像の取得
# returns: (player, rect) - 描画用画像とその座標
# ----------------------------
def load_player():
    player = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
    player = pygame.transform.scale(player, PLAYER_SIZE)
    rect = player.get_rect()
    rect.center = (300, 250)
    return player, rect

# ----------------------------
# 初期化処理
# returns: (screen, font, clock) - 画面、フォント、FPSの定義（定数を参照）
# ----------------------------
def init_game():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Typing Game")
    font = pygame.font.Font(None, FONT_SIZE)
    return screen, font, clock


# ----------------------------
# 開始画面
# ----------------------------
def show_title(screen, font):
    title_running = True
    while title_running:
        screen.fill(BG_COLOR)

        # タイトル表示
        text1 = font.render("Typing Game", True, (255, 50, 50))
        text2 = font.render("Press any key to start", True, (100, 100, 100))

        # 位置調整（中央に表示）
        text1_rect = text1.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3))
        text2_rect = text2.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 80))

        # 描画
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)

        pygame.display.update()

        #入力でゲーム開始
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return

# ----------------------------
# 終了画面
# スコアを表示する
# ----------------------------
def show_result(screen, font, score):
    wait_ticks = pygame.time.get_ticks() + 300
    result_running = True
    while result_running:
        screen.fill(BG_COLOR)

        # メッセージ表示
        text1 = font.render("TIME UP!", True, (255, 50, 50))
        text2 = font.render(f"Your Score: {score}", True, (255, 255, 255))
        text3 = font.render("Press any key to exit", True, (100, 100, 100))

        # 位置調整（中央に表示）
        text1_rect = text1.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3))
        text2_rect = text2.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 80))
        text3_rect = text3.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 160))

        # 描画
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)

        pygame.display.update()

        #入力で終了
        for event in pygame.event.get():
            now = pygame.time.get_ticks()
            if now < wait_ticks:
                continue #入力を無視する
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    return "RETRY"
                pygame.quit()
                sys.exit()

# ---------------------------- 
# メインループ
# ----------------------------
def main():
    screen, font , clock = init_game()
    player, player_rect = load_player()

    #変数の初期化
    score = 0
    elapsed = 0
    game_state = GameState.TITLE

    # 出題と入力変数の設定
    question = random.choice(WORD_LIST)
    user_input = ""

    running = True  # ループ処理の実行を継続するフラグ

    while running:
        
        if game_state == GameState.TITLE:
            show_title(screen, font)
            start_time = pygame.time.get_ticks()
            game_state = GameState.PLAYING

        elif game_state == GameState.PLAYING:
            #経過時間の計測
            elapsed = (pygame.time.get_ticks() - start_time) // 1000

            # #画面の背景色を変更する
            screen.fill(BG_COLOR)
            # キャラクターの表示
            screen.blit(player, player_rect)

            #イベント処理
            for event in pygame.event.get():
                #閉じるボタンが押されたら終了
                if event.type == QUIT:
                    pygame.quit() #Pygame の終了(画面閉じられる)
                    sys.exit()
                if event.type == KEYDOWN:
                    if DEBUG_MODE:
                        print(user_input)
                    if event.key == K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == K_RETURN:
                        if user_input == question:
                            print("正解！")
                            # 新しい問題に切り替え
                            user_input = ""
                            score += 1
                            question = random.choice(WORD_LIST)
                        else:
                            print("不正解")
                    else:
                        user_input += event.unicode

            # 描画処理
            # 問題文と回答（中央に表示）
            text_q = font.render(f"question: {question}", True, (255,255,255))
            text_a = font.render(f"answer: {user_input}", True, (0, 255, 0))
            # 中央に表示する為の位置計算
            # 入力文字の長さによる表示のブレを防ぐため、回答欄の表示位置は問題文と同じX座標とする
            text_q_rect = text_q.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3))
            text_a_rect = text_q.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 80))
            # 描画
            screen.blit(text_q, text_q_rect)
            screen.blit(text_a, text_a_rect)

            # プレイ状況（右上に表示）
            # 時間とスコア
            text_t = font.render(f"time: {elapsed} / {TIME_LIMIT}", True, (200,200,200))
            text_s = font.render(f"score: {score}", True, (50,50,200))
            text_t_rect = text_t.get_rect(topright=(SCREEN_SIZE[0] - 10, 10))
            text_s_rect = text_s.get_rect(topright=(SCREEN_SIZE[0] - 10, 55))
            screen.blit(text_t, text_t_rect)
            screen.blit(text_s, text_s_rect)

            if elapsed >= TIME_LIMIT:
                game_state = GameState.RESULT

        elif game_state == GameState.RESULT:
            if show_result(screen, font, score) == "RETRY":
                #再スタート処理
                score = 0
                user_input = ""
                question = random.choice(WORD_LIST)
                game_state = GameState.TITLE 
            else:
                running = False

        pygame.display.update()
        clock.tick(60)

# ----------------------------
# 実行エントリーポイント
# ----------------------------
if __name__ == "__main__":
    main()
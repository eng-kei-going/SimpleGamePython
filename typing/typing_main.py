import sys
import random
import json
from pathlib import Path
from enum import Enum

import pygame
from pygame.locals import *

class GameState(Enum):
    TITLE = 1
    PLAYING = 2
    RESULT = 3

class GameStatus:
    def __init__(self):
        self.score = 0
        self.user_input = ""
        self.question = ""
        self.explanation = ""
        self.is_correct = True
        self.feedback_text = ""
        self.feedback_time = 0

    def reset(self):
        self.score = 0
        self.user_input = ""
        self.set_new_question()
        self.feedback_text = ""
        self.feedback_time = 0

    def set_new_question(self):
        q = random.choice(QUESTION_LIST)
        self.question = q["question"]
        self.explanation = q["explanation"]

    def set_feedback(self, text, is_correct):
        """フィードバックメッセージ（正誤）と、その表示開始時刻を設定する"""
        self.feedback_text = text
        self.user_input = ""
        self.is_correct = is_correct
        self.feedback_time = pygame.time.get_ticks()

# ----------------------------
# 環境設定
# ----------------------------
DEBUG_MODE = False
BASE_DIR = Path(__file__).parent
PLAYER_IMG_PATH = BASE_DIR / "images" / "enaga.png"
FONT_PATH = BASE_DIR / "fonts" / "NotoSansJP-Regular.ttf"
QUESTION_JSON_PATH = BASE_DIR / "data" / "questions.json"

def load_questions_from_json(filepath):
    with open(str(filepath), encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# 定数
# ----------------------------
SCREEN_SIZE = (1280, 720)
FONT_SIZE = 48
EXFONT_SIZE = 32
PLAYER_SIZE = (32, 32)
TIME_LIMIT = 60
FEEDBACK_DURATION = 1000

QUESTION_LIST = load_questions_from_json(QUESTION_JSON_PATH)

# ----------------------------
# 色定数（用途 + コメントに色名）
# ----------------------------
COLOR_BACKGROUND = (50, 50, 50)              # dark gray
COLOR_TEXT_MAIN = (255, 255, 255)            # white
COLOR_TEXT_SUB = (180, 180, 180)             # light gray
COLOR_TEXT_TITLE = (100, 200, 255)           # light blue
COLOR_TEXT_INSTRUCTION = (100, 100, 100)     # gray
COLOR_TEXT_ANSWER = (0, 255, 0)              # green
COLOR_TEXT_TIMER = (200, 200, 200)           # gray
COLOR_TEXT_SCORE = (50, 50, 200)             # blue
COLOR_FEEDBACK = (255, 255, 0)               # yellow
COLOR_FEEDBACK_ERROR = (255, 50, 50)         # red

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
    font = pygame.font.Font(str(FONT_PATH), FONT_SIZE)
    exfont = pygame.font.Font(str(FONT_PATH),EXFONT_SIZE)
    return screen, font, exfont, clock

# ----------------------------
# フィードバックの描画
# ----------------------------
def draw_feedback(screen, font, status):
    """タイピング結果に対するフィードバックを描画（正誤に応じ色分け）"""
    now = pygame.time.get_ticks()
    if now - status.feedback_time < FEEDBACK_DURATION:

        # 正誤による色変更
        if status.is_correct:
            color = COLOR_FEEDBACK
        else:
            color = COLOR_FEEDBACK_ERROR

        fb_surface = font.render(status.feedback_text, True, color)
        fb_rect = fb_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 160))
        screen.blit(fb_surface, fb_rect)

# ----------------------------
# 開始画面
# ----------------------------
def show_title(screen, font):
    title_running = True
    while title_running:
        screen.fill(COLOR_BACKGROUND)

        # タイトル表示
        text1 = font.render("Typing Game", True, COLOR_TEXT_TITLE)
        text2 = font.render("Press any key to start", True, COLOR_TEXT_INSTRUCTION)

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
    wait_ticks = pygame.time.get_ticks() + 1000
    result_running = True
    while result_running:
        screen.fill(COLOR_BACKGROUND)

        # メッセージ表示
        text1 = font.render("TIME UP!", True, COLOR_FEEDBACK_ERROR)
        text2 = font.render(f"Your Score: {score}", True, COLOR_TEXT_MAIN)
        text3 = font.render("Press any key to exit  (R: Retry)", True, COLOR_TEXT_INSTRUCTION)

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
    status = GameStatus()

    def handle_correct_answer():
        status.set_feedback("Correct!", True)
        status.score += 1
        status.set_new_question()
    
    #ゲーム初期化
    screen, font, exfont, clock = init_game()
    player, player_rect = load_player()
    status.reset()
    game_state = GameState.TITLE

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
            screen.fill(COLOR_BACKGROUND)
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
                        print(status.user_input)
                    if event.key == K_BACKSPACE:
                        status.user_input = status.user_input[:-1]
                    elif event.key == K_RETURN:
                        if status.user_input == status.question:
                            handle_correct_answer()
                        else:
                            status.set_feedback("Wrong!", False)
                    else:
                        status.user_input += event.unicode

            # 問題文と回答を中央に表示
            text_q = font.render(f"Q: {status.question}", True, COLOR_TEXT_MAIN)
            text_ex = exfont.render(f" {status.explanation}", True, COLOR_TEXT_SUB)
            text_a = font.render(f"A: {status.user_input}", True, COLOR_TEXT_ANSWER)
            # 中央に表示する為の位置計算
            # 入力文字の長さによる表示のブレを防ぐため、回答欄の表示位置は問題文と同じX座標とする
            text_q_rect = text_q.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3))
            text_ex_rect = text_ex.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 50))
            text_a_rect = text_q.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 3 + 100))
            screen.blit(text_q, text_q_rect)
            screen.blit(text_ex, text_ex_rect)
            screen.blit(text_a, text_a_rect)

            # プレイ状況(時間とスコア)を右上に表示
            text_t = font.render(f"time: {elapsed} / {TIME_LIMIT}", True, COLOR_TEXT_TIMER)
            text_s = font.render(f"score: {status.score}", True, COLOR_TEXT_SCORE)
            text_t_rect = text_t.get_rect(topright=(SCREEN_SIZE[0] - 10, 10))
            text_s_rect = text_s.get_rect(topright=(SCREEN_SIZE[0] - 10, 55))
            screen.blit(text_t, text_t_rect)
            screen.blit(text_s, text_s_rect)

            draw_feedback(screen, font, status)

            if elapsed >= TIME_LIMIT:
                game_state = GameState.RESULT

        elif game_state == GameState.RESULT:
            if show_result(screen, font, status.score) == "RETRY":
                #再スタート処理
                status.reset()
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
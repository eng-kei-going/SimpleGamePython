import random
import pyttsx3

def read_text(text):
    engine = pyttsx3.init()

    engine.setProperty('rate',120)

      # 声を英語に変更
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()

answer = random.randint(1,10)
guess = 0
count = 0
text = ''

#print('test')

while guess != answer:
    text = '1～10 の かず を あててみて：'
    read_text(text)
    guess = int(input(text))
    count += 1
    if guess < answer:
        text = 'ちいさい よ' 
        print(text)
        read_text(text)
    elif guess > answer:
        text = 'おおきい よ'
        print(text)
        read_text(text)
    else:
        text = 'せいかい！！'
        print(text)
        read_text(text)
        text = f'{count} かい でした！！'
        print(text)
        read_text(text)
        
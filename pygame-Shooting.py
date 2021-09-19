import pygame as pg
import sys
import random
from time import sleep


흰색 = (255,255,255)
빨강 = (255,0,0)
화면가로길이 = 480
화면세로길이 = 640
바위이미지 = [f'rock{인덱스}.png' for 인덱스 in range(1,31)]
소리 = [f'explosion{인덱스}.wav' for 인덱스 in range(1,5)]

def 바위맞춘개수(count):
    global 화면
    font = pg.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 운석수 : ' + str(count), True, 흰색)
    화면.blit(text, (10,0))

def 바위놓친개수(count):
    global 화면
    font = pg.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 운석 수 : ' + str(count), True, 빨강)
    화면.blit(text, (340,0))

def 메시지출력(텍스트):
    global 화면, 게임오버사운드
    텍스트폰트 = pg.font.Font('NanumGothic.ttf', 60)
    텍스트 = 텍스트폰트.render(텍스트, True, 빨강)
    텍스트위치 = 텍스트.get_rect()
    텍스트위치.center = (화면가로길이 / 2, 화면세로길이 / 2)
    화면.blit(텍스트, 텍스트위치)
    pg.display.update()
    pg.mixer.music.stop()
    게임오버사운드.play()
    sleep(2)
    pg.mixer.music.play(-1)
    runGame()

def 충돌():
    global 화면
    메시지출력('전투기 파괴!')

def 게임오버():
    global 화면
    메시지출력('게임 오버!')

def drawObject(obj, x, y):
    global 화면, 시계
    화면.blit(obj, (x,y))

def initGame():
    global 화면, 시계, 배경, 전투기, 미사일, 폭파이미지, 미사일사운드, 게임오버사운드
    pg.init()
    화면 = pg.display.set_mode((화면가로길이, 화면세로길이))
    pg.display.set_caption('PyShooting')
    배경 = pg.image.load('background.png')
    전투기 = pg.image.load('fighter.png')
    미사일 = pg.image.load('missile.png')
    폭파이미지 = pg.image.load('explosion.png')
    pg.mixer.music.load('music.wav')
    pg.mixer.music.play(-1)
    미사일사운드 = pg.mixer.Sound('missile.wav')
    게임오버사운드 = pg.mixer.Sound('gameover.wav')
    시계 = pg.time.Clock()

def runGame():
    global 화면, 시계, 배경, 전투기, 미사일, 폭파이미지, 미사일사운드, 게임오버사운드

    전투기크기 = 전투기.get_rect().size
    전투기가로길이 = 전투기크기[0]
    전투기세로길이 = 전투기크기[1]

    x = 화면가로길이 * 0.45
    y = 화면세로길이 * 0.9
    전투기좌우방향 = 0
    전투기세로방향 = 0

    미사일좌우위아래 = []

    바위 = pg.image.load(random.choice(바위이미지))
    바위크기 = 바위.get_rect().size
    바위가로길이 = 바위크기[0]
    바위세로길이 = 바위크기[1]
    파괴사운드 = pg.mixer.Sound(random.choice(소리))

    바위가로위치 = random.randrange(0, 화면가로길이 - 바위가로길이)
    바위세로위치 = 0
    바위스피드 = 2

    바위충돌 = False
    개수 = 0
    바위놓친개수2 = 0

    onGame = False
    while not onGame:
        for 이벤트 in pg.event.get():
            if 이벤트.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if 이벤트.type == pg.KEYDOWN:
                if 이벤트.key == pg.K_LEFT:
                    전투기좌우방향 -= 5

                elif 이벤트.key == pg.K_RIGHT:
                    전투기좌우방향 += 5

                elif 이벤트.key == pg.K_UP:
                    전투기세로방향 -= 5
                
                elif 이벤트.key == pg.K_DOWN:
                    전투기세로방향 += 5

                elif 이벤트.key == pg.K_SPACE:
                    미사일사운드.play()
                    미사일좌우 = x + 전투기가로길이 / 2
                    미사일위아래 = y - 전투기세로길이
                    미사일좌우위아래.append([미사일좌우, 미사일위아래])


            if 이벤트.type == pg.KEYUP:
                전투기좌우방향 = 0

        drawObject(배경, 0,0)

        x += 전투기좌우방향
        y += 전투기세로방향
        if x < 0:
            x = 0
        elif x > 화면가로길이 - 전투기세로길이:
            x = 화면가로길이 - 전투기세로길이

        if y < 바위세로위치 + 바위세로길이:
            if (바위가로위치 > x and 바위가로위치 < x + 전투기가로길이) or (바위가로위치 + 바위가로길이 > x and 바위가로위치 + 바위가로길이 < x + 전투기가로길이):
                충돌()

        drawObject(전투기, x, y)

        if len(미사일좌우위아래) != 0:
            for i, bxy in enumerate(미사일좌우위아래): # enumerate는 몇 번째와 함께 보내준다.
                bxy[1] -= 20
                미사일좌우위아래[i][1] = bxy[1]

                if bxy[1] < 바위세로위치:
                    if bxy[0] > 바위가로위치 and bxy[0] < 바위가로위치 + 바위가로길이:
                        미사일좌우위아래.remove(bxy)
                        바위충돌 = True
                        개수 += 1


                if bxy[1] <= 0: # 만약에 위 화면을 나간다면
                    try:
                        미사일좌우위아래.remove(bxy) # 삭제해라 bxy를
                    except:
                        pass
                    
        if len(미사일좌우위아래) != 0:
            for bx, by in 미사일좌우위아래:
                drawObject(미사일, bx, by) # 미사일을 그려준다.

        바위맞춘개수(개수)

        바위세로위치 += 바위스피드

        if 바위세로위치 > 화면세로길이:
            바위 = pg.image.load(random.choice(바위이미지))
            바위크기 = 바위.get_rect().size
            바위가로길이 = 바위크기[0]
            바위세로길이 = 바위크기[1]

            바위가로위치 = random.randrange(0, 화면가로길이 - 바위가로길이)
            바위세로위치 = 0
            바위놓친개수2 += 1

        if 바위놓친개수2 == 3:
            게임오버()

        바위놓친개수(바위놓친개수2)

        if 바위충돌:
            drawObject(폭파이미지, 바위가로위치, 바위세로위치)
            파괴사운드.play()

            바위 = pg.image.load(random.choice(바위이미지))
            바위크기 = 바위.get_rect().size
            바위가로길이 = 바위크기[0]
            바위세로길이 = 바위크기[1]
            바위가로위치 = random.randrange(0, 화면가로길이 - 바위가로길이)
            바위세로위치 = 0
            파괴사운드 = pg.mixer.Sound(random.choice(소리))
            바위충돌 = False

            바위스피드 += 0.1
            if 바위스피드 >= 10:
                바위스피드 = 10

        drawObject(바위, 바위가로위치, 바위세로위치)

        pg.display.update()

        시계.tick(60)

    pg.quit()

initGame()
runGame()



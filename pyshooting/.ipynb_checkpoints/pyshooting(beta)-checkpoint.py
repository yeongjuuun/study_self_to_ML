#!/usr/bin/env python
# coding: utf-8
# %% [markdown]
# ## 파이슈팅.py

# %%

# %%


#게임 창
import random
import time
import pygame
import sys

from time import sleep
padWidth = 480         # 게임화면 가로크기
padHeight = 640        # 게임화면 세로크기
rockImage = ['./resources/rock.png']
explosionSound = []

# 게임 메시지 출력
def writeMessage(text):
    global gamePad
    textfont = pygame.font.Font('./resources/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()
    
#전투기가 운석과 충돌했을 때 메시지 출력
def crash():
    global gamePad
    writeMessage('전투기 파괴!')
    
# 게임 오버 메시지 보이기
def gameOver():
    global gamePad
    writeMessage('게임 오버!')

# 운석을 맞춘 개수 계산
def writeScore(count):
    global gamePad
    font = pygame.font.Font('./resources/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수:'+str(count), True, (255, 255, 255))
    gamePad.blit(text,(10,0))
    
#운석이 화면 아래로 통과한 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font('./resources/NanumGothic.ttf', 20)
    text = font.render('놓친 운석 :' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (360,0))



# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
def initGame():
    global gamePad, clock, background, fighter, missile, explosion
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('pyshooting')                                                           #게임 이름
    background = pygame.image.load("./resources/background.png")  #배경그림
    fighter = pygame.image.load("./resources/fighter.png")        #플레이어
    missile = pygame.image.load('./resources/missile.png')
    explosion = pygame.image.load('./resources/explosion.png')
    clock = pygame.time.Clock()
    
    
    
def runGame():
    global gamePad, clock, background, fighter, missile, explosion
    
    
    # 전투기 미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0
    
    #미사일 초기 위치
    missileXY = []
    
    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size # 운석크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    
    #운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2
    
    # 플레이어 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    
    # 플레이어 초기 위치 (x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:          # 게임 프로그램 종료
                pygame.quit()
                sys.exit()
                
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:    # 전투기 왼쪽으로 이동
                    fighterX -= 5
                    
                elif event.key == pygame.K_RIGHT: # 전투기 오른쪽으로 이동
                    fighterX += 5
                
                elif event.key == pygame.K_UP: # 전투기 위쪽으로 이동
                    fighterY -= 5
                
                elif event.key == pygame.K_DOWN: # 전투기 아래쪽으로 이동
                    fighterY += 5
                    
                elif event.key == pygame.K_SPACE: # 미사일발사
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
                    
                    
                    
            if event.type in [pygame.KEYUP]:     # 방향키를 떼면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    fighterY = 0
                
                    
        drawObject(background, 0, 0)                 # 배경 화면 그리기
        drawObject(fighter, x, y)               # 플레이어를 게임 화면의 (x,y) 좌표에 그림
        
        # 전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth
        
        y += fighterY
        if y < 0:
            y = 0
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight
            
        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()
                                      
        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY): # 미사일 요소에 대헤 반복함
                bxy[1] -= 10   # 총알의 y좌표 -10 (위로 이동)
                missileXY[i][1] = bxy[1]
                
                # 미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0]>rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                
                if bxy[1] <= 0: # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy)   #미사일 제거
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
        # 운석 맞춘 점수 표시
        writeScore(shotCount)
        
        rockY += rockSpeed # 운석 아래로 움직임
        
        #운석이 지구로 떨어진 경우
        if rockY > padHeight:
            #새로운 운석(랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1
            
        if rockPassed == 3: #운석 3개 놓치면 게임오버
            gameOver()
        
        # 농친 운석 수 표시
        writePassed(rockPassed)
            
        #운석을 맞춘 경우
        if isShot:
            #  운석 폭발
            drawObject(explosion, rockX, rockY) # 운석 폭발 그리기
            
            # 새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            isShot = False
            
            #운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10
            
            
        drawObject(rock, rockX, rockY)            # 운석 그리기
        
        pygame.display.update()                   # 게임화면을 다시그림
        
        clock.tick(60)                            # 프레임
        
    pygame.quit()
    
initGame()
runGame()

# %%

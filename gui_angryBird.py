'''
프로그램 이름: 앵그리 버드 게임 (Angry Birds Game)
사용 방법: 
- Space 키를 눌러 새의 발사 힘을 조정하고, 떼면 새가 발사됩니다.
- 항상 10초 내로 발사해야합니다. (제한 시간)  
- 모든 타겟을 맞추면 승리합니다.
- 제한 시간 10초가 초과되면 패배합니다.
'''

import gui_core as gui
import random, math, time

# 게임 윈도우 초기화
w = gui.Window(title='Angry Birds Game', width=800, height=600, interval=1/60)

# 이미지 로드
background_image = 'background.png' 
bird_image = 'bird.png' 
target_image = 'target.png' 
slingshot_image = 'slingshot.png' 

# 음악 로드
flying_sound = 'fly.wav'  # 새가 날아갈 때 재생할 소리 파일 
collision_sound = 'collision.wav'  # 충돌 시 재생할 소리 파일 
background_music = 'background.wav'  # 배경 음악 파일 

# 배경 이미지 생성
background = w.newImage(0, 0, background_image, new_width=800, new_height=600)
# 새총 이미지 생성
slingshot = w.newImage(70, 475, slingshot_image, new_width=60, new_height=100)
# 새(bird) 이미지 생성
bird = w.newImage(90, 450, bird_image, new_width=80, new_height=80)

# 게임 상태 변수 초기화
bird_velocity = [0, 0]  # 새의 속도 (x, y)
gravity = 0.5  # 중력 가속도
is_flying = False  # 새가 발사되었는지 여부
is_aiming = False  # 새를 발사 준비 중인지 여부
is_game_over = False  # 게임 종료 여부
flight_power = 0  # 발사 힘
score = 0  # 점수
game_start_time = 0  # 게임 시작 시간

# 점수 텍스트
score_text = w.newText(10, 10, 200, text='Score: 0', fill_color='black', anchor='nw')
w.internals얘는안봐도돼요.canvas.itemconfig(score_text, font=('Arial', 18))  # 점수 텍스트 크기 키우기

# 시간 텍스트
time_text = w.newText(10, 40, 200, text='Time: 0', fill_color='black', anchor='nw')
w.internals얘는안봐도돼요.canvas.itemconfig(time_text, font=('Arial', 18))  # 시간 텍스트 크기 키우기

# 상태 텍스트 (승리/패배), 핑크색으로 변경하고 크기 크게 하기
status_text = w.newText(400, 300, 200, text='', fill_color='magenta', anchor='center')
w.internals얘는안봐도돼요.canvas.itemconfig(status_text, font=('Arial', 48, 'bold'))  # 상태 텍스트 매우 크게 하기

targets = []  # 타겟 리스트
target_initial_positions = []  # 타겟 초기 위치 리스트
target_offsets = []  # 타겟 흔들림 오프셋 리스트

def is_position_valid(x, y, positions, min_distance=70):
    """
    주어진 위치가 기존 위치들과 일정 거리 이상 떨어져 있는지 확인하는 함수
    """
    for pos in positions:
        if math.hypot(x - pos[0], y - pos[1]) < min_distance:
            return False
    return True

def initialize_targets():
    """
    타겟을 랜덤한 위치에 생성하는 함수
    """
    global targets, target_initial_positions, target_offsets
    targets = []
    target_initial_positions = []
    target_offsets = [] # 흔들거림을 구현하기 위함

    # 새로운 타겟 랜덤 위치에 생성
    while len(targets) < 10:
        x = random.randint(400, 750)
        y = random.randint(50, 550)
        if is_position_valid(x, y, target_initial_positions):
            target = w.newImage(x, y, target_image, new_width=60, new_height=60)
            targets.append(target)
            target_initial_positions.append((x, y))
            target_offsets.append((random.uniform(-1, 1), random.uniform(-1, 1)))

def initialize(start_time):
    """
    게임 초기화 함수
    """
    global is_flying, bird_velocity, is_aiming, flight_power, game_start_time, is_game_over, background_music_playing

    # 새 상태 초기화
    is_flying = False
    is_aiming = False
    flight_power = 0
    bird_velocity = [0, 0]
    game_start_time = start_time
    is_game_over = False
    w.setText(status_text, '')
    w.setText(time_text, 'Time: 0')
    w.moveObject(bird, 90, 450)  # 새의 위치를 초기 위치로 설정

    # 타겟 초기화 (처음 게임 시작 시에만 랜덤 위치 설정)
    if not targets:
        initialize_targets()
        
    # 배경 음악 반복 재생
    def play_background_music():
        if not is_game_over:
            w.playSound(background_music)
            w.internals얘는안봐도돼요.master.after(11000, play_background_music)  # 11초 후 배경 음악 재생 (wav 파일 길이에 맞게 조정)
    play_background_music()  # 배경 음악 재생 시작

def update(current_time):
    """
    게임 업데이트 함수 (프레임마다 호출됨)
    """
    global is_flying, bird_velocity, gravity, is_aiming, flight_power, score, targets, target_offsets, game_start_time, is_game_over
        
    if w.keys['Escape']:
        w.stop() # 아예 창도 닫아버림
        return
    
    # 타겟을 흔들리게 함
    for i, target in enumerate(targets):
        initial_x, initial_y = target_initial_positions[i] # 각 타겟의 초기 위치와 흔들림 오프셋을 가져옴
        offset_x, offset_y = target_offsets[i]                 
        
        # 현재 시간에 따른 새로운 위치를 계산
        # math.sin과 math.cos를 사용하여 주기적으로 위치를 변동시킴
        new_x = initial_x + math.sin(current_time + offset_x) * 5
        new_y = initial_y + math.cos(current_time + offset_y) * 5
            
        # 계산된 새로운 위치로 타겟을 이동
        w.moveObject(target, new_x, new_y)  

    # 경과 시간 계산
    elapsed_time = current_time - game_start_time
    w.setText(time_text, f'Time: {int(elapsed_time)}')  # 흐른 시간을 표시
    
    # 10초가 넘으면 패배 (시간제한)
    if elapsed_time > 10:
        w.setText(status_text, '패배!')
        is_game_over = True
        w.playSound('')  # 배경 음악 중지
        return # 종료

    # 모든 타겟을 맞추면 승리
    if len(targets) == 0:
        w.setText(status_text, '승리!')
        is_game_over = True
        w.playSound('')  # 배경 음악 중지
        return # 종료
    
    if not is_flying:
        # Space 키가 눌린 상태인 경우
        if w.keys['space']:
            is_aiming = True
            flight_power += 1
            if flight_power > 100:
                flight_power = 100
        
        # Space 키가 떼어진 경우
        if not w.keys['space'] and is_aiming:
            w.playSound(flying_sound)  # 새가 날아갈 때 소리 재생
            bird_velocity[0] = flight_power / 2 
            bird_velocity[1] = -flight_power / 2
            is_flying = True
            is_aiming = False
            flight_power = 0            
        
        # 새총 위치에 새를 고정
        w.moveObject(bird, 92, 445)
    else:
        # 물리 법칙을 적용하여 새 위치 업데이트
        bx, by = w.getPosition(bird)
        bx += bird_velocity[0] # x축 속도에 따른 위치 변화
        by += bird_velocity[1] # y축 속도에 따른 위치 변화
        # 중력 가속도 적용 (아래로)
        bird_velocity[1] += gravity
        
        w.moveObject(bird, bx, by)
        
        # 타겟과의 충돌 체크
        for i, target in enumerate(targets):
            tx, ty = w.getPosition(target)
            # 물체 사이의 거리가 40보다 작을 때 충돌한 것으로 간주
            if abs(bx - tx) < 40 and abs(by - ty) < 40: 
                w.playSound(collision_sound)  # 충돌 시 소리 재생
                w.deleteObject(target) 
                targets.remove(target) # 충돌 시 삭제
                target_initial_positions.pop(i)
                target_offsets.pop(i)
                # 점수 업데이트 (10점 >> 총 100점이 만점)
                score += 10
                w.setText(score_text, f'Score: {score}')                
                break
            
        # 새가 화면 밖으로 나간 경우
        if by > w.internals얘는안봐도돼요.master.winfo_height():
            is_flying = False
            initialize(current_time)

w.initialize = initialize
w.update = update

w.start()

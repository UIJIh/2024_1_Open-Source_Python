'''
황의지 (20183163)
프로그램 이름: 앵그리 버드 게임 (Angry Birds Game)
전반적인 사용 방법: 
- 배경 음악과 새가 날아가는 소리, 충돌 소리가 포함돼있으니 소리를 켜주세요.
- 게임 목표는 제자리 운동하는 돼지를 새로 맞추어서 모두 없애는 것입니다.
- Space 키를 눌러 새의 발사 힘을 조정하고, 떼면 새(제 친구 얼굴입니다)가 발사됩니다.

- 새 위에 화살표와 계기판으로 분노 게이지(발사 힘)을 보여줍니다. 
    >>>>>>>> 추가 목표!!! (사용자에게 비행에 대한 정보(발사 힘)를 알려주기)
    >>>>>>>> 원래는 선으로 표현하는게 어려울 것이라고 "이산적으로 원 도형을 배치"하라고 조언 주셨으나
    >>>>>>>> 고생 끝에 선을 사용해서 연속적으로 표현했습니다. ^-^

- 모든 타겟을 새(제 친구 얼굴)로 맞추면 승리합니다.
- 레벨이 올라갈수록 타겟 돼지의 수는 늘어나고, 제한 시간이 줄어듭니다.(10초씩 마이너스)
- 제한 시간 안에 타겟을 모두 맞추지 못하면 실패합니다.
- 제한 시간, 점수(레벨 올라가면 0으로 다시 초기화), 레벨은 좌측 상단에 표시됩니다.
'''

'''
키 사용 방법:
"스페이스" 누르면 누른 시간만큼 날아가는 파워가 올라가고, 떼면 날아갑니다.
"esc" 누르면 게임을 강제 종료합니다.
"p" 누르면 모든 게임 동작들(돼지 움직임, 시간 흐름 등)이 정지합니다. 다시 "p" 누르면 재개합니다.
"s" 게임 시작 후 "10초 뒤"에 누르면 모든 타겟이 없어지면서 다음 레벨로 올라가거나 승리합니다. >>>>>>>> 치트키!!!
"r" 게임을 리셋합니다. TIMEOVER가 돼도 r 누르면 다시 시작합니다.
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
gage_image = 'dashboard.png'

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
# 분노 게이지판 이미지 생성
gage = w.newImage(32, 340, gage_image, new_width=110, new_height=90)

# 게임 상태 변수 초기화
bird_velocity = [0, 0]  # 새의 속도 (x, y)
flight_velocity = [0, 0]
gravity = 0.5  # 중력 가속도
is_flying = False  # 새가 발사되었는지 여부
is_aiming = False  # 새를 발사 준비 중인지 여부
is_game_over = False  # 게임 종료 여부
is_paused = False  # 게임 정지 여부
flight_power = 0  # 발사 힘
score = 0  # 점수
game_start_time = 0  # 게임 시작 시간
pause_start_time = 0  # 일시 정지 시작 시간
pause_duration = 0  # 일시 정지 시간 누적
current_level = 0  # 레벨은 항상 0으로 초기화
max_level = 5  # 조절 가능
is_level_up = False  # 레벨업 여부
background_music_playing = True  # 배경 음악 재생 상태

# 점수 텍스트
score_text = w.newText(10, 10, 200, text='Score: 0', fill_color='black', anchor='nw')
w.internals얘는안봐도돼요.canvas.itemconfig(score_text, font=('Arial', 18))  # 크기 키우기

# 시간 텍스트
time_text = w.newText(10, 40, 200, text='Time: 0', fill_color='black', anchor='nw')
w.internals얘는안봐도돼요.canvas.itemconfig(time_text, font=('Arial', 18))  # 크기 키우기

# 레벨 텍스트
level_text = w.newText(10, 70, 200, text=f'Level: 0', fill_color='black', anchor='nw')
w.internals얘는안봐도돼요.canvas.itemconfig(level_text, font=('Arial', 18))  

# 상태 텍스트 (승리/패배), 핑크색으로 변경하고 크기 크게 하기
status_text = w.newText(400, 300, 200, text='', fill_color='magenta', anchor='center')
w.internals얘는안봐도돼요.canvas.itemconfig(status_text, font=('Arial', 30, 'bold'))  # 상태 텍스트 매우 크게 하기

# 정지 상태 텍스트
pause_text = w.newText(400, 250, 200, text='정지', fill_color='red', anchor='center')
w.internals얘는안봐도돼요.canvas.itemconfig(pause_text, font=('Arial', 30, 'bold'))  # 정지 텍스트 매우 크게 하기

targets = []  # 타겟 리스트
target_initial_positions = []  # 타겟 초기 위치 리스트
target_offsets = []  # 타겟 흔들림 오프셋 리스트

# Constants
MAX_FLIGHT_POWER = 100  # threshold
ARROW_MAX_ANGLE = 180  # 화살표 최대 각도 
ARROW_BASE_X = 95  # 화살표 시작점 X 좌표
ARROW_BASE_Y = 430  # 화살표 시작점 Y 좌표
ARROW_LENGTH = 55  # 화살표 길이
ARROW_WIDTH = 50  # 화살표 너비 조정
ARROW_HEIGHT = 35  # 화살표 길이 조정
ARROW_THICKNESS = 4  # 화살표 두께 조정

####################### 추가 목표!! 사용자에게 현재 게임 상황에 대한 정보를 주기!! 분노게이지(발사 힘)를 계기판에 표시해줌!! 
def update_arrow(flight_power):
    # flight_power에 따라 각도 계산 
    angle_deg = 180 - (flight_power / MAX_FLIGHT_POWER) * ARROW_MAX_ANGLE

    x1 = ARROW_BASE_X + ARROW_LENGTH * math.cos(math.radians(angle_deg))
    y1 = ARROW_BASE_Y - ARROW_LENGTH * math.sin(math.radians(angle_deg))
    
    # 이전 화살표 삭제
    w.internals얘는안봐도돼요.canvas.delete("angle_line")
    
    # 새로운 화살표 그리기
    w.internals얘는안봐도돼요.canvas.create_line(
        ARROW_BASE_X, ARROW_BASE_Y, x1, y1,
        tags="angle_line",
        arrow="last",
        arrowshape=(ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS)
    )

# 배경 음악 반복 재생
def play_background_music():
    if not is_game_over and background_music_playing:
        w.playSound(background_music)
        w.internals얘는안봐도돼요.master.after(11000, play_background_music)  # 11초 후(거의 파일 길이) 배경 음악 재생 

# d만큼 떨어져있는지 확인
def is_far_enough(x, y, positions, min_distance=70):
    for pos in positions:
        if math.hypot(x - pos[0], y - pos[1]) < min_distance:
            return False
    return True

# 타겟을 랜덤한 위치에 생성
def initialize_targets(length=10):
    global targets, target_initial_positions, target_offsets
    # 기존 타겟 삭제
    for target in targets:
        w.deleteObject(target)
    targets = []
    target_initial_positions = []
    target_offsets = []  # 흔들거림을 구현하기 위함
    # 새로운 타겟 랜덤 위치에 생성
    while len(targets) < length:
        x = random.randint(400, 750)
        y = random.randint(50, 550)
        if is_far_enough(x, y, target_initial_positions):
            target = w.newImage(x, y, target_image, new_width=60, new_height=60)
            targets.append(target)
            target_initial_positions.append((x, y))
            target_offsets.append((random.uniform(-1, 1), random.uniform(-1, 1)))

# 새의 위치 초기화
def initialize_bird():
    w.setText(time_text, 'Time: 0')
    w.moveObject(bird, 90, 450)  # 새의 위치를 초기 위치로 설정

# 게임 초기화
def initialize(start_time, is_reset=False):
    global is_flying, bird_velocity, is_aiming, flight_power, game_start_time, is_game_over, background_music_playing, current_level, max_level, is_level_up, level_text, is_paused, pause_duration, score

    is_flying = False
    is_aiming = False
    flight_power = 0
    bird_velocity = [0, 0]
    game_start_time = start_time
    is_game_over = False
    is_paused = False
    pause_duration = 0
    score = 0  # 점수 초기화

    if is_reset:
        current_level = 0  # 레벨 초기화
    current_level += 1
    is_level_up = False

    w.setText(pause_text, '')  # 초기에는 텍스트를 비워서 보이지 않게 함
    w.setText(status_text, '')
    w.setText(level_text, f'Level: {current_level}')
    w.setText(score_text, 'Score: 0')  # 점수 텍스트 초기화
    initialize_bird()
    # 레벨에 따라 타겟 수 조정
    initialize_targets(10 + current_level * 2)  # 레벨이 올라갈수록 타겟 수 증가
    if background_music_playing:
        play_background_music()

# 업데이트 함수
def update(current_time):
    global is_flying, bird_velocity, gravity, is_aiming, flight_power, score, targets, target_offsets, game_start_time, is_game_over, current_level, max_level, is_level_up, flight_velocity, is_paused, pause_start_time, pause_duration, background_music_playing
    
    #################### 키입력 1 : 일시정지
    if w.keys['p']:
        is_paused = not is_paused
        if is_paused:
            pause_start_time = current_time
            w.setText(pause_text, '정지')  # 정지 상태 표시
        else:
            pause_duration += current_time - pause_start_time
            w.setText(pause_text, '')  # 정지 상태 해제
        w.keys['p'] = False

    if is_paused:
        time.sleep(0.1)  # 일시 정지 상태에서 CPU 사용률을 낮추기 위해 잠시 대기
        return
    
    #################### 키입력 2 : 종료
    if w.keys['Escape']:
        w.stop() 
        return
    
    #################### 키입력 3 : 리셋
    if w.keys['r']:
        initialize(current_time, is_reset=True)  # 레벨과 타겟을 초기화
        w.keys['r'] = False

    #################### 키입력 4 : 치트키
    if w.keys['s'] and current_time - game_start_time - pause_duration > 10:
        for target in targets:
            w.deleteObject(target)
        targets.clear() # 모두 깨주기
        w.keys['s'] = False

    if is_game_over:
        return    

    for i, target in enumerate(targets):
        initial_x, initial_y = target_initial_positions[i]
        offset_x, offset_y = target_offsets[i]                 
        new_x = initial_x + math.sin(current_time + offset_x) * 5
        new_y = initial_y + math.cos(current_time + offset_y) * 5
        w.moveObject(target, new_x, new_y)  
    
    if not is_game_over:
        elapsed_time = current_time - game_start_time - pause_duration
        time_limit = 60 - int(elapsed_time)
        w.setText(time_text, f'Time: {int(time_limit)}')

        if current_level == 2:
            time_limit = 50 - int(elapsed_time)
            w.setText(time_text, f'Time: {int(time_limit)}')
        elif current_level == 3:
            time_limit = 40 - int(elapsed_time)
            w.setText(time_text, f'Time: {int(time_limit)}')
        elif current_level == 4:
            time_limit = 30 - int(elapsed_time)
            w.setText(time_text, f'Time: {int(time_limit)}')
        elif current_level == 5:
            time_limit = 20 - int(elapsed_time)
            w.setText(time_text, f'Time: {int(time_limit)}')
        
        if time_limit <= 0:
            w.setText(status_text, 'TIME OVER')
            is_game_over = True
            w.playSound('')  # 배경 음악 중지
            w.setText(time_text, 'Time: 0')
            return
            
    if len(targets) == 0:
        # 레벨 다 클리어
        if current_level == max_level:
            w.setText(status_text, '승리')
            is_game_over = True
            is_level_up = False
            w.playSound('')
            w.setText(time_text, 'Time: 0')
            return
        else:
            # 레벨업
            is_level_up = True
            initialize(current_time)            
        return
    
    if not is_flying:
        #################### 키입력 4 : 새 날리기
        # Space 키가 눌린 상태인 경우
        if w.keys['space']:
            if background_music_playing:
                w.playSound('')  # 시끄러워서 그냥 게임 시작하면 배경 음악 중지
                background_music_playing = False
            is_aiming = True
            flight_power += 1            
            update_arrow(flight_power)
            if flight_power > 100:
                flight_power = 100   

        # Space 키가 떼어진 경우
        if not w.keys['space'] and is_aiming:
            w.playSound(flying_sound)
            bird_velocity[0] = flight_power / 2 
            bird_velocity[1] = -flight_power / 2
            is_flying = True
            is_aiming = False
            flight_power = 0                    
            update_arrow(flight_power)
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
            # 물체 사이의 거리가 40 미만 충돌한 것으로 간주
            if not is_far_enough(bx, by, [(tx, ty)], min_distance=55): # 충돌 감지 거리 더 좁히기 가능함 (일단 깨기 쉽게 올림)
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
            # 분노게이지 화살과 새 다시 제자리로 돌려놓기
            update_arrow(flight_power)
            initialize_bird()

# main
w.initialize = initialize
w.update = update
time.sleep(1)
play_background_music()
initialize_targets() 
w.start()
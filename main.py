#------------------------------------------------------
# Author: Michael Luo and Deeksha Tandon
# Name of game: SYNC
# Date modified: May 8, 2023
#
# A rhythm game where you need to click the corresponding key at the correct time. 
# This program teaches music.
#------------------------------------------------------

# Import modules
import pygame
from pygame import mixer

# initial pygame
pygame.init()  

# window size
WINDOW_WIDTH = int(960)     # half the size of 1920, the size of the program window
WINDOW_HEIGHT = int(540)    # half the size of 1080, the size of the program window

# Set up the display window 
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# sets the caption name at the top of the window
pygame.display.set_caption("SYNC") 

# Set up the clock object   
clock = pygame.time.Clock() 

# define colours
COLOUR_RED = (255,15,15)
COLOUR_WHITE = (255,255,255)
COLOUR_BLACK = (0,0,0)

# size of circles for mouse over button effects
NORMAL_CIRCLE_RADIUS = int(20)  # the radius of the red circle that appears when hovering over a button on many screens
SMALL_CIRCLE_RADIUS = int(15)   # the radius of the white circle that appears when hovering over a button on the exit confirmation screen

NORMAL_CIRCLE_OFFSET = int(32)  # how far to the side the circle is from the button

# stuff for the game --------------------------------------
PROGRESS_BAR_LENGTH = int(410)  # the length of the progress bar
level_sequence = []         # order that circles appear in
next_note = float()         # what time the next circles need to be spawned in at

# lanes----------------------------------------------------
LANE1_Y = int(267)          # the y location of the top lane
LANE2_Y = int(317)          # the y location of the middle lane
LANE3_Y = int(367)          # the y location of the bottom lane

lane1_circle_list = []      # list of all circles currently on the top lane
lane2_circle_list = []      # list of all circles currently on the middle lane
lane3_circle_list = []      # list of all circles currently on the bottom lane  

speed = int()               # the number of pixels to move by, increasing this increases the speed of the circles

# scoring in game ----------------------------------------

# defining accuracy
EVALUATION_LINE = int(120)  # the x of the evaluation line
perfect_min_range = int()   # how far to the right of the evaluation line you can be while still scoring perfect
perfect_max_range = int()   # how far to the left of the evaluation line you can be while still scoring perfect
good_min_range = int()      # how far to the right of the evaluation line you can be while still scoring good
good_max_range = int()      # how far to the left of the evaluation line you can be while still scoring good
bad_min_range = int()       # how far to the right of the evaluation line you can be while still scoring bad
bad_max_range = int()       # how far to the left of the evaluation line you can be while still scoring bad

# showing accuracy message
DURATION = int(100)         # the length of time that a message in game is blit to screen in number of frames
counter1 = int()           # counts the remaining time a message will be displayed for lane 1
counter2 = int()           # counts the remaining time a message will be displayed for lane 2
counter3 = int()           # counts the remaining time a message will be displayed for lane 3
text1 = int()              # the message displayed on lane 1
text2 = int()              # the message displayed on lane 2
text3 = int()              # the message displayed on lane 3

# points awarded
PERFECT_BASE_POINTS = 200   # the amount of points the player gets for scoring a perfect before any modifiers
GOOD_BASE_POINTS = 70       # the amount of points the player gets for scoring a good before any modifiers
BAD_BASE_POINTS = 20        # the amount of points the player gets for scoring a bad before any modifiers

# score
score_game = int(0)         # in game score 
real_score = float(0)       # the score while being put through a counting affect before being shown
displayed_score = int(0)    # the score currently shown on screen

# combo
combo = int(0)              # the players current combo streak
max_combo = int(0)          # the players best streak during a game

# counts the number of these messages the player gets in a game
number_of_perfects = int(0) 
number_of_goods = int(0)
number_of_bads = int(0)
number_of_misses = int(0)

# audio -----------------------------------------------
lobby_music = str("music/TimTaj_In_House.mp3")  # background music

# framerate--------------
framerate = int(0)
STANDARD_FPS = int(60)

# set up fonts------------------------------------------------------------
tinyfont = pygame.font.Font("fonts/lexend/static/Lexend-Regular.ttf",10)
smallfont = pygame.font.Font("fonts/lexend/static/Lexend-Regular.ttf",20)
mediumfont = pygame.font.Font("fonts/lexend/static/Lexend-Regular.ttf",35)
largefont = pygame.font.Font("fonts/lexend/static/Lexend-Regular.ttf",40)

# Title Button positions-------------------------------------------------
button_start = pygame.Rect(90,280,165,40)
button_exit = pygame.Rect(90,336,125,40)

# exit confirmation buttons----------------------------------------------
button_confirm = pygame.Rect(265,345,185,35)
button_exit_back = pygame.Rect(547,345,120,35)

# main menu button positions---------------------------------------------
button_game = pygame.Rect(45,87,150,40)
button_lesson = pygame.Rect(45,150,210,40)
button_quiz = pygame.Rect(45,224,135,40)
button_result = pygame.Rect(45,292,200,40)
button_back = pygame.Rect(45,363,140,40)

# level result button positions------------------------------------------
result_button_leave = pygame.Rect(105,460,148,37)
result_button_replay = pygame.Rect(355,460,165,37)

# lesson buttton positions ---------------------------------------------
lesson_button_back = pygame.Rect(40,449,127,54)
lesson_button_next = pygame.Rect(788,449,127,54)

# quiz button positions--------------------------------------------------
quiz_button_start = pygame.Rect(416,368,145,37)
quiz_button_next = pygame.Rect(805,469,90,26)

quiz_button_1 = pygame.Rect(65,130,830,68)
quiz_button_2 = pygame.Rect(65,205,830,68)
quiz_button_3 = pygame.Rect(65,283,830,68)
quiz_button_4 = pygame.Rect(65,363,830,68)

# quiz result button positions-------------------------------------------
result_button_back = pygame.Rect(80,473,140,37)

# ranges for scoring in game---------------------------------------------
perfect_min_range = EVALUATION_LINE + 6   
perfect_max_range = EVALUATION_LINE - 6   
good_min_range = EVALUATION_LINE + 15     
good_max_range = EVALUATION_LINE - 15    
bad_min_range = EVALUATION_LINE + 35     
bad_max_range = EVALUATION_LINE - 35  

# which lesson image is currently shown
current_lesson = int(0)

# declare variables for quiz-----------------------------------------------------------------
quiz_score = int(0)          # the players score in the quiz
NUM_OF_QUESTIONS = int(5)    # the number of questions in the quiz
quiz_percentage = int()      # the percent of questions the player got correct
total_score = str()          # a fracton with the number of question they got right over total number of questions
questions = []               # list containg the all the questions and their answers
quiz_start = bool()          # if we are the starting page of the quiz
question_num = int()         # the current question the player is answering
selection = str("")          # which multiple choice option is selected

# transition -----------------------------------------------------------
transition = False             # used to stop a transition once its done
TRANSITION_SPEED = float(60)   # the speed of the transition

# images ---------------------------------------------------------------
title_image = pygame.image.load("images/title_page.png").convert()            # image for title page
main_menu_image = pygame.image.load("images/main_menu.png").convert()         # Load an image for main menu page
game_image = pygame.image.load("images/game_background.png").convert()        # image for game
game_result_image = pygame.image.load("images/game_result.png").convert()     # image for level result
credits_image = pygame.image.load("images/credits_page.png").convert()        # image for credits
result_image = pygame.image.load("images/result_screen.png").convert()        # image for quiz result
quiz_start_image = pygame.image.load("images/quiz1_image.png").convert()      # image for first page of quiz
quiz_image = pygame.image.load("images/quiz2_image.png").convert()            # image for different questions in quiz

# lesson images ---------------------------------------
lesson_one = pygame.image.load("images/lesson_images/Lesson_image_1.png").convert()
lesson_two = pygame.image.load("images/lesson_images/Lesson_image_2.png").convert()
lesson_three = pygame.image.load("images/lesson_images/Lesson_image_3.png").convert()
lesson_four= pygame.image.load("images/lesson_images/Lesson_image_4.png").convert()
lesson_five = pygame.image.load("images/lesson_images/Lesson_image_5.png").convert()
lesson_six = pygame.image.load("images/lesson_images/Lesson_image_6.png").convert()
lesson_seven = pygame.image.load("images/lesson_images/Lesson_image_7.png").convert()
lesson_eight = pygame.image.load("images/lesson_images/Lesson_image_8.png").convert()
lesson_nine = pygame.image.load("images/lesson_images/Lesson_image_9.png").convert()
lesson_ten = pygame.image.load("images/lesson_images/Lesson_image_10.png").convert()
lesson_eleven= pygame.image.load("images/lesson_images/Lesson_image_11.png").convert()

lesson_list = [lesson_one, lesson_two, lesson_three, lesson_four, lesson_five, lesson_six, lesson_seven, lesson_eight, lesson_nine, lesson_ten, lesson_eleven]

# some images are all 1920 x 1080 so we need to resize them to fit
title_image = pygame.transform.scale(title_image,(WINDOW_WIDTH, WINDOW_HEIGHT))
main_menu_image = pygame.transform.scale(main_menu_image,(WINDOW_WIDTH, WINDOW_HEIGHT))
game_image = pygame.transform.scale(game_image,(WINDOW_WIDTH, WINDOW_HEIGHT))

# target circle for game
CIRCLE_IMAGE_WIDTH = 42
circle_image = pygame.image.load("images/sync_circle2.png").convert_alpha()   
circle_image = pygame.transform.scale(circle_image,(CIRCLE_IMAGE_WIDTH, CIRCLE_IMAGE_WIDTH))

# sets the image icon
pygame.display.set_icon(circle_image)


# -----------------------------------------Subprograms----------------------------------------------------


# draws a circle to indicate the mouse is hovering over a certain button
def mouse_hover(button_location,circle_size,x_offset=0,y_offset=0, default_colour = COLOUR_WHITE, highlight_colour = COLOUR_RED):
    # finds the location for the circle using the button location
    circle_location_x = button_location[0] - x_offset
    circle_location_y = button_location[1] + button_location[3]//2 - y_offset
    circle_location = (circle_location_x, circle_location_y)            

    # Check if the mouse is within the rectangle of the button
    if button_location.collidepoint(mouse_x, mouse_y):
        
        # creates a circle beside the button to indicate the mouse is hovering over it
        pygame.draw.circle(screen, highlight_colour, circle_location, circle_size)
    else:
        # replaces the circle with a circle if mouse is not hovering over the button
        pygame.draw.circle(screen, default_colour, circle_location, circle_size) 


# play music
def play_music(song_file_path, volume = 0.4, repetitions=-1):
    mixer.music.load(song_file_path)
    # Set volume
    mixer.music.set_volume(volume)
    # Start playing the music
    mixer.music.play(repetitions)

# opens a file and returns a list containg all the lines from the file
def read_file(file):
    file_lines = ""
    with open(file) as file:
        for line in file:
            file_lines += line
    file_list=file_lines.split("\n")    
    return file_list

# opens a file a returns a list containg lists that contain the data from a line
def read_file2(file):
    file_list = []
    with open(file) as file:
        file_lines = file.readlines()
    
    # turn each line into a list containing the data
    for i in range(len(file_lines)):
        file_list.append(file_lines[i].split())
    
    return file_list
    
# moves all the circle targets along the same lane a certain distance to the left
def move_lane_of_circles(circle_list, y_position,speed):
    for i in range(len(circle_list)):
        current_x = int(circle_list[i][0])
        new_x = current_x-speed
        circle_list[i][0] = new_x
        
        # drawing circles on lane
        screen.blit(circle_image, (circle_list[i][0],y_position))  
        
# sets streak to zero
def break_combo():
    global combo
    combo = 0
    
# increases combo by 1
def add_combo():
    global combo
    combo += 1

# awards score based on distance of circle to the target
def accuracy_range(circle_position):
    global score_game
    global combo   
    
    # update score and combo for perfect accuracy 
    if circle_position < perfect_min_range and circle_position > perfect_max_range:
        score_game += PERFECT_BASE_POINTS*(combo+1)
        add_combo()
        global number_of_perfects
        number_of_perfects += 1 
        return "1"   
    
    # update score and combo for good accuracy
    elif circle_position < good_min_range and circle_position > good_max_range:
        score_game += GOOD_BASE_POINTS*(combo+1) 
        add_combo()             
        global number_of_goods
        number_of_goods += 1         
        return "2" 
    
    # update score and combo for bad accuracy 
    elif circle_position < bad_min_range and circle_position > bad_max_range:   
        score_game += BAD_BASE_POINTS*(combo+1)
        add_combo()
        global number_of_bads
        number_of_bads += 1   
        return "3" 
    
    # update score and combo for misses
    else:            
        break_combo()
        global number_of_misses
        number_of_misses += 1        
        return "4" 
    
# creates the score counting effect 
def score_count_effect():
    global score_game
    global real_score
    
    if score_game - real_score <= 0:
        real_score = score_game
    elif score_game - real_score <=100:
        real_score += 0.5
    elif score_game - real_score <=200:
        real_score += 2
    elif score_game - real_score <=300:
        real_score += 5
    elif score_game - real_score <=450:
        real_score += 15
    else:
        real_score += 80   


# handles a lane of circles during the game
def game_lane(lane_num, lane_y, circle_list, counter, text, key, speed):
    message = ""
    # moves all the circles in the lane by a certain amount
    move_lane_of_circles(circle_list, lane_y, speed)
    
    # checks if those circles have moved off screen
    try:
        if circle_list[0][0] <= -CIRCLE_IMAGE_WIDTH:
            circle_list.pop(0)
            break_combo()
            counter = DURATION
            text = 4            
    except IndexError:
        None    
    
    # handles the key presses
    if key:
        try: 
            circle_position = circle_list[0][0] + CIRCLE_IMAGE_WIDTH//2
            # awarding score based on accuracy to the target
            message = accuracy_range(circle_position)
            # removes the circle
            circle_list.pop(0)
        except IndexError:
            None
            
    # the remaining part is responsible for the drawing a message telling the player their timing             
    if message == "1":                
        counter = DURATION
        text = 1
    elif message == "2":
        counter = DURATION
        text = 2
    elif message == "3":
        counter = DURATION
        text = 3
    elif message == "4":
        counter = DURATION
        text = 4

    if counter > 0:
        counter -= 1
        # display result on screen
        if text == 1:
            draw_text(smallfont, "Perfect!", COLOUR_BLACK, (155,lane_y-5))
        if text == 2:
            draw_text(smallfont, "Good", COLOUR_BLACK, (155,lane_y-5))
        if text == 3:
            draw_text(smallfont, "Bad", COLOUR_BLACK, (155,lane_y-5))
        if text == 4:
            draw_text(smallfont, "Miss!", COLOUR_BLACK, (155,lane_y-5))          
    
    return text, counter 


# used to draw text on to the screen
def draw_text(font_size, text, colour, location):
    rendered_text = font_size.render(text, True, colour)
    screen.blit(rendered_text, location)

# creates the progress bar showing level completion
def progress_bar(total_size, increment_timing, x, y, colour, height=10):
    length = total_size * increment_timing
    progress_bar = pygame.Rect(x,y,length,height)
    pygame.draw.rect(screen, colour, progress_bar)
    # circle the create a rounded look to the bar
    pygame.draw.circle(screen, colour, (x+int(length),y+height//2),height//2)


# program title screen
def title():
    global game_state
    
    if transition == True:
        transition_end(title_image)    
    
    # Display the title image on the screen    
    screen.blit(title_image, (0, 0))
    
    mouse_hover(button_start, NORMAL_CIRCLE_RADIUS, NORMAL_CIRCLE_OFFSET)
    mouse_hover(button_exit, NORMAL_CIRCLE_RADIUS, NORMAL_CIRCLE_OFFSET)
    
    # checks for button presses        
    if mouse_up:
        # start button
        if button_start.collidepoint(mouse_x, mouse_y):
            # move to menu screen
            transition_start(title_image)
            game_state = "menu"
        # exit button
        if button_exit.collidepoint(mouse_x, mouse_y):
            game_state = "exit screen"


# exit screen that appears on title screen
def exit_screen():
    global game_state
    
    # show are you sure screen
    exit_confirmation_screen = pygame.image.load("images/exit_confirmation_screen.png")
    image_width = exit_confirmation_screen.get_width()
    image_height = exit_confirmation_screen.get_height()                
    
    exit_confirmation_screen = pygame.transform.scale(exit_confirmation_screen,(image_width//2, image_height//2))

    # placing menu in center of screen
    image_width = exit_confirmation_screen.get_width()
    image_height = exit_confirmation_screen.get_height()
    screen.blit(exit_confirmation_screen, (WINDOW_WIDTH/2-image_width/2, WINDOW_HEIGHT/2-image_height/2))
        
    # creating mouse hover effects 
    mouse_hover(button_confirm,SMALL_CIRCLE_RADIUS,23,-2,COLOUR_BLACK, COLOUR_WHITE)
    mouse_hover(button_exit_back,SMALL_CIRCLE_RADIUS,23,-5,COLOUR_BLACK, COLOUR_WHITE)
    
    # checking for button presses
    if mouse_up:
        if button_confirm.collidepoint(mouse_x, mouse_y):
            game_state = "credits"
            transition_start(title_image)
        elif button_exit_back.collidepoint(mouse_x, mouse_y):
            game_state = "title"
      
            
# the main menu
def menu():
    global game_state
    global quiz_start
    
    # Display the image on the screen
    screen.blit(main_menu_image, (0, 0))        
    
    if transition == True:
        transition_end(main_menu_image)
        
    # code for buttons on main menu, handles mouse hovering over a button
    mouse_hover(button_game,NORMAL_CIRCLE_RADIUS,45)
    mouse_hover(button_lesson,NORMAL_CIRCLE_RADIUS,45)
    mouse_hover(button_quiz,NORMAL_CIRCLE_RADIUS,45)
    mouse_hover(button_result,NORMAL_CIRCLE_RADIUS,45)
    mouse_hover(button_back,NORMAL_CIRCLE_RADIUS,45)
    
    # if a button has been pressed it will send the player to the corresponding screen
    if mouse_up:
        if button_game.collidepoint(mouse_x, mouse_y):
            game_state="game"
            transition_start(main_menu_image)
        elif button_lesson.collidepoint(mouse_x, mouse_y):
            game_state="lesson"
            transition_start(main_menu_image)
        elif button_quiz.collidepoint(mouse_x, mouse_y):
            game_state="quiz"
            quiz_start = True
            transition_start(main_menu_image)
        elif button_result.collidepoint(mouse_x, mouse_y):
            game_state="result"
            transition_start(main_menu_image)
        elif button_back.collidepoint(mouse_x, mouse_y):
            game_state="title"
            transition_start(main_menu_image)
     
            
# game start allows things to be done only once per play through such as loading music
def game_start():
    global score_game
    global combo
    global maxcombo
    
    if transition == True:
        transition_end(game_image)
    
    # resets stats
    score_game = 0
    combo = 0
    maxcombo = 0
    
    # get level data
    level_sequence = read_file2("levels/level1.txt")
           
    # stop the current music and play the music for the level
    level_music = level_sequence.pop(0)
    level_music = level_music.pop()
    play_music(level_music)

    speed = level_sequence.pop(0)
    speed = float(speed.pop())
    
    # get length of song in seconds
    level_music_sound = pygame.mixer.Sound(level_music)
    song_length = level_music_sound.get_length()
    
    level(song_length, level_sequence, speed, score_game)


# the actual game that you play
def level(song_length, level_sequence, speed, score_game):
    
    global game_state
    global max_combo
    global combo
    
    # set fps to 120
    framerate = STANDARD_FPS
    framerate = framerate*2
    
    counter1 = 0
    counter2 = 0
    counter3 = 0
    text1 = 0
    text2 = 0
    text3 = 0
    
    level_running = True
    while level_running:
        
        key1 = False
        key2 = False
        key3 = False    
    
        # check events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
    
            # keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    key1 = True
                if event.key == pygame.K_s:
                    key2 = True
                if event.key == pygame.K_d:
                    key3 = True
                    
        # increase the frame rate cap of the program to 120
        clock.tick(framerate)
        
        # Load the image for game and display the image on the screen
        screen.blit(game_image, (0, 0))       
        
        # get position of song in milliseconds and converts it to seconds
        current_song_position = pygame.mixer.music.get_pos()
        current_song_position = current_song_position/1000
        
        # get the song completion percentage
        # +1 is there so that it doesn't try to divide by 0
        song_completed_percent = 1/(song_length/(current_song_position+1))
        
        # create a progress bar
        progress_bar(PROGRESS_BAR_LENGTH, song_completed_percent, 264,32, COLOUR_BLACK)       
        
        # this calculates the time it takes for the note to get to the evaluation line in order to get when the next note needs to be spawned
        next_note = current_song_position + ((WINDOW_WIDTH+CIRCLE_IMAGE_WIDTH/2-EVALUATION_LINE)/speed/framerate)
        
        # spawns circles at edge of screen 
        try: 
            if float(level_sequence[0][0]) <= next_note:
                
                if level_sequence[0][1] == "1":
                    # list that stores the location of all circles on lane 1
                    lane1_circle_list.append([WINDOW_WIDTH,LANE1_Y])
        
                if level_sequence[0][2] == "1":
                    # list that stores the location of all circles on lane 2
                    lane2_circle_list.append([WINDOW_WIDTH,LANE2_Y])
                    
                if level_sequence[0][3] == "1":
                    # list that stores the location of all circles on lane 3
                    lane3_circle_list.append([WINDOW_WIDTH,LANE3_Y])  
                    
                # removes the first item in list so that we start looking at second item
                level_sequence = level_sequence[1:len(level_sequence)]
        except IndexError:
            None
        
        text1, counter1 = game_lane(1, LANE1_Y, lane1_circle_list, counter1, text1, key1,speed)
        text2, counter2 = game_lane(2, LANE2_Y, lane2_circle_list, counter2, text2, key2,speed)
        text3, counter3 = game_lane(3, LANE3_Y, lane3_circle_list, counter3, text3, key3,speed)
        
        # keeps track of the players longest streak
        if max_combo < combo:
            max_combo = combo
        
        # displays the score during game
        score_count_effect()
        displayed_score = round(real_score)
        
        # draw score and combo
        draw_text(mediumfont,str(displayed_score),COLOUR_BLACK,(825,25)) 
        draw_text(mediumfont,str(combo) + "x",COLOUR_BLACK,(835,460))
        
        pygame.display.flip()
        
        # end game when song is done
        if song_completed_percent >= 0.99:
            level_running = False
    
    # show the results of the game
    game_state = "game result"
    transition_start(game_image)
            
    # return the framerate to 60
    framerate = STANDARD_FPS
        
        
# a screen containing the players stats for a game 
def game_result():
    global game_state
    
    screen.blit(game_result_image, (0, 0))
    
    if transition == True:
        transition_end(game_result_image)
    
    # display result on screen
    draw_text(largefont,str(score_game),COLOUR_BLACK,(190,130))
    draw_text(largefont,str(max_combo)+"x",COLOUR_BLACK,(210,185))

    # display accuracy
    draw_text(mediumfont,"Perfect: "+str(number_of_perfects),COLOUR_BLACK,(540,90))
    draw_text(mediumfont,"Good: "+str(number_of_goods),COLOUR_BLACK,(540,140))
    draw_text(mediumfont,"Bad: "+str(number_of_bads),COLOUR_BLACK,(540,190))
    draw_text(mediumfont,"Miss: "+str(number_of_misses),COLOUR_BLACK,(540,240))
    
    mouse_hover(result_button_replay, NORMAL_CIRCLE_RADIUS, NORMAL_CIRCLE_OFFSET)
    mouse_hover(result_button_leave, NORMAL_CIRCLE_RADIUS, NORMAL_CIRCLE_OFFSET)
    
    # buttons for exit and replay
    if mouse_up:
        if result_button_replay.collidepoint(mouse_x, mouse_y):
            game_state = "game"
            transition_start(game_result_image)
        elif result_button_leave.collidepoint(mouse_x, mouse_y):
            game_state = "menu"  
            transition_start(game_result_image)
            # play music
            play_music(lobby_music) 

# quiz results
def result():
    global game_state
    
    screen.blit(result_image, (0, 0))
    
    # transition
    if transition == True:
        transition_end(result_image)
    
    # calculate the players percentage
    quiz_percentage = 100*(quiz_score/NUM_OF_QUESTIONS)
    quiz_percentage = str(round(quiz_percentage))+"%"
    
    total_score = (str(quiz_score)+"/"+str(NUM_OF_QUESTIONS))
    
    # chose appropriate comment 
    if quiz_score == 0:
        comment = "Abysmal"
    elif quiz_score == 1:
        comment = "Substandard"
    elif quiz_score == 2:
        comment = "adequate"
    elif quiz_score == 3:
        comment = "Nice"
    elif quiz_score == 4:
        comment = "great"        
    else:
        comment = "Superb!"
    
    # display total score, percent, and comment
    draw_text(largefont,total_score, COLOUR_BLACK, (455,235))
    draw_text(largefont,quiz_percentage,COLOUR_BLACK,(455,280))
    draw_text(largefont,comment,COLOUR_BLACK,(415,335))
    
    # the back button
    mouse_hover(result_button_back, NORMAL_CIRCLE_RADIUS, NORMAL_CIRCLE_OFFSET)
    if mouse_up:
        if result_button_back.collidepoint(mouse_x, mouse_y):
            game_state = "menu"
            transition_start(result_image)    


# play the lesson
def lesson():
    global current_lesson
    global game_state
    
    if transition == True:
        transition_end(lesson_one)    
    
    # blit the current lesson image
    screen.blit(lesson_list[current_lesson], (0,0))
    
    # buttons
    mouse_hover(lesson_button_back,NORMAL_CIRCLE_RADIUS,NORMAL_CIRCLE_OFFSET)
    mouse_hover(lesson_button_next,NORMAL_CIRCLE_RADIUS,NORMAL_CIRCLE_OFFSET)    
    
    if mouse_up:
        
        if lesson_button_back.collidepoint(mouse_x, mouse_y):
            current_lesson += -1
        if lesson_button_next.collidepoint(mouse_x, mouse_y):
            current_lesson += 1
    
    # returns the main menu once they complete lesson or back out
    if current_lesson == -1:
        game_state = "menu"
        transition_start(lesson_one)
        current_lesson = 0
    elif current_lesson == 11:
        game_state = "menu"
        transition_start(lesson_eleven)
        current_lesson = 0        

    
# play quiz
def quiz():
    
    global quiz_start
    global question_num
    global game_state
    global selection 
    global quiz_score
    
    # transition
    if transition == True:
        transition_end(quiz_start_image)
    
    # quiz start screen
    if quiz_start == True:
        quiz_score = 0
        question_num = 0
        screen.blit(quiz_start_image, (0, 0))
        
        mouse_hover(quiz_button_start,NORMAL_CIRCLE_RADIUS, NORMAL_CIRCLE_OFFSET)
        if mouse_up:
            if quiz_button_start.collidepoint(mouse_x, mouse_y):         
                quiz_start = False
                question_num += 1
                
    # actual quiz         
    else:
        screen.blit(quiz_image, (0,0))
        
        # gets questions and answers
        file = "quiz.txt"
        
        file_list = []
        with open(file) as file:
            file_lines = file.readlines()
        
        # turn each line into a list containing the data
        for i in range(len(file_lines)):
            file_list.append(file_lines[i].split("_"))    
        
        # draw text
        draw_text(mediumfont, str(question_num), COLOUR_BLACK, (550, 38))
        draw_text(smallfont, file_list[question_num-1][0], COLOUR_BLACK, (85, 90))
        draw_text(mediumfont, file_list[question_num-1][1], COLOUR_BLACK, (130, 140))
        draw_text(mediumfont, file_list[question_num-1][2], COLOUR_BLACK, (130, 215))
        draw_text(mediumfont, file_list[question_num-1][3], COLOUR_BLACK, (130, 293))
        draw_text(mediumfont, file_list[question_num-1][4], COLOUR_BLACK, (130, 373))
        
        # button hover effect
        mouse_hover(quiz_button_1,NORMAL_CIRCLE_RADIUS,NORMAL_CIRCLE_OFFSET)
        mouse_hover(quiz_button_2,NORMAL_CIRCLE_RADIUS,NORMAL_CIRCLE_OFFSET)
        mouse_hover(quiz_button_3,NORMAL_CIRCLE_RADIUS,NORMAL_CIRCLE_OFFSET)
        mouse_hover(quiz_button_4,NORMAL_CIRCLE_RADIUS,NORMAL_CIRCLE_OFFSET)
        mouse_hover(quiz_button_next,SMALL_CIRCLE_RADIUS,25)
        
        # to show the answer currently selected
        if selection == "A":
            pygame.draw.circle(screen, COLOUR_RED, (33, 165), 25)
        if selection == "B":
            pygame.draw.circle(screen, COLOUR_RED, (33, 240), 25)
        if selection == "C":
            pygame.draw.circle(screen, COLOUR_RED, (33, 318), 25)
        if selection == "D":
            pygame.draw.circle(screen, COLOUR_RED, (33, 398), 25)
            
        # mouse presses
        if mouse_up:
            
            # multiple choice buttons
            if quiz_button_1.collidepoint(mouse_x, mouse_y):
                selection = "A"
            if quiz_button_2.collidepoint(mouse_x, mouse_y):
                selection = "B"
            if quiz_button_3.collidepoint(mouse_x, mouse_y):
                selection = "C"
            if quiz_button_4.collidepoint(mouse_x, mouse_y):
                selection = "D"
            
            # next button
            if quiz_button_next.collidepoint(mouse_x, mouse_y):  
                
                # check if their answer was correct and moves to the next question
                if question_num < 5:
                    
                    correct_answer = file_list[question_num-1][5]
                    
                    if correct_answer == selection:
                        quiz_score += 1
                        
                    selection = ""
                    
                    question_num += 1
                
                # check if their answer was correct and displays result of quiz
                else:
                    
                    correct_answer = file_list[question_num-1][5]

                    if correct_answer == selection:
                        quiz_score += 1

                    selection = ""
                    
                    game_state = "result"
                    transition_start(quiz_image)
        

# display citations
def credits():
    global running
    
    transition_end(credits_image)
    
    # open file
    citations_list = read_file("credits.txt")
    
    x = 50
    y1 = WINDOW_HEIGHT
    height_of_text = (len(citations_list)*30+WINDOW_HEIGHT)
    
    # moves text up
    for b in range(height_of_text):
        
        # checks for the quit event
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    
        clock.tick(STANDARD_FPS)
        screen.blit(credits_image, (0, 0))
        
        # y1 is the starting y location of the text
        # y2 is the y location of the individual lines relative to y1
        y1 -= 1
        y2 = y1
        
        # draws all the text each frame
        for c in range(len(citations_list)):
            y2 += 30
            
            # moves text to side if indented
            if citations_list[c][0:1] == "\t":
                
                draw_text(tinyfont,citations_list[c][1:],COLOUR_WHITE,(x+40,y2))
                
            else:
                draw_text(tinyfont,citations_list[c],COLOUR_WHITE,(x,y2))
                
        pygame.display.flip()
            
    running = False

# transition animation start
def transition_start(background_image):
    global transition
    transition = True
    
    # sets a circles size to block most of the screen and places it out the edge of the window
    circle_radius = WINDOW_WIDTH//2
    location = WINDOW_WIDTH+circle_radius
    
    # moves the circle across the screen until it reaches the center of the screen where the program changes the game state
    while location > WINDOW_WIDTH/2:
        clock.tick(STANDARD_FPS)
        screen.blit(background_image, (0, 0))
        location -= TRANSITION_SPEED
        pygame.draw.circle(screen, COLOUR_RED, (int(location),WINDOW_HEIGHT//2), circle_radius)
        pygame.display.flip()

# transition animation end
def transition_end(background_image):
    global transition
    transition = False
    
    # sets the circle to the same size as the start of the transition and puts it where the start left off
    circle_radius = WINDOW_WIDTH//2
    location = WINDOW_WIDTH/2
    
    # move the circle off the screen
    while location > -circle_radius:
        clock.tick(STANDARD_FPS)
        screen.blit(background_image, (0, 0))
        location -= TRANSITION_SPEED
        pygame.draw.circle(screen, COLOUR_RED, (int(location),WINDOW_HEIGHT//2), circle_radius)
        pygame.display.flip()
        

# the main game loop        
def game_loop():
    
    global mouse_x
    global mouse_y
    global mouse_up
    global game_state
    global framerate
    global running
    
    game_state = "title"
    
    framerate = 60
    
    # play music
    play_music(lobby_music,0.3)
    
    # dictionary containing the different functions for different screens and their key
    game_states = {"title":title, "exit screen":exit_screen, "menu":menu, "game":game_start, "game result":game_result,"lesson":lesson, "quiz":quiz, "result":result, "credits":credits}
    
    # Game loop
    try:
        running = True
        while running:
            # Cap the frame rate to 60fps
            clock.tick(framerate)
            
            mouse_up = False
            
            # check events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    
                # ensures that buttons on subsequent pages are not pressed by requiring mouse_up to be False before mouse_up can be True
                if not mouse_up:
                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_up = True
                    else:
                        mouse_up = False 
                        
                mouse_x, mouse_y = pygame.mouse.get_pos()
            
            game_states[game_state]()
            
            # Update the display
            pygame.display.flip()
    
    except pygame.error:
        None
        
    # Quit Pygame
    pygame.quit()


#--------------------- main program -------------------------

game_loop()

    
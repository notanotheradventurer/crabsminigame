# Define variables for images
default madcrab = 'madcrab.png'
default madcrab_mask = 'madcrab_mask.webp'
default background = 'crabgame_bg.png'
default charm_amber_icon = 'charm_amber.webp'

# Initialize variables to avoid undefined variable errors
init:
    $ timer_jump = "timeout_label"
    $ time = 0.0
    $ charm_amber = 0
    $ points_to_win = 20  # Points required to win
    $ min_interval = 0.2  # Minimum interval between crab appearances
    $ initial_speed = 0.5  # Initial speed factor
    $ max_crabs = 5  # Maximum number of crabs at any time
    $ crabs = []  # Global crabs list to track remaining crabs

# Screen to show the countdown timer
screen countdown:
    zorder 2
    timer 1.0 repeat True action If(time > 0, true=SetVariable('time', time - 1), false=[Hide('countdown'), Jump(timer_jump)])
    text str(int(time)):
        xalign 0.5
        yalign 0.05
        size 40
        color "#FF0000"

# Screen for the grabacrab minigame
screen grabacrab(timer_duration=30, speed_increment=0.5):
    zorder 1
    default speed = initial_speed
    default elapsed_time = 0.0

    # Background image
    add background

    # Main grid
    grid 6 3:
        pos (363, 303)
        xsize 1138
        ysize 671
        spacing 20

        # Placeholder for crab images
        for i in range(18):
            if i in crabs:
                frame:
                    background None
                    xsize 180
                    ysize 180
                    align (0.5, 0.5)
                    imagebutton:
                        background None
                        idle madcrab
                        hover madcrab
                        focus_mask True
                        xalign 0.5
                        yalign 0.5
                        action [
                            Function(crabs.remove, i),
                            SetVariable('score', score + 1)
                        ]
            else:
                null

    # Timer to add crabs at dynamic intervals
    timer max(initial_speed / (1 + elapsed_time / 10), min_interval) action [
        Function(add_crab, elapsed_time, timer_duration, max_crabs),
        SetVariable('elapsed_time', elapsed_time + max(initial_speed / (1 + elapsed_time / 10), min_interval))
    ] repeat True

    # Display the score
    hbox:
        xalign 0.5
        yalign 0.97  # Adjusted to move down to the center bottom
        spacing 10
        text "Score: [score]" size 40 color "#FFFFFF"

    # Display charm amber icon and amount
    hbox:
        xalign 0.95  # Positioned to the lower right
        yalign 0.95
        spacing 10
        add charm_amber_icon:
            xsize 64
            ysize 64
        text str(charm_amber) size 40 color "#FFFFFF"

# Function to add a crab
init python:
    import random

    def add_crab(elapsed_time, timer_duration, max_crabs):
        global crabs
        if len(crabs) < 18:
            # As the game progresses, add more crabs, especially in the last 10 seconds
            num_new_crabs = min(max_crabs, max(1, int(len(crabs) * (1 + elapsed_time / timer_duration))))
            for _ in range(num_new_crabs):
                new_crab = random.randint(0, 17)
                if new_crab not in crabs:
                    crabs.append(new_crab)

# Label to call the grabacrab minigame
label play_grabacrab:
    # Set initial time for countdown
    $ time = 30.0
    $ score = 0
    $ elapsed_time = 0.0
    $ timer_jump = "timeout_label"
    # Reset crabs list
    $ crabs = []
    # Show countdown screen
    show screen countdown
    # Show grabacrab game
    call screen grabacrab(timer_duration=30, speed_increment=0.5)
    # Calculate remaining crabs and deduct from score
    $ remaining_crabs = len(crabs)
    $ score -= remaining_crabs
    if score < 0:
        $ score = 0
    jump end_game

# Label for timeout handling
label timeout_label:
    # Calculate remaining crabs and deduct from score
    $ remaining_crabs = len(crabs)
    $ score -= remaining_crabs
    if score < 0:
        $ score = 0
    jump end_game

label end_game:
    "Well well, it seems you have missed a few...."
    "Remaining crabs: [remaining_crabs]"
    "Adjusted Score: [score]"
    if score >= points_to_win:
        $ charm_amber += 1
        jump win_screen
    else:
        jump lose_screen
    return

label win_screen:
    "Congratulations! You won and earned a Charm Amber!"
    menu:
        "Play Again":
            jump play_grabacrab
        "Exit to Main Menu":
            return

label lose_screen:
    "Time's up! You didn't reach the target score."
    menu:
        "Try Again":
            jump play_grabacrab
        "Exit to Main Menu":
            return

label start:
    "Let's play the grabacrab game!"
    call play_grabacrab
    "Game over! You scored [score] points."
    return

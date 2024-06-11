# Define variables for images
default madcrab = 'madcrab.webp'
default madcrab_mask = 'madcrab_mask.webp'
default background = 'crabgame_bg.png'

# Initialize variables to avoid undefined variable errors
init:
    $ timer_jump = "timeout_label"
    $ time = 0.0

# Screen to show the countdown timer
screen countdown:
    zorder 2
    timer 1.0 repeat True action If(time > 0, true=SetVariable('time', time - 1), false=[Hide('countdown'), Jump(timer_jump)])
    text str(int(time)):
        xalign 0.5
        yalign 0.05
        size 40
        color "#FF0000"

# Screen for the minigame
screen whack_a_mole(timer_duration=30, speed_increment=0.5):
    zorder 1
    default crabs = []
    default speed = 1.0

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
                        focus_mask madcrab_mask
                        xalign 0.5
                        yalign 0.5
                        action [
                            Function(crabs.remove, i),
                            SetVariable('score', score + 1)
                        ]
            else:
                null

    # Timer to add crabs at random intervals
    timer 1.0 / speed action Function(add_crab, crabs) repeat True

    # Speed up the game over time
    timer 10.0 action SetVariable('speed', speed + speed_increment) repeat True

    # Display the score
    text "Score: [score]" xpos 0.5 ypos 0.95 size 40 color "#FFFFFF" xanchor 0.5 yanchor 0.5

# Function to add a crab
init python:
    import random

    def add_crab(crabs):
        if len(crabs) < 18:
            crabs.append(random.randint(0, 17))

# Label to call the minigame
label play_whack_a_mole:
    # Set initial time for countdown
    $ time = 30.0
    $ score = 0
    $ timer_jump = "timeout_label"
    # Show countdown screen
    show screen countdown
    # Show whack-a-mole game
    call screen whack_a_mole(timer_duration=30, speed_increment=0.5)
    return

label timeout_label:
    "Time ended! Your score is [score] points."
    return

label start:
    "Let's play the whack-a-mole game!"
    call play_whack_a_mole
    "Game over! You scored [score] points."
    return
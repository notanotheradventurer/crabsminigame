# game/ui.rpy

screen countdown:
    zorder 2
    timer 1.0 repeat True action If(time > 0, true=SetVariable('time', time - 1), false=[Hide('countdown'), Jump(timer_jump)])
    hbox:
        xalign 0.5
        yalign 0.05
        spacing 20
        frame:
            background None  # Transparent background
            xsize 300
            ysize COUNTDOWN_SIZE + 20  # Extra space for vertical centering
            align (0.0, 0.5)  # Left align within the frame
            text "Round: [round_number]":
                size HUD_SIZE
                color HUD_COLOR
                xalign 0.0  # Left align text
                yalign 0.5  # Vertically centered
        frame:
            background None  # Transparent background
            xsize 300
            ysize COUNTDOWN_SIZE + 20  # Extra space for vertical centering
            align (0.5, 0.5)  # Center align within the frame
            text str(int(time)):
                size COUNTDOWN_SIZE
                color "#FF0000"
                xalign 0.5  # Center align text
                yalign 0.5  # Vertically centered
        frame:
            background None  # Transparent background
            xsize 300
            ysize COUNTDOWN_SIZE + 20  # Extra space for vertical centering
            align (1.0, 0.5)  # Right align within the frame
            text "Top Score: [top_score]":
                size HUD_SIZE
                color HUD_COLOR
                xalign 1.0  # Right align text
                yalign 0.5  # Vertically centered

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
        yalign 0.97
        spacing 10
        text "Score: [score]" size 40 color "#FFFFFF"

    # Display charm amber icon and amount
    hbox:
        xalign 0.95
        yalign 0.95
        spacing 10
        add charm_amber_icon:
            xsize 64
            ysize 64
        text str(charm_amber) size 40 color "#FFFFFF"

screen marisol_layer_buttons():
    zorder 1
    add marisol_background
    $ marisol_attributes = get_marisol_attributes()

    for attribute, layer in layer_attributes:
        $ image_path = f"images/marisol/{attribute}.png"

        if layer is not None:
            if layer not in hidden_layers:
                imagebutton idle image_path hover image_path:
                    action [
                        Function(decrement_charm_amber),
                        Function(hide_layer, layer),
                        Return("return")  # Ensure return to stop further interaction
                    ]
        else:
            add image_path

screen marisol_dialogue_screen():
    zorder 2
    add marisol_background
    window:
        style "say_who_window"
        vbox:
            text "[marisol_text]" xalign 0.5 yalign 0.5

screen flash_screen:
    zorder 3
    add Solid("#FFFFFF")
    timer FLASH_DURATION action Hide("flash_screen")

screen reward_message_screen():
    zorder 4
    add Solid(REWARD_BACKGROUND_COLOR)
    text REWARD_TEXT:
        color REWARD_TEXT_COLOR
        size REWARD_TEXT_SIZE
        xalign 0.5
        yalign 0.5
    timer 1.5 action Hide("reward_message_screen")

screen charm_amber_options():
    modal True
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 10
        text "The goddess grants you a Charm Amber!" size 40 color REWARD_TEXT_COLOR
        textbutton "Spend Charm Amber" action Call("spend_charm_amber")
        textbutton "Play Again" action Return()
        textbutton "Exit to Main Menu" action Return()

screen overlay_click_blocker(message=None):
    zorder 10  # Higher than marisol_layer_buttons
    modal True  # Captures all clicks

    # Transparent frame to cover the screen
    frame:
        background None
        xysize (config.screen_width, config.screen_height)

        # Capture click and evaluate conditions
        imagebutton:
            idle im.Scale("images/transparent.png", config.screen_width, config.screen_height)
            hover im.Scale("images/transparent.png", config.screen_width, config.screen_height)
            focus_mask im.Scale("images/mask.png", config.screen_width, config.screen_height)
            action Function(handle_overlay_click)

    # Optional message to display
    if message:
        frame:
            background None  # Transparent frame background
            xalign 0.5
            yalign 0.5
            text "[message]":
                size 30
                color "#FFFFFF"
                xalign 0.5
                yalign 0.5
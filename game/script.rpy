# game/script.rpy

label start:
    "Let's play the grabacrab game!"
    call play_grabacrab from _call_play_grabacrab
    return

label play_grabacrab:
    $ time = 30.0
    $ score = 0
    $ elapsed_time = 0.0
    $ timer_jump = "timeout_label"
    $ crabs = []
    show screen countdown
    call screen grabacrab(timer_duration=30, speed_increment=0.5)
    $ remaining_crabs = len(crabs)
    $ score -= remaining_crabs
    if score < 0:
        $ score = 0
    jump end_game

label timeout_label:
    $ remaining_crabs = len(crabs)
    $ score -= remaining_crabs
    if score < 0:
        $ score = 0
    jump end_game

label end_game:
    # Calculate the final score by subtracting remaining crabs
    $ remaining_crabs = len(crabs)
    $ final_score = score - remaining_crabs
    if final_score < 0:
        $ final_score = 0
    
    # Provide feedback through Marisol
    if final_score >= points_to_win:
        $ marisol_text = "You did well, you missed " + str(remaining_crabs) + " crabs, so your total is " + str(final_score) + "."
        $ charm_amber += 1  # Award Charm Amber
        show screen flash_screen
        $ renpy.pause(FLASH_DURATION)
        hide screen flash_screen
    else:
        $ marisol_text = "You missed " + str(remaining_crabs) + " crabs, so your total is "  + str(final_score) + ". Better luck next time!"

    show screen marisol_dialogue_screen
    "[marisol_text]"
    hide screen marisol_dialogue_screen

    # Update the top score if the final score is higher
    $ update_top_score(final_score)

    if final_score >= points_to_win:
        show screen reward_message_screen
        $ renpy.pause(1.5)
        hide screen reward_message_screen

    # Call the new menu options label
    jump menu_options

label spend_charm_amber:
    $ layer_hidden = False  # Flag to track if a layer has been hidden

    while charm_amber > 0 or layer_hidden:
        if charm_amber > 0 and not layer_hidden:
            $ marisol_text = "The goddess demands a reward, but all I have is my clothing... so be it, it's yours to have! Take off an item of clothing."
            show screen marisol_dialogue_screen
            "[marisol_text]"  # Requires player to click to continue
            hide screen marisol_dialogue_screen
            $ update_marisol()
            show screen marisol_layer_buttons

            # Wait for the player to click an image button
            $ _result = ui.interact()
            hide screen marisol_layer_buttons
            $ layer_hidden = True  # Set the flag to true after interaction

        else:
            hide screen marisol_dialogue_screen
            hide screen marisol_layer_buttons
            
            # Show the overlay screen to capture clicks and display a message
            show screen overlay_click_blocker(message="Click to continue.")
            $ _result = ui.interact()  # Wait for the player to interact to continue
            hide screen overlay_click_blocker
            $ layer_hidden = False  # Reset the flag

            # Check if all layers are hidden and handle accordingly
            if total_layers <= 0:
                jump game_over

    # If no Charm Amber left and no layer to hide, return to menu options
    jump menu_options

label game_over:
    "All layers are hidden. Game over!"
    return

label round_2:
    $ update_top_score(score)
    $ round_number += 1
    "Round [round_number] starts now!"
    call play_grabacrab from _call_play_grabacrab_1
    return

label menu_options:
    menu:
        "Spend Charm Amber" if charm_amber > 0:
            jump spend_charm_amber
        "Play Again":
            $ round_number += 1
            jump play_grabacrab
        "Exit to Main Menu":
            return
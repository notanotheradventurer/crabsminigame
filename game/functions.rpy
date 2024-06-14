# game/functions.rpy

init python:
    import random
    import renpy.exports as renpy  # Ensure we can call jump from Python

    def add_crab(elapsed_time, timer_duration, max_crabs):
        global crabs
        if len(crabs) < 18:
            num_new_crabs = min(max_crabs, max(1, int(len(crabs) * (1 + elapsed_time / timer_duration))))
            for _ in range(num_new_crabs):
                new_crab = random.randint(0, 17)
                if new_crab not in crabs:
                    crabs.append(new_crab)

    def decrement_charm_amber():
        global charm_amber
        if charm_amber > 0:
            charm_amber -= 1

    def hide_layer(layer):
        global total_layers
        if layer not in hidden_layers:
            hidden_layers.append(layer)
            # Hide bottom_back if bottom_left is hidden
            if layer == "bottom_left":
                if "bottom_back" not in hidden_layers:
                    hidden_layers.append("bottom_back")
            update_marisol()
            total_layers -= 1  # Decrement total layers
            if total_layers <= 0:
                renpy.jump("game_over")  # Jump to game over when all layers are hidden

    def update_marisol():
        marisol_attributes = get_marisol_attributes()

        # Hide all images initially
        for layer, _ in layer_attributes:
            renpy.hide(f"marisol_{layer}")

        # Show images that are not hidden
        for layer, action in marisol_attributes.items():
            if action != "hidden":
                renpy.show(f"marisol_{layer}")

        # Refresh the screen for buttons
        renpy.show_screen("marisol_layer_buttons")

    def check_all_layers_hidden():
        # Check if all layers are hidden
        all_layers_hidden = all(layer in hidden_layers for layer, action in layer_attributes if layer is not None)
        return all_layers_hidden

    def update_top_score(new_score):
        global top_score
        if new_score > top_score:
            top_score = new_score
            persistent.top_score = top_score
            renpy.save_persistent()

    hidden_layers = []

    layer_attributes = [
        ("bottom_back", "bottom_back"),
        ("body", None),  # Not a button
        ("left_arm", None),  # Not a button
        ("right_arm", None),  # Not a button
        ("panties", "panties"),
        ("top", "top"),
        ("bottom_left", "bottom_left"),
        ("right_hand", None),  # Not a button
        ("shoulders", "shoulders"),
        ("cover", "cover"),
    ]

    def get_marisol_attributes():
        attributes = {layer: (layer if layer not in hidden_layers else "hidden") for layer, action in layer_attributes}
        return attributes

    # CLI functions for testing
    def hide_layer_cli(layer):
        if layer not in hidden_layers:
            hidden_layers.append(layer)
            update_marisol()
        else:
            print(f"Layer {layer} is already hidden.")

    def show_layer_cli(layer):
        if layer in hidden_layers:
            hidden_layers.remove(layer)
            update_marisol()
        else:
            print(f"Layer {layer} is not hidden.")

    def list_hidden_layers():
        print("Hidden Layers:", hidden_layers)

    def handle_overlay_click():
        global charm_amber

        # Check if all layers are hidden
        all_layers_hidden = check_all_layers_hidden()
        
        renpy.hide_screen('overlay_click_blocker')

        if all_layers_hidden or total_layers <= 0:
            # Display end game message and proceed to game over
            renpy.call("show_game_end")
        elif charm_amber > 0:
            renpy.jump("spend_charm_amber")
        else:
            renpy.jump("round_2")

# Define label for showing end game message
label show_game_end:
    $ marisol_text = "You Win! Click to end!"
    show screen marisol_dialogue_screen
    "[marisol_text]"
    hide screen marisol_dialogue_screen
    return

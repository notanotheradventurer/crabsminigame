# game/defaults.rpy

# Define variables for images and game settings
default madcrab = 'madcrab.png'
default madcrab_mask = 'madcrab_mask.webp'
default background = 'crabgame_bg.png'
default charm_amber_icon = 'charm_amber.webp'
default marisol_background = 'images/crabgame_dialogue.png'

# Variables to track state and scores
default timer_jump = "timeout_label"
default charm_amber = 0
default score = 0
default points_to_win = 30
default min_interval = 0.2
default initial_speed = 0.5
default max_crabs = 5
default crabs = []
default remaining_crabs = 0
default round_number = 1
default top_score = persistent.top_score if persistent.top_score is not None else 0
default final_score = 0  # Declare final_score as global

# Configuration for the HUD
define HUD_SIZE = 30
define HUD_MARGIN = 150
define HUD_COLOR = "#FFFFFF"
define COUNTDOWN_SIZE = HUD_SIZE + 10  # Slightly larger for visibility
define FLASH_DURATION = 0.3
define REWARD_TEXT = "The Goddess Rewards You A Charm Amber!"
define REWARD_TEXT_COLOR = "#FF9900"
define REWARD_TEXT_SIZE = 40
define REWARD_BACKGROUND_COLOR = "#000000"


default total_layers = 5  # Update this value to the number of layers there are to hide

# SCREEN Constants
# -----------------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024

# IMAGE Constants
# ----------------
ICON_PATH = './assets/icon/icon.png'

# MENU Constants — Bakery Theme
# -----------------------------------
MENU_BG_COLOR        = (245, 222, 179)  # wheat / cream
MENU_TITLE_COLOR     = (101, 56, 27)    # chocolate brown
MENU_TITLE_FONT_SIZE = 160
MENU_TITLE_Y_OFFSET  = 300

MENU_BTN_COLOR         = (183, 110, 75)   # rosy brown
MENU_BTN_HOVER_COLOR   = (210, 140, 100)  # light rosy brown (hover)
MENU_BTN_TEXT_COLOR    = (255, 248, 240)   # cream white
MENU_BTN_SHADOW_COLOR  = (120, 60, 30)    # brown shadow
MENU_BTN_FONT_SIZE     = 56
MENU_BTN_WIDTH         = 360
MENU_BTN_HEIGHT        = 80
MENU_BTN_BORDER_RADIUS = 20
MENU_BTN_SHADOW_OFFSET = 5
MENU_BTN_SPACING       = 110              # vertical spacing between buttons

# MAP Constants
# --------------
MAP_BG_COLOR         = (255, 255, 255)
MAP_SEPARATOR_COLOR  = (0, 0, 0)
MAP_SEPARATOR_WIDTH  = 4

MAP_KITCHEN_RATIO        = 0.55   # proportion of screen height for kitchen
MAP_INGREDIENT_BOX_RATIO = 0.70   # proportion of half-width for ingredient box
MAP_CUSTOMER_GAP_RATIO   = 0.35   # proportion of shop height left as gap for customers
MAP_COMPTOIR_HEIGHT      = 20     # height of the counter drawn at the top of the path
MAP_COMPTOIR_COLOR       = (180, 120, 60)  # wood-like brown

# PLAYER Constants
# ----------------
PLAYER_SIZE  = 30
PLAYER_SPEED = 5
PLAYER_1_COLOR = (220, 50, 50)   # red
PLAYER_2_COLOR = (50, 100, 220)  # blue
FPS = 60
TIME_FAST_FORWARD_SCALE = 10   # time multiplier when fast-forward key is held

# CUSTOMER Constants
# ------------------
CUSTOMER_SIZE              = 20
CUSTOMER_SPEED             = 80    # pixels per second
CUSTOMER_COLOR             = (100, 180, 100)   # green placeholder
CUSTOMER_ANGRY_COLOR       = (200, 80, 80)     # red when leaving angry
CUSTOMER_PATIENCE_BAR_W    = 60
CUSTOMER_PATIENCE_BAR_H    = 8
CUSTOMER_LABEL_FONT_SIZE   = 22
CUSTOMER_SPAWN_INTERVAL    = 8.0   # seconds between spawns
CUSTOMER_MAX_COUNT         = 3     # max simultaneous customers per zone
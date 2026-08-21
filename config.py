WIDTH = 1280
HEIGHT = 720
BASE_WIDTH = 1280
BASE_HEIGHT = 720
FPS = 60
CAMERA_ID = 0
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
RESULT_SAVE_PATH = "data/session_results.csv"
PATIENT_ID = "patient_001"
PATIENT_NAME = "Demo Patient"
TRAINING_DURATION = 90
NOTE_TYPE_HIT = "hit"
NOTE_TYPE_TAP = "tap"
NOTE_TYPE_HOLD = "hold"
NOTE_DISTANCE = 360
HOLD_BODY_LENGTH = 220
CALIBRATION_TIME = 3.0
SOUND_HIT = "assets/sounds/hit.wav"
SOUND_TAP = "assets/sounds/tap.wav"
SOUND_HOLD = "assets/sounds/hold.wav"
DIFFICULTIES = {
    "EASY": {"name":"Easy","bpm":60,"hit_radius":190,"tap_radius":180,"hold_time":0.5,"note_appear_time":2.8,"perfect_window":0.30,"good_window":0.50,"miss_window":0.85,"line_move_multiplier":0.6},
    "NORMAL": {"name":"Normal","bpm":70,"hit_radius":150,"tap_radius":140,"hold_time":0.8,"note_appear_time":2.2,"perfect_window":0.22,"good_window":0.38,"miss_window":0.65,"line_move_multiplier":1.0},
    "HARD": {"name":"Hard","bpm":85,"hit_radius":105,"tap_radius":95,"hold_time":1.1,"note_appear_time":1.35,"perfect_window":0.12,"good_window":0.24,"miss_window":0.42,"line_move_multiplier":1.7}
}
DEFAULT_DIFFICULTY = "NORMAL"
# =========================================================
# 菜单背景音乐配置
# =========================================================

MENU_MUSIC_PATH = "assets/music/menu_bgm.mp3"

# 菜单音乐相对于设置音量的比例
MENU_MUSIC_VOLUME_SCALE = 0.45

# 训练音乐音量比例
TRAINING_MUSIC_VOLUME_SCALE = 1.0

# 菜单音乐淡入时间，单位：毫秒
MENU_MUSIC_FADE_IN_MS = 1200

# 菜单音乐淡出时间，单位：毫秒
MENU_MUSIC_FADE_OUT_MS = 700
SONGS = {
    "Q": {"name":"Demo Training", "chart":"charts/demo.json"},
    "W": {"name":"Morning Gentle", "chart":"charts/song2.json"},
    "E": {"name":"Active Rhythm", "chart":"charts/song3.json"}
}

# 音乐路径



DEFAULT_SONG_KEY = "Q"
REST_REMINDER_TIME = 60
COUNTDOWN_SECONDS = 3
CALIBRATION_DURATION = 5.0
MIN_CALIBRATION_POINTS = 20
MIN_HAND_RANGE_X = 80
MIN_HAND_RANGE_Y = 60
LINE_LENGTH = 330
LINE_MOVE_AMPLITUDE = 45
LINE_MOVE_SPEED = 1.2
LINE_ROTATE_AMPLITUDE = 12
LINE_ROTATE_SPEED = 0.8
BACKGROUND = (12, 18, 28)
PANEL = (28, 40, 58)
WHITE = (245, 245, 245)
GRAY = (170, 170, 170)
GREEN = (80, 220, 150)
BLUE = (90, 180, 255)
YELLOW = (255, 220, 120)
RED = (255, 120, 120)
PURPLE = (190, 140, 255)
LINE_COLOR = BLUE
HAND_OUTER = GREEN
HAND_INNER = WHITE

DEFAULT_MUSIC_VOLUME = 0.75
DEFAULT_SOUND_VOLUME = 0.80
DEFAULT_SHOW_FPS = True

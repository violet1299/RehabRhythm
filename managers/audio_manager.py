import os
import pygame

from config import *


class AudioManager:
    """统一管理菜单音乐、训练音乐和音符音效。"""

    def __init__(self):
        self.music_loaded = False
        self.music_volume = DEFAULT_MUSIC_VOLUME
        self.sound_volume = DEFAULT_SOUND_VOLUME
        self.current_music_path = None
        self.current_music_type = None
        self.menu_music_path = MENU_MUSIC_PATH
        self.sounds = {}

    def load_music(self, path):
        """兼容旧代码：只加载训练音乐，不立即播放。"""
        if not path:
            print("训练音乐路径为空")
            self.music_loaded = False
            return False
        if not os.path.exists(path):
            print("未找到音乐文件:", path)
            self.music_loaded = False
            return False
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            self.music_loaded = True
            self.current_music_path = path
            self.current_music_type = "training"
            print("音乐加载成功:", path)
            return True
        except pygame.error as error:
            print("音乐加载失败:", error)
            self.music_loaded = False
            return False

    def play_music(self):
        """兼容旧代码：播放已经通过 load_music() 加载的训练音乐。"""
        if not self.music_loaded:
            print("没有可播放的训练音乐")
            return False
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops=0, start=0.0)
            self.current_music_type = "training"
            print("音乐开始播放")
            return True
        except pygame.error as error:
            print("音乐播放失败:", error)
            return False

    def play_menu_music(self, restart=False):
        """循环播放开始页、菜单页和结果页背景音乐。"""
        if not pygame.mixer.get_init():
            print("音频系统尚未初始化")
            return False
        if not os.path.exists(self.menu_music_path):
            print(f"菜单背景音乐不存在: {self.menu_music_path}")
            return False
        if (
            not restart
            and self.current_music_type == "menu"
            and pygame.mixer.music.get_busy()
        ):
            return True
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.menu_music_path)
            actual_volume = self.music_volume * MENU_MUSIC_VOLUME_SCALE
            pygame.mixer.music.set_volume(max(0.0, min(1.0, actual_volume)))
            pygame.mixer.music.play(loops=-1, fade_ms=MENU_MUSIC_FADE_IN_MS)
            self.music_loaded = True
            self.current_music_path = self.menu_music_path
            self.current_music_type = "menu"
            print(f"菜单背景音乐开始播放: {self.menu_music_path}")
            return True
        except pygame.error as error:
            print(f"菜单背景音乐播放失败: {error}")
            self.music_loaded = False
            return False

    def fadeout_menu_music(self):
        """进入倒计时时淡出菜单音乐。"""
        if not pygame.mixer.get_init() or self.current_music_type != "menu":
            return
        try:
            pygame.mixer.music.fadeout(MENU_MUSIC_FADE_OUT_MS)
            self.music_loaded = False
            self.current_music_type = None
            self.current_music_path = None
        except pygame.error as error:
            print(f"菜单音乐淡出失败: {error}")

    def play_training_music(self, music_path, restart=True):
        """播放一次当前谱面的训练音乐。"""
        if not pygame.mixer.get_init():
            print("音频系统尚未初始化")
            return False
        if not music_path:
            print("训练音乐路径为空")
            return False
        if not os.path.exists(music_path):
            print(f"训练音乐不存在: {music_path}")
            return False
        if (
            not restart
            and self.current_music_type == "training"
            and self.current_music_path == music_path
            and pygame.mixer.music.get_busy()
        ):
            return True
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            actual_volume = self.music_volume * TRAINING_MUSIC_VOLUME_SCALE
            pygame.mixer.music.set_volume(max(0.0, min(1.0, actual_volume)))
            pygame.mixer.music.play(loops=0)
            self.music_loaded = True
            self.current_music_path = music_path
            self.current_music_type = "training"
            print(f"训练音乐开始播放: {music_path}")
            return True
        except pygame.error as error:
            print(f"训练音乐播放失败: {error}")
            self.music_loaded = False
            return False

    def pause_music(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.pause()

    def unpause_music(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.unpause()

    def stop_music(self, fade_ms=0):
        """停止当前音乐；fade_ms 大于 0 时使用淡出。"""
        if not pygame.mixer.get_init():
            return
        try:
            if fade_ms > 0:
                pygame.mixer.music.fadeout(fade_ms)
            else:
                pygame.mixer.music.stop()
            self.music_loaded = False
            self.current_music_type = None
            self.current_music_path = None
        except pygame.error as error:
            print(f"停止音乐失败: {error}")

    def set_music_volume(self, value):
        """修改音乐音量，并根据当前音乐类型立即更新。"""
        self.music_volume = max(0.0, min(1.0, float(value)))
        if not pygame.mixer.get_init():
            return
        if self.current_music_type == "menu":
            actual_volume = self.music_volume * MENU_MUSIC_VOLUME_SCALE
        else:
            actual_volume = self.music_volume * TRAINING_MUSIC_VOLUME_SCALE
        pygame.mixer.music.set_volume(max(0.0, min(1.0, actual_volume)))

    def set_sound_volume(self, value):
        self.sound_volume = max(0.0, min(1.0, float(value)))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def load_sounds(self):
        sound_files = {
            NOTE_TYPE_HIT: SOUND_HIT,
            NOTE_TYPE_TAP: SOUND_TAP,
            NOTE_TYPE_HOLD: SOUND_HOLD,
        }
        for note_type, path in sound_files.items():
            if not os.path.exists(path):
                print("未找到音效:", path)
                continue
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sound_volume)
                self.sounds[note_type] = sound
                print("音效加载成功:", path)
            except pygame.error as error:
                print("音效加载失败:", path, error)

    def play_note_sound(self, note_type):
        sound = self.sounds.get(note_type)
        if sound:
            sound.play()
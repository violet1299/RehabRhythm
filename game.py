import pygame, sys, math, os, time, csv
from theme import *
from managers.analysis_manager import AnalysisManager
from managers.settings_manager import SettingsManager
from config import *
from camera_tracker import CameraTracker
from chart import RehabChart
from note import RehabNote
from scenes.menu_scene import MenuScene
from scenes.settings_scene import SettingsScene
from scenes.history_scene import HistoryScene
from scenes.result_scene import ResultScene
from scenes.analysis_scene import AnalysisScene
from scenes.calibration_scene import CalibrationScene
from scenes.training_scene import TrainingHUD
from scenes.about_scene import AboutScene
from scenes.countdown_scene import CountdownScene
from managers.transition_manager import TransitionManager
from scenes.pause_scene import PauseScene
from scenes.tutorial_scene import TutorialScene
from scenes.start_scene import StartScene
from scenes.gesture_guide_scene import GestureGuideScene

from particle import create_hit_particles
from ui import RehabUI
from managers.score_manager import ScoreManager
from managers.audio_manager import AudioManager
START="START"; GESTURE_GUIDE="GESTURE_GUIDE"; MENU="MENU"; CALIBRATION="CALIBRATION"; TUTORIAL = "TUTORIAL";COUNTDOWN="COUNTDOWN"; TRAINING="TRAINING"; PAUSE="PAUSE"; RESULT="RESULT"; HISTORY="HISTORY";SETTINGS = "SETTINGS";ANALYSIS = "ANALYSIS";ABOUT = "ABOUT"
class RehabRhythmGame:
    def __init__(self):
        pygame.init(); 
        pygame.mixer.init(); 
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.FULLSCREEN | pygame.SCALED
        )
        pygame.display.set_caption("RehabRhythm - V4 Smart Chart Edition"); self.clock=pygame.time.Clock(); self.scene=START; self.previous_scene=MENU; self.running=True;self.hand_cursor = None
        self.hand_click_ready = True
        self.hand_click_cooldown = 0
        self.ui=RehabUI(); self.tracker=CameraTracker(); self.score=ScoreManager();self.analysis_manager = AnalysisManager(); self.song_key=DEFAULT_SONG_KEY; self.song_info=SONGS[self.song_key]; self.difficulty_key=DEFAULT_DIFFICULTY; self.difficulty=DIFFICULTIES[self.difficulty_key]; self.apply_difficulty_values(); self.chart=RehabChart(self.song_info["chart"],self.difficulty_key)
        self.settings = SettingsManager()
        saved_settings = self.settings.load()

        self.audio = AudioManager()
        self.audio.set_music_volume(saved_settings["music_volume"])
        self.audio.set_sound_volume(saved_settings["sound_volume"])
        self.audio.load_sounds()

        self.start_scene = StartScene()
        self.gesture_guide_scene = GestureGuideScene()
        self.menu_scene = MenuScene()
        self.settings_scene = SettingsScene()
        self.history_scene = HistoryScene()
        self.result_scene = ResultScene()
        self.analysis_scene = AnalysisScene()
        self.calibration_scene = CalibrationScene()
        self.tutorial_scene = TutorialScene()

        self.training_hud = TrainingHUD()
        self.about_scene = AboutScene()
        self.countdown_scene = CountdownScene()
        self.transition = TransitionManager()
        self.pause_scene = PauseScene()

        # 启动游戏后，在开始页面循环播放菜单背景音乐
        self.audio.play_menu_music()

        self.menu_gesture_last_select_time = 0
        self.menu_gesture_cooldown = 1.0
        self.fullscreen = True

        self.menu_hover_start_time = 0
        self.menu_last_selected_index = -1

       
        self.notes=[]; self.particles=[]; self.judgement_texts=[]; self.combo_popup=None; self.combo_flash_alpha=0
        self.training_start_time=0; self.pause_start_time=0; self.total_pause_time=0; self.countdown_start_time=0; self.last_adapt_time=0; self.calibration_start_time=0; self.calibration_points=[]; self.result_saved=False;self.show_fps = DEFAULT_SHOW_FPS
        self.hand_range={"min_x":0,"max_x":WIDTH,"min_y":0,"max_y":HEIGHT,"center_x":WIDTH//2,"center_y":HEIGHT//2,"range_x":WIDTH,"range_y":HEIGHT}; self.tracker_started=False
    def start_camera_and_open_menu(self):
        if not self.tracker_started:
            self.tracker.start()
            self.tracker_started = True
        self.scene = MENU
        self.hand_cursor = None
        self.menu_hover_start_time = time.time()
        self.menu_last_selected_index = -1

    def advance_gesture_guide(self):
        if self.gesture_guide_scene.advance():
            self.start_camera_and_open_menu()

    def apply_difficulty_values(self):
        d=self.difficulty; self.current_bpm=d["bpm"]; self.hit_radius=d["hit_radius"]; self.tap_radius=d["tap_radius"]; self.hold_required_time=d["hold_time"]; self.note_appear_time=d["note_appear_time"]; self.perfect_window=d["perfect_window"]; self.good_window=d["good_window"]; self.miss_window=d["miss_window"]; self.line_move_multiplier=d["line_move_multiplier"]
    def reload_chart(self):
        """切换歌曲或难度时重新读取谱面，但保持菜单音乐继续播放。"""
        self.chart = RehabChart(
            self.song_info["chart"],
            self.difficulty_key
        )
    def set_difficulty(self,key):
        if key not in DIFFICULTIES: return
        self.difficulty_key=key; self.difficulty=DIFFICULTIES[key]; self.apply_difficulty_values(); self.reload_chart(); print("难度已切换:",self.difficulty["name"],"音符数:",len(self.chart.notes))
    def set_song(self,key):
        if key not in SONGS: return
        self.song_key=key; self.song_info=SONGS[key]; self.reload_chart(); print("歌曲已切换:",self.song_info["name"])
    def save_result(self):
        os.makedirs("data", exist_ok=True)
        file_exists = os.path.exists(RESULT_SAVE_PATH)

        analysis = self.analysis_manager.generate(self.score, self.current_bpm)

        with open(RESULT_SAVE_PATH, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "time", "patient_id", "difficulty", "song", "chart",
                    "score", "accuracy", "perfect", "good", "miss",
                    "max_combo", "final_bpm", "training_duration",
                    "reaction", "stability", "fatigue", "ai_advice",
                    "hand_range_x", "hand_range_y"
                ])

            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                PATIENT_ID,
                self.difficulty["name"],
                self.song_info["name"],
                self.chart.title,
                self.score.score,
                self.score.accuracy(),
                self.score.perfect,
                self.score.good,
                self.score.miss,
                self.score.max_combo,
                self.current_bpm,
                int(self.get_training_time()),
                analysis["reaction"],
                analysis["stability"],
                analysis["fatigue"],
                analysis["advice"],
                self.hand_range["range_x"],
                self.hand_range["range_y"]
            ])
    def load_history_records(self):
        if not os.path.exists(RESULT_SAVE_PATH): return []
        try:
            with open(RESULT_SAVE_PATH,"r",encoding="utf-8") as f: return list(csv.DictReader(f))
        except Exception: return []
    def generate_ai_advice(self,accuracy,miss,bpm,max_combo):
        if accuracy>=90 and miss<=2: return "Great stability. Continue with the current rhythm speed."
        if accuracy>=75: return "Good progress. Keep gentle and steady hand movement."
        if miss>=5: return "Many notes were missed. A slower rhythm is recommended."
        if bpm>=80 and accuracy<75: return "The rhythm may be too fast. Reduce speed to avoid fatigue."
        if max_combo<5: return "Try shorter sessions and focus on smooth continuous movement."
        return "Training completed. Continue regular practice comfortably."
    def start_calibration(self): self.scene=CALIBRATION; self.calibration_start_time=time.time(); self.calibration_points.clear(); self.result_saved=False
    def update_calibration(self):
        hands = self.tracker.get_hands()
        if hands:
            self.calibration_points.extend(hands)

        elapsed = time.time() - self.calibration_start_time
        

        if elapsed >= CALIBRATION_DURATION:
            print("CALL finish_calibration")
            self.finish_calibration()
    def finish_calibration(self):
        if len(self.calibration_points) < MIN_CALIBRATION_POINTS:
            hands = self.tracker.get_hands()
            if hands:
                self.calibration_points.extend(hands)

        if len(self.calibration_points) < 3:
            self.hand_range = {
                "min_x": WIDTH // 2 - 220,
                "max_x": WIDTH // 2 + 220,
                "min_y": HEIGHT // 2 - 180,
                "max_y": HEIGHT // 2 + 180,
                "center_x": WIDTH // 2,
                "center_y": HEIGHT // 2,
                "range_x": 440,
                "range_y": 360
            }
            self.start_countdown()
            return

        xs = [p[0] for p in self.calibration_points]
        ys = [p[1] for p in self.calibration_points]

        min_x = max(0, min(xs) - 60)
        max_x = min(WIDTH, max(xs) + 60)
        min_y = max(0, min(ys) - 60)
        max_y = min(HEIGHT, max(ys) + 60)

        rx = max_x - min_x
        ry = max_y - min_y

        if rx < MIN_HAND_RANGE_X or ry < MIN_HAND_RANGE_Y:
            min_x = max(0, WIDTH // 2 - 220)
            max_x = min(WIDTH, WIDTH // 2 + 220)
            min_y = max(0, HEIGHT // 2 - 180)
            max_y = min(HEIGHT, HEIGHT // 2 + 180)
            rx = max_x - min_x
            ry = max_y - min_y

        self.hand_range = {
            "min_x": min_x,
            "max_x": max_x,
            "min_y": min_y,
            "max_y": max_y,
            "center_x": (min_x + max_x) // 2,
            "center_y": (min_y + max_y) // 2,
            "range_x": rx,
            "range_y": ry
        }

        print("FINISH calibration, go countdown")
        self.start_countdown()
        print("scene now:", self.scene)
    def reset_training(self):
        self.score.reset(); self.chart.reset(); self.apply_difficulty_values(); self.notes.clear(); self.particles.clear(); self.judgement_texts.clear(); self.combo_popup=None; self.combo_flash_alpha=0; self.training_start_time=time.time(); self.pause_start_time=0; self.total_pause_time=0; self.last_adapt_time=0; self.result_saved=False
    def start_countdown(self):
        """进入倒计时，并让菜单音乐自然淡出。"""
        self.audio.fadeout_menu_music()
        self.scene = COUNTDOWN
        self.countdown_start_time = time.time()
        self.reset_training()
    def start_training(self):
        """倒计时结束后开始训练，并播放当前谱面的训练音乐。"""
        self.scene = TRAINING
        self.training_start_time = time.time()
        self.total_pause_time = 0
        print("进入训练阶段")
        self.audio.play_training_music(self.chart.music_path)
    def resume_training_from_pause(self):
        """从暂停页面继续训练。"""
        if self.scene != PAUSE:
            return

        self.total_pause_time += time.time() - self.pause_start_time
        self.pause_start_time = 0
        self.scene = TRAINING
        self.audio.unpause_music()


    def quit_training_to_menu(self):
        """结束当前训练并返回主菜单，不保存未完成结果。"""
        self.audio.stop_music()

        self.notes.clear()
        self.particles.clear()
        self.judgement_texts.clear()

        self.combo_popup = None
        self.combo_flash_alpha = 0
        self.pause_start_time = 0
        self.total_pause_time = 0
        self.result_saved = False

        self.scene = MENU
        self.audio.play_menu_music(restart=True)

    def finish_training(self):
        if not self.result_saved:
            self.save_result()
            self.result_saved = True

        self.audio.stop_music()
        self.scene = RESULT
        self.audio.play_menu_music(restart=True)
    def get_training_time(self): return self.pause_start_time-self.training_start_time-self.total_pause_time if self.scene==PAUSE else time.time()-self.training_start_time-self.total_pause_time
    
    def go_scene(self, scene):
        if self.scene != scene:
            self.transition.start(scene)
    
    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.scene == START and self.start_scene.clicked(event.pos):
                    self.gesture_guide_scene.reset()
                    self.scene = GESTURE_GUIDE
                elif self.scene == GESTURE_GUIDE and self.gesture_guide_scene.clicked(event.pos):
                    self.advance_gesture_guide()
                continue

            if event.type != pygame.KEYDOWN:
                continue

            # F11 切换全屏
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()
                continue

            # =========================
            # Pause 页面专用按键
            # =========================
            if self.scene == PAUSE:

                # SPACE：继续训练
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.resume_training_from_pause()
                    continue

                # ESC：放弃本次训练，返回主菜单
                if event.key == pygame.K_ESCAPE:
                    self.quit_training_to_menu()
                    continue

            # =========================
            # ESC 通用处理
            # =========================
            if event.key == pygame.K_ESCAPE:

                if self.scene == TRAINING:
                    self.scene = PAUSE
                    self.pause_start_time = time.time()
                    self.audio.pause_music()

                elif self.scene == HISTORY:
                    self.go_scene(self.previous_scene)

                elif self.scene == SETTINGS:
                    self.go_scene(MENU)

                elif self.scene == ANALYSIS:
                    self.go_scene(RESULT)

                elif self.scene == ABOUT:
                    self.go_scene(MENU)

                elif self.scene == TUTORIAL:
                    self.scene = MENU
                    self.audio.play_menu_music()

                elif self.scene == GESTURE_GUIDE:
                    self.scene = START
                    self.audio.play_menu_music()

                elif self.scene == START:
                    if self.fullscreen:
                        self.toggle_fullscreen()
                    else:
                        self.running = False

                elif self.scene in (CALIBRATION, COUNTDOWN, RESULT):
                    self.audio.stop_music()
                    self.scene = MENU
                    self.audio.play_menu_music(restart=True)

                else:
                    if self.fullscreen:
                        self.toggle_fullscreen()
                    else:
                        self.running = False

                continue

            # =========================
            # MENU
            # =========================
            if self.scene == MENU:
                if event.key == pygame.K_1:
                    self.set_difficulty("EASY")

                elif event.key == pygame.K_2:
                    self.set_difficulty("NORMAL")

                elif event.key == pygame.K_3:
                    self.set_difficulty("HARD")

                elif event.key == pygame.K_q:
                    self.set_song("Q")

                elif event.key == pygame.K_w:
                    self.set_song("W")

                elif event.key == pygame.K_e:
                    self.set_song("E")

                elif event.key == pygame.K_s:
                    self.go_scene(SETTINGS)

                elif event.key in (pygame.K_b, pygame.K_i):
                    self.go_scene(ABOUT)

            # =========================
            # SETTINGS
            # =========================
            if self.scene == SETTINGS:
                if event.key == pygame.K_UP:
                    self.audio.set_music_volume(
                        self.audio.music_volume + 0.05
                    )
                    self.save_settings()

                elif event.key == pygame.K_DOWN:
                    self.audio.set_music_volume(
                        self.audio.music_volume - 0.05
                    )
                    self.save_settings()

                elif event.key == pygame.K_RIGHT:
                    self.audio.set_sound_volume(
                        self.audio.sound_volume + 0.05
                    )
                    self.save_settings()

                elif event.key == pygame.K_LEFT:
                    self.audio.set_sound_volume(
                        self.audio.sound_volume - 0.05
                    )
                    self.save_settings()

                elif event.key == pygame.K_f:
                    self.show_fps = not self.show_fps
                    self.save_settings()

                elif event.key == pygame.K_r:
                    self.audio.set_music_volume(DEFAULT_MUSIC_VOLUME)
                    self.audio.set_sound_volume(DEFAULT_SOUND_VOLUME)
                    self.show_fps = DEFAULT_SHOW_FPS
                    self.save_settings()

            # =========================
            # SPACE
            # =========================
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):

                if self.scene == START:
                    self.gesture_guide_scene.reset()
                    self.scene = GESTURE_GUIDE

                elif self.scene == GESTURE_GUIDE:
                    self.advance_gesture_guide()

                elif self.scene == MENU:
                    self.tutorial_scene.reset()
                    self.scene = TUTORIAL

                elif self.scene == RESULT:
                    self.tutorial_scene.reset()
                    self.scene = TUTORIAL

            # History
            if event.key == pygame.K_h and self.scene in [MENU, RESULT]:
                self.previous_scene = self.scene
                self.go_scene(HISTORY)

            # Result -> Analysis
            if self.scene == RESULT and event.key == pygame.K_a:
                self.go_scene(ANALYSIS)

            # Tutorial
            elif self.scene == TUTORIAL:
                status = self.tutorial_scene.update(self.tracker)
                action = self.tutorial_scene.handle_event(event, status)

                if action == "menu":
                    self.scene = MENU
                    self.audio.play_menu_music()

                elif action == "calibration":
                    self.start_calibration()
    def expand_note_position(self, x, y):
        """
        扩大音符在全屏训练界面中的活动范围。
        只扩大横向范围，避免音符超出上下边界。
        """
        scale_x = 1.28

        new_x = WIDTH // 2 + (x - WIDTH // 2) * scale_x

        new_x = max(
            45,
            min(WIDTH - 45, new_x)
        )

        return int(new_x), int(y)
    def _map_hand_to_screen(self, hx, hy):
        """
        CameraTracker in this project usually returns screen coordinates.
        If it ever returns normalized coordinates (0~1), this function also supports that.
        """
        if 0 <= hx <= 1.5 and 0 <= hy <= 1.5:
            return int(hx * WIDTH), int(hy * HEIGHT)
        return int(hx), int(hy)

    def _get_menu_index_from_cursor(self, cursor_x, cursor_y):
        """
        Prefer real button rects from menu_scene.
        If rects are not available yet, fall back to a 2x3 grid.
        """
        if hasattr(self.menu_scene, "rects"):
            for i, rect in enumerate(self.menu_scene.rects):
                if rect.collidepoint(cursor_x, cursor_y):
                    return i

        if cursor_y < HEIGHT * 0.58:
            if cursor_x < WIDTH / 3:
                return 0
            elif cursor_x < WIDTH * 2 / 3:
                return 1
            else:
                return 2
        else:
            if cursor_x < WIDTH / 3:
                return 3
            elif cursor_x < WIDTH * 2 / 3:
                return 4
            else:
                return 5

    def _execute_menu_action(self, index):
        if index == 0:
            self.tutorial_scene.reset()
            self.scene = TUTORIAL
        elif index == 1:
            self.previous_scene = MENU
            self.go_scene(HISTORY)
        elif index == 2:
            self.go_scene(SETTINGS)
        elif index == 3:
            keys = list(SONGS.keys())
            current = keys.index(self.song_key)
            self.set_song(keys[(current + 1) % len(keys)])
        elif index == 4:
            keys = list(DIFFICULTIES.keys())
            current = keys.index(self.difficulty_key)
            self.set_difficulty(keys[(current + 1) % len(keys)])
        elif index == 5:
            self.go_scene(ABOUT)

    def _is_open_palm(self, fingertips):
        return len(fingertips) >= 3
    

    def update_menu_controller(self):
        """
        V5 menu gesture controller:
        hand position controls cursor,
        hover selects menu card,
        open palm confirms selection.
        """
        if self.scene != MENU:
            self.hand_cursor = None
            return

        if not self.tracker_started:
            self.hand_cursor = None
            return

        hands = self.tracker.get_hands()
        fingertips = self.tracker.get_fingertips()

        if not hands:
            self.hand_cursor = None
            return

        hx, hy = hands[0]
        cursor_x, cursor_y = self._map_hand_to_screen(hx, hy)
        cursor_x = max(0, min(WIDTH - 1, cursor_x))
        cursor_y = max(0, min(HEIGHT - 1, cursor_y))

        self.hand_cursor = (cursor_x, cursor_y)

        # A closed fist is used to move and point at a menu card.
        # An open palm confirms the currently highlighted card.
        fist_active = self.tracker.is_fist()
        palm_active = self.tracker.is_open_palm()

        if fist_active:
            selected = self._get_menu_index_from_cursor(cursor_x, cursor_y)
            self.menu_scene.selected_index = selected
        else:
            selected = getattr(self.menu_scene, "selected_index", 0)

        now = time.time()
        if now < self.hand_click_cooldown:
            return

        if selected != self.menu_last_selected_index:
            self.menu_last_selected_index = selected
            self.menu_hover_start_time = now

        # 手停在同一个按钮 1 秒后确认
        # 停留超过0.5秒后，只有张开手才确认
        if now - self.menu_hover_start_time >= 0.5:
            if palm_active:
                self.hand_click_cooldown = now + 1.2
                self.menu_hover_start_time = now + 999
                self._execute_menu_action(selected)
    def update_countdown(self):
        if time.time()-self.countdown_start_time>=COUNTDOWN_SECONDS: self.start_training()
    def update_training(self):
        elapsed=self.get_training_time()
        if elapsed>=self.chart.duration: self.finish_training(); return
        for nd in self.chart.get_due_notes(elapsed,self.note_appear_time): self.notes.append(RehabNote(nd)); self.score.register_note()
        cy,angle=self.get_line_state(elapsed); palms=self.tracker.get_hands(); tips=self.tracker.get_fingertips()
        for note in self.notes[:]:
            note.update(elapsed,self.note_appear_time); nx,ny=note.get_position(cy,angle)
            if note.is_too_late(elapsed,self.miss_window,self.hold_required_time): self.notes.remove(note); self.score.hit_miss(); self.add_judgement_text("MISS",nx,ny); continue
            judge=note.judge_time(elapsed,self.perfect_window,self.good_window)
            if note.note_type==NOTE_TYPE_HIT:
                if judge is None: continue
                for hx,hy in palms:
                    if math.hypot(nx-hx,ny-hy)<=self.hit_radius: self.handle_note_hit(note,nx,ny,judge); break
            elif note.note_type==NOTE_TYPE_TAP:
                if judge is None: continue
                for tx,ty in tips:
                    if math.hypot(nx-tx,ny-ty)<=self.tap_radius: self.handle_note_hit(note,nx,ny,judge); break
            elif note.note_type==NOTE_TYPE_HOLD:
                rect=pygame.Rect(nx-self.hit_radius//2,ny-(HOLD_BODY_LENGTH+70)//2,self.hit_radius,HOLD_BODY_LENGTH+70); holding=False
                for hx,hy in palms:
                    if rect.collidepoint(hx,hy):
                        holding=True
                        if note.hold_start_time is None: note.hold_start_time=elapsed; self.audio.play_note_sound(NOTE_TYPE_HOLD)
                        note.hold_progress=min(1.0,note.hold_progress+(1/FPS)/self.hold_required_time)
                        if note.hold_progress>=1.0: self.handle_note_hit(note,nx,ny,"PERFECT")
                        break
                if not holding: note.hold_start_time=None
        for p in self.particles[:]:
            if not p.update(): self.particles.remove(p)
        self.apply_adaptive_difficulty()
    def handle_note_hit(self,note,x,y,judgement):
        self.score.hit_perfect() if judgement=="PERFECT" else self.score.hit_good(); self.audio.play_note_sound(note.note_type); self.particles.extend(create_hit_particles(x,y,judgement)); self.add_judgement_text(judgement,x,y)
        if self.score.combo in [10,20,30,50] or (self.score.combo>0 and self.score.combo%100==0): self.combo_popup={"combo":self.score.combo,"start":time.time(),"life":0.9}; self.combo_flash_alpha=90
        if note in self.notes: self.notes.remove(note)
    def add_judgement_text(self,text,x,y): self.judgement_texts.append({"text":text,"x":x,"y":y-55,"life":0.6,"start":time.time()})
    def save_settings(self):
        self.settings.save(
            self.audio.music_volume,
            self.audio.sound_volume,
            self.show_fps
        )
    def apply_adaptive_difficulty(self):
        elapsed=self.get_training_time()
        if elapsed-self.last_adapt_time<8.0: return
        self.last_adapt_time=elapsed; acc=self.score.accuracy()
        if acc>=88 and self.score.combo>=12: self.current_bpm=min(95,self.current_bpm+2)
        elif acc<70 or self.score.health<50: self.current_bpm=max(55,self.current_bpm-2)
    def get_line_state(self, elapsed):
        # 判定线的基础位置固定在屏幕中间
        base_y = int(HEIGHT * 0.58)

        # 上下轻微移动
        move = int(
            LINE_MOVE_AMPLITUDE
            * self.line_move_multiplier
            * math.sin(
                elapsed
                * LINE_MOVE_SPEED
                * self.line_move_multiplier
            )
        )

        cy = base_y + move

        # 旋转角度
        angle = (
            LINE_ROTATE_AMPLITUDE
            * self.line_move_multiplier
            * math.sin(
                elapsed
                * LINE_ROTATE_SPEED
                * self.line_move_multiplier
            )
        )

        # 防止线跑出画面
        cy = max(
            170,
            min(HEIGHT - 170, cy)
        )

        return cy, angle
    def draw_calibration(self):
        progress = 0.0

        if hasattr(self, "calibration_start_time"):
            progress = min(1.0, (time.time() - self.calibration_start_time) / CALIBRATION_TIME)

        hands = self.tracker.get_hands()
        hand_detected = len(hands) > 0

        self.calibration_scene.draw(
            self.screen,
            progress,
            hand_detected
        )
    
    def draw_judgement_texts(self):
        font=pygame.font.Font(None,42); now=time.time()
        for item in self.judgement_texts[:]:
            el=now-item["start"]
            if el>item["life"]: self.judgement_texts.remove(item); continue
            alpha=int(255*(1-el/item["life"])); y=item["y"]-int(el*30); color=GREEN if item["text"]=="PERFECT" else YELLOW if item["text"]=="GOOD" else RED; surf=font.render(item["text"],True,color); surf.set_alpha(alpha); self.screen.blit(surf,surf.get_rect(center=(item["x"],y)))
    def draw_combo_effect(self):
        if self.combo_flash_alpha>0: flash=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); flash.fill((80,220,255,int(self.combo_flash_alpha))); self.screen.blit(flash,(0,0)); self.combo_flash_alpha=max(0,self.combo_flash_alpha-5)
        if self.combo_popup is None: return
        el=time.time()-self.combo_popup["start"]
        if el>self.combo_popup["life"]: self.combo_popup=None; return
        alpha=int(255*(1-el/self.combo_popup["life"])); scale=1+0.25*(1-el/self.combo_popup["life"]); font=pygame.font.Font(None,int(72*scale)); text=font.render(f"{self.combo_popup['combo']} COMBO!",True,GREEN); text.set_alpha(alpha); self.screen.blit(text,text.get_rect(center=(WIDTH//2,HEIGHT//2-120)))
    def draw_training(self):
        elapsed=self.get_training_time(); cy,angle=self.get_line_state(elapsed); self.ui.draw_background(self.screen); self.ui.draw_judgement_line(self.screen,cy,angle); area=pygame.Rect(self.hand_range["min_x"],self.hand_range["min_y"],self.hand_range["range_x"],self.hand_range["range_y"]); pygame.draw.rect(self.screen,PANEL,area,2,border_radius=16)
        for note in self.notes:
            nx, ny = note.get_position(cy, angle)
            nx, ny = self.expand_note_position(nx, ny)

            self.ui.draw_note(
                self.screen,
                note,
                nx,
                ny
            )
        for p in self.particles: p.draw(self.screen)
        self.draw_judgement_texts(); self.draw_combo_effect(); self.ui.draw_hands(self.screen,self.tracker.get_hands(),self.tracker.get_fingertips()); 
        self.training_hud.draw(
        self.screen,
        self.score,
        elapsed,
        self.current_bpm,
        self.show_fps,
        self.clock
    )
        
        REST_HINT_DURATION = 4.0

        if (
            REST_REMINDER_TIME
            <= elapsed
            < REST_REMINDER_TIME + REST_HINT_DURATION
        ):
            self.ui.draw_rest_hint(self.screen)
    def draw_pause(self):
        self.draw_training()

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect(210, 175, 380, 250)
        self.ui.w.draw_card(self.screen, panel, NEON_PURPLE, CARD_BG_DARK, 24)

        title_font = pygame.font.Font(None, 76)
        mid_font = pygame.font.Font(None, 34)
        small_font = pygame.font.Font(None, 24)

        title = title_font.render("PAUSED", True, TEXT_MAIN)
        subtitle = small_font.render("Training session is temporarily paused", True, TEXT_SUB)

        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.y + 60)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, panel.y + 110)))

        resume = mid_font.render("ESC  Resume", True, NEON_GREEN)
        quit_tip = small_font.render("Close window or press ESC outside training to quit", True, TEXT_MUTED)

        self.screen.blit(resume, resume.get_rect(center=(WIDTH // 2, panel.y + 165)))
        self.screen.blit(quit_tip, quit_tip.get_rect(center=(WIDTH // 2, panel.y + 215)))
    def draw_ai_advice_box(self):
        title_font=pygame.font.Font(None,26); small=pygame.font.Font(None,23); advice=self.generate_ai_advice(self.score.accuracy(),self.score.miss,self.current_bpm,self.score.max_combo); box=pygame.Rect(90,485,620,70); pygame.draw.rect(self.screen,PANEL,box,border_radius=18); pygame.draw.rect(self.screen,BLUE,box,2,border_radius=18); self.screen.blit(title_font.render("AI Recommendation",True,BLUE),(box.x+24,box.y+12)); self.screen.blit(small.render(advice,True,WHITE),(box.x+24,box.y+40))
    
    def draw(self):
        if self.scene == START:
            self.start_scene.draw(self.screen)
        elif self.scene == GESTURE_GUIDE:
            self.gesture_guide_scene.draw(self.screen)
        elif self.scene == MENU:
            self.menu_scene.draw(
                self.screen,
                self.difficulty["name"],
                self.song_info["name"]
            )
        elif self.scene == TUTORIAL:
            status = self.tutorial_scene.update(self.tracker)
            self.tutorial_scene.draw(self.screen, status)
        elif self.scene==CALIBRATION: self.draw_calibration()
        elif self.scene == COUNTDOWN:

         remain = max(
             0,
             3 - int(time.time() - self.countdown_start_time)
         )

         self.countdown_scene.draw(
             self.screen,
                remain
            )
        elif self.scene==TRAINING: self.draw_training()
        elif self.scene == PAUSE:
            self.pause_scene.draw(self.screen)
        elif self.scene == RESULT:
            self.result_scene.draw(self.screen, self.score)
        elif self.scene == HISTORY:
            self.history_scene.draw(self.screen)
        elif self.scene == ANALYSIS:
            analysis = self.analysis_manager.generate(self.score, self.current_bpm)
            self.analysis_scene.draw(self.screen, analysis)
        elif self.scene == SETTINGS:
            self.settings_scene.draw(
                self.screen,
                self.audio.music_volume,
                self.audio.sound_volume,
                self.show_fps
            )
        elif self.scene == ABOUT:
                self.about_scene.draw(self.screen)

        # ==========================
        # V5 Hand Cursor
        # ==========================
        if self.scene == MENU and self.hand_cursor is not None:
            x, y = self.hand_cursor

            glow = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.circle(glow, (80, 220, 255, 55), (35, 35), 32)
            self.screen.blit(glow, (x - 35, y - 35))

            pygame.draw.circle(self.screen, (80, 220, 255), (x, y), 18)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 18, 3)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 5)

    def run(self):
        while self.running:
            # 获取上一帧到这一帧经过的时间，单位为秒
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_events()
            self.update_menu_controller()

            # 开始界面的按钮悬停动画
            if self.scene == START:
                self.start_scene.update(dt)

            if self.scene == CALIBRATION:
                self.update_calibration()

            elif self.scene == COUNTDOWN:
                self.update_countdown()

            elif self.scene == TRAINING:
                self.update_training()

            self.draw()

            self.transition.update(self)
            self.transition.draw(
                self.screen,
                WIDTH,
                HEIGHT
            )

            pygame.display.flip()

        self.close()
    def close(self): self.audio.stop_music(); self.tracker.stop() if self.tracker_started else None; pygame.quit(); sys.exit()
if __name__=="__main__": RehabRhythmGame().run()
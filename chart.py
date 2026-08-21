import json, os
from config import *

class RehabChart:
    def __init__(self, chart_path=None, difficulty_key=DEFAULT_DIFFICULTY):
        self.chart_path = chart_path or SONGS[DEFAULT_SONG_KEY]["chart"]
        self.difficulty_key = difficulty_key
        self.title = "Untitled"
        self.music_path = "assets/bgm.wav"
        self.bpm = 70
        self.duration = TRAINING_DURATION
        self.base_notes = []
        self.notes = []
        self.remaining = []
        self.load()

    def load(self):
        if not os.path.exists(self.chart_path):
            print("未找到谱面，使用默认谱面:", self.chart_path)
            self.create_default_chart(); return
        try:
            with open(self.chart_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.title = data.get("title", "Untitled")
            self.music_path = data.get("music", "assets/bgm.wav")
            self.bpm = int(data.get("bpm", 70))
            self.duration = int(data.get("duration", TRAINING_DURATION))
            self.base_notes = []
            for item in data.get("notes", []):
                if isinstance(item, dict):
                    t = float(item.get("time", 0)); typ = item.get("type", NOTE_TYPE_HIT)
                else:
                    t = float(item); typ = NOTE_TYPE_HIT
                if typ not in [NOTE_TYPE_HIT, NOTE_TYPE_TAP, NOTE_TYPE_HOLD]: typ = NOTE_TYPE_HIT
                self.base_notes.append({"time": t, "type": typ})
            self.base_notes.sort(key=lambda n:n["time"])
            self.generate_for_difficulty(self.difficulty_key)
            print("谱面加载成功:", self.title, self.difficulty_key, "音符数:", len(self.notes))
        except Exception as e:
            print("谱面加载失败，使用默认谱面:", e)
            self.create_default_chart()

    def create_default_chart(self):
        self.title = "Default Rehab Chart"; self.music_path = "assets/bgm.wav"; self.bpm = 70; self.duration = TRAINING_DURATION
        self.base_notes=[]; types=[NOTE_TYPE_HIT,NOTE_TYPE_TAP,NOTE_TYPE_HOLD]
        t=3.0; i=0
        while t < self.duration:
            self.base_notes.append({"time":round(t,2),"type":types[i%3]}); t += 1.3; i += 1
        self.generate_for_difficulty(self.difficulty_key)

    def generate_for_difficulty(self, difficulty_key):
        if difficulty_key == "EASY":
            out=[]; last=-99
            for i,n in enumerate(self.base_notes):
                if i % 2 == 0 and n["time"] - last >= 1.8:
                    out.append(dict(n)); last = n["time"]
            self.notes = out
        elif difficulty_key == "HARD":
            out=[]
            for i,n in enumerate(self.base_notes):
                out.append(dict(n))
                if i < len(self.base_notes)-1:
                    nt=self.base_notes[i+1]["time"]; gap=nt-n["time"]
                    if gap >= 1.1: out.append({"time":round(n["time"]+gap*0.5,2),"type":NOTE_TYPE_TAP})
                    if gap >= 1.6: out.append({"time":round(n["time"]+gap*0.75,2),"type":NOTE_TYPE_HIT})
            self.notes=sorted(out,key=lambda n:n["time"])
        else:
            self.notes=[dict(n) for n in self.base_notes]
        self.remaining = self.notes.copy()

    def reset(self): self.remaining = self.notes.copy()

    def get_due_notes(self, current_time, appear_time):
        due=[]
        for note in self.remaining[:]:
            if current_time >= note["time"] - appear_time:
                due.append(note); self.remaining.remove(note)
        return due

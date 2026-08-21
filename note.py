import random, math
from config import *
class RehabNote:
    def __init__(self, note_data):
        self.target_time=float(note_data["time"]); self.note_type=note_data.get("type",NOTE_TYPE_HIT)
        self.side=random.choice([-1,1]); self.offset_x=random.randint(-150,150); self.distance=NOTE_DISTANCE
        self.hold_start_time=None; self.hold_progress=0.0
    def update(self,current_time,appear_time):
        self.distance=((self.target_time-current_time)/appear_time)*NOTE_DISTANCE
    def get_position(self,center_y,angle):
        rad=math.radians(angle); base_x=WIDTH//2+self.offset_x*math.cos(rad); base_y=center_y+self.offset_x*math.sin(rad)
        normal_x=-math.sin(rad); normal_y=math.cos(rad)
        return int(base_x+normal_x*self.distance*self.side), int(base_y+normal_y*self.distance*self.side)
    def is_too_late(self,current_time,miss_window,hold_time):
        return current_time > self.target_time + miss_window + (hold_time if self.note_type==NOTE_TYPE_HOLD else 0)
    def judge_time(self,current_time,perfect_window,good_window):
        diff=abs(current_time-self.target_time)
        if diff <= perfect_window: return "PERFECT"
        if diff <= good_window: return "GOOD"
        return None

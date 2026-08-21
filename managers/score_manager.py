class ScoreManager:
    def __init__(self): self.reset()
    def reset(self):
        self.score=0; self.combo=0; self.max_combo=0; self.perfect=0; self.good=0; self.miss=0; self.total_notes=0; self.hit_notes=0; self.health=100
    def register_note(self): self.total_notes += 1
    def hit_perfect(self):
        self.perfect+=1; self.hit_notes+=1; self.combo+=1; self.max_combo=max(self.max_combo,self.combo); self.score += 120+self.combo*2; self.health=min(100,self.health+2)
    def hit_good(self):
        self.good+=1; self.hit_notes+=1; self.combo+=1; self.max_combo=max(self.max_combo,self.combo); self.score += 80+self.combo; self.health=min(100,self.health+1)
    def hit_miss(self): self.miss += 1; self.combo=0; self.health=max(0,self.health-6)
    def accuracy(self): return 0.0 if self.total_notes==0 else round((self.hit_notes/self.total_notes)*100,1)
    def get_result_level(self):
        acc=self.accuracy()
        return "Excellent" if acc>=90 else "Good" if acc>=75 else "Completed" if acc>=60 else "Keep Practicing"

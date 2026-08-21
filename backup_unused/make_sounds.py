import wave, math, os, struct
SAMPLE_RATE=44100
def write_wav(path,samples):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with wave.open(path,"w") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SAMPLE_RATE)
        for s in samples: f.writeframes(struct.pack("<h",int(max(-1,min(1,s))*32767)))
def sine(freq,t): return math.sin(2*math.pi*freq*t)
def make_tap(): write_wav("assets/sounds/tap.wav",[(sine(1800,i/SAMPLE_RATE)*0.7+sine(2600,i/SAMPLE_RATE)*0.3)*math.exp(-55*i/SAMPLE_RATE) for i in range(int(SAMPLE_RATE*0.08))])
def make_hit(): write_wav("assets/sounds/hit.wav",[(sine(220,i/SAMPLE_RATE)*0.5+sine(520,i/SAMPLE_RATE)*0.4+sine(1200,i/SAMPLE_RATE)*0.2)*math.exp(-35*i/SAMPLE_RATE) for i in range(int(SAMPLE_RATE*0.12))])
def make_hold(): write_wav("assets/sounds/hold.wav",[(sine(660,i/SAMPLE_RATE)*0.35+sine(990,i/SAMPLE_RATE)*0.25+sine(1320,i/SAMPLE_RATE)*0.15)*math.exp(-18*i/SAMPLE_RATE) for i in range(int(SAMPLE_RATE*0.18))])
if __name__=="__main__": make_tap(); make_hit(); make_hold(); print("音效生成完成：assets/sounds/")

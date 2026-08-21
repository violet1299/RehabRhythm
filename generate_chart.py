import librosa
import json
import random

def create_audio_chart(audio_path, output_json_path):
    print("正在分析音乐节奏，请稍候...")
    # 1. 加载音频文件
    y, sr = librosa.load(audio_path)
    
    # 2. 自动检测起始点（Onset）和 节拍（Beat）
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    print(f"检测到歌曲 BPM (每分钟节拍数): {int(tempo)}")
    
    chart_data = []
    last_time = 0
    # 针对老年人康复：限制节奏密度（比如两次击打之间至少间隔 1.0 秒）
    min_interval = 1.0 
    
    for t in beat_times:
        if t - last_time >= min_interval:
            # 随机生成音符在屏幕上的位置 (基于 640x480 的标准分辨率)
            # 留出边缘距离，防止老人够不到
            x = random.randint(100, 540)
            y = random.randint(100, 380)
            
            chart_data.append({
                "time": round(float(t), 2),
                "x": x,
                "y": y,
                "hit": False # 标记该音符是否已被击打
            })
            last_time = t
            
    # 3. 保存为配置文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(chart_data, f, indent=4, ensure_ascii=False)
    print(f"谱面生成成功！共生成 {len(chart_data)} 个康复击打点，已保存至 {output_json_path}")

# 使用示例：把你的音乐命名为 my_song.mp3 放在同目录下
if __name__ == "__main__":
    # 请确保你当前目录下有一个名为 'my_song.mp3' 的文件
    create_audio_chart("F:\桌面\毕设\HOYO.wav", "chart.json")
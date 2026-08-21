import cv2
import mediapipe as mp
import threading
import time
import math

from config import *


class CameraTracker:
    def __init__(self):
        self.running = False
        self.thread = None
        self.camera_ready = False
        self.tracking_ready = False
        self.cap = None

        self.tracks = {0: None, 1: None}
        self.last_seen = {0: 0, 1: 0}

        self.smooth_factor = 0.45
        self.hand_hold_time = 0.45
        self.merge_distance = 70
        self.gesture_margin = 4

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            model_complexity=1,
            max_num_hands=2,
            min_detection_confidence=0.35,
            min_tracking_confidence=0.35
        )

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        if self.cap:
            self.cap.release()
            self.cap = None
        self.hands.close()

    def _open_camera(self):
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.camera_ready = self.cap.isOpened()

    def _loop(self):
        self._open_camera()

        while self.running:
            if self.cap is None or not self.cap.isOpened():
                self.camera_ready = False
                time.sleep(0.3)
                self._open_camera()
                continue

            ok, frame = self.cap.read()
            if not ok:
                self.camera_ready = False
                time.sleep(0.03)
                continue

            self.camera_ready = True
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            try:
                result = self.hands.process(rgb)
            except Exception:
                time.sleep(0.01)
                continue

            detected = []

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    landmark_list = hand_landmarks.landmark
                    palm_landmark = landmark_list[9]

                    palm = (
                        int(palm_landmark.x * WIDTH),
                        int(palm_landmark.y * HEIGHT)
                    )

                    tips = []
                    for index in [4, 8, 12, 16, 20]:
                        point = landmark_list[index]
                        tips.append((
                            int(point.x * WIDTH),
                            int(point.y * HEIGHT)
                        ))

                    landmarks = []
                    for point in landmark_list:
                        landmarks.append((
                            int(point.x * WIDTH),
                            int(point.y * HEIGHT)
                        ))

                    detected.append({
                        "palm": palm,
                        "tips": tips,
                        "landmarks": landmarks
                    })

            self._update_tracks(detected)
            self.tracking_ready = any(
                track is not None for track in self.tracks.values()
            )
            time.sleep(0.005)

    def _update_tracks(self, detected):
        now = time.time()

        if not detected:
            for track_id in self.tracks:
                if now - self.last_seen[track_id] > self.hand_hold_time:
                    self.tracks[track_id] = None
            return

        if len(detected) == 1:
            data = detected[0]
            track_id = self._nearest_track(data["palm"])
            if track_id is None:
                track_id = 0 if self.tracks[0] is None else 1
            self.tracks[track_id] = self._smooth_data(
                self.tracks[track_id], data
            )
            self.last_seen[track_id] = now
            return

        hand_1 = detected[0]
        hand_2 = detected[1]

        if self._distance(hand_1["palm"], hand_2["palm"]) < self.merge_distance:
            merged = {
                "palm": (
                    (hand_1["palm"][0] + hand_2["palm"][0]) // 2,
                    (hand_1["palm"][1] + hand_2["palm"][1]) // 2
                ),
                "tips": hand_1["tips"],
                "landmarks": hand_1["landmarks"]
            }

            track_id = self._nearest_track(merged["palm"])
            if track_id is None:
                track_id = 0

            self.tracks[track_id] = self._smooth_data(
                self.tracks[track_id], merged
            )
            self.last_seen[track_id] = now
            return

        old_0 = self.tracks[0]
        old_1 = self.tracks[1]

        if old_0 is None and old_1 is None:
            detected.sort(key=lambda hand: hand["palm"][0])
            self.tracks[0] = detected[0]
            self.tracks[1] = detected[1]
            self.last_seen[0] = now
            self.last_seen[1] = now
            return

        normal_cost = self._cost(old_0, hand_1) + self._cost(old_1, hand_2)
        swapped_cost = self._cost(old_0, hand_2) + self._cost(old_1, hand_1)

        assignments = (
            {0: hand_1, 1: hand_2}
            if normal_cost <= swapped_cost
            else {0: hand_2, 1: hand_1}
        )

        for track_id, data in assignments.items():
            self.tracks[track_id] = self._smooth_data(
                self.tracks[track_id], data
            )
            self.last_seen[track_id] = now

    def _nearest_track(self, point):
        best_track_id = None
        best_distance = 999999

        for track_id, data in self.tracks.items():
            if data is None:
                continue
            distance = self._distance(point, data["palm"])
            if distance < best_distance:
                best_track_id = track_id
                best_distance = distance

        return best_track_id

    def _smooth_data(self, old, new):
        if old is None:
            return new

        return {
            "palm": self._smooth_point(old["palm"], new["palm"]),
            "tips": [
                self._smooth_point(old["tips"][i], new["tips"][i])
                for i in range(len(new["tips"]))
            ],
            "landmarks": [
                self._smooth_point(old["landmarks"][i], new["landmarks"][i])
                for i in range(len(new["landmarks"]))
            ]
        }

    def _smooth_point(self, old, new):
        return (
            int(old[0] * self.smooth_factor + new[0] * (1 - self.smooth_factor)),
            int(old[1] * self.smooth_factor + new[1] * (1 - self.smooth_factor))
        )

    def _distance(self, a, b):
        if a is None or b is None:
            return 999999
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def _cost(self, old, new):
        return 300 if old is None else self._distance(old["palm"], new["palm"])

    def get_hands(self):
        return [
            self.tracks[i]["palm"]
            for i in [0, 1]
            if self.tracks[i] is not None
        ]

    def get_fingertips(self):
        tips = []
        for i in [0, 1]:
            hand = self.tracks[i]
            if hand is not None:
                tips.extend(hand["tips"])
        return tips

    def _get_finger_states(self, hand):
        if hand is None:
            return None

        lm = hand.get("landmarks")
        if lm is None or len(lm) < 21:
            return None

        margin = self.gesture_margin

        index_open = (
            lm[8][1] < lm[6][1] - margin
            and lm[6][1] < lm[5][1] + margin
        )
        middle_open = (
            lm[12][1] < lm[10][1] - margin
            and lm[10][1] < lm[9][1] + margin
        )
        ring_open = (
            lm[16][1] < lm[14][1] - margin
            and lm[14][1] < lm[13][1] + margin
        )
        pinky_open = (
            lm[20][1] < lm[18][1] - margin
            and lm[18][1] < lm[17][1] + margin
        )

        return {
            "index": index_open,
            "middle": middle_open,
            "ring": ring_open,
            "pinky": pinky_open
        }

    def _is_open_palm_hand(self, hand):
        states = self._get_finger_states(hand)
        if states is None:
            return False
        return sum(1 for opened in states.values() if opened) >= 3

    def _is_fist_hand(self, hand):
        states = self._get_finger_states(hand)
        if states is None:
            return False
        return sum(1 for opened in states.values() if not opened) >= 3

    def _is_pointing_hand(self, hand):
        states = self._get_finger_states(hand)
        if states is None:
            return False
        return (
            states["index"]
            and not states["middle"]
            and not states["ring"]
            and not states["pinky"]
        )

    def is_open_palm(self):
        return any(
            self._is_open_palm_hand(self.tracks[i])
            for i in [0, 1]
        )

    def is_fist(self):
        return any(
            self._is_fist_hand(self.tracks[i])
            for i in [0, 1]
        )

    def is_pointing(self):
        return any(
            self._is_pointing_hand(self.tracks[i])
            for i in [0, 1]
        )

    def get_fist_hands(self):
        positions = []
        for i in [0, 1]:
            hand = self.tracks[i]
            if self._is_fist_hand(hand):
                positions.append(hand["palm"])
        return positions

    def get_open_palm_hands(self):
        positions = []
        for i in [0, 1]:
            hand = self.tracks[i]
            if self._is_open_palm_hand(hand):
                positions.append(hand["palm"])
        return positions

    def get_pointing_tips(self):
        positions = []
        for i in [0, 1]:
            hand = self.tracks[i]
            if self._is_pointing_hand(hand):
                positions.append(hand["landmarks"][8])
        return positions

    def get_gesture_names(self):
        gestures = []

        for i in [0, 1]:
            hand = self.tracks[i]
            if hand is None:
                continue

            if self._is_pointing_hand(hand):
                gesture = "POINT"
            elif self._is_open_palm_hand(hand):
                gesture = "PALM"
            elif self._is_fist_hand(hand):
                gesture = "FIST"
            else:
                gesture = "UNKNOWN"

            gestures.append({
                "track_id": i,
                "gesture": gesture,
                "position": hand["palm"]
            })

        return gestures
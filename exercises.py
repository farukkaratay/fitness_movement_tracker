import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class BaseExercise:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.connections = []
        self.detection_threshold = 160
        self.joint_visibility = []
        
    def init_counter(self):
        self.counter = 0
        self.stage = None
        
    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle
    
    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            landmarks = results.pose_landmarks.landmark
            angle, position = self.get_joint_angle(landmarks)
            
            # Sayma mantığı
            if angle > self.detection_threshold:
                self.stage = "up"
            if angle < self.detection_threshold - 30 and self.stage == "up":
                self.stage = "down"
                self.counter += 1
                
            # Açıyı ve konumu göster
            cv2.putText(image, f"Angle: {angle:.1f}", position, 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            
        except:
            pass
        
        # Sadece ilgili eklemleri çiz
        if results.pose_landmarks:
            # Tüm landmark'ları gizle
            for landmark in mp_pose.PoseLandmark:
                results.pose_landmarks.landmark[landmark.value].visibility = 0
            
            # Sadece seçilen eklemleri göster
            for joint in self.joint_visibility:
                results.pose_landmarks.landmark[joint.value].visibility = 1
            
            # Seçilen bağlantıları çiz
            for connection in self.connections:
                start_idx = connection[0].value
                end_idx = connection[1].value
                
                # Sadece görünür olan bağlantıları çiz
                if (results.pose_landmarks.landmark[start_idx].visibility > 0.1 and 
                    results.pose_landmarks.landmark[end_idx].visibility > 0.1):
                    
                    h, w, c = image.shape
                    cx1 = int(results.pose_landmarks.landmark[start_idx].x * w)
                    cy1 = int(results.pose_landmarks.landmark[start_idx].y * h)
                    cx2 = int(results.pose_landmarks.landmark[end_idx].x * w)
                    cy2 = int(results.pose_landmarks.landmark[end_idx].y * h)
                    
                    cv2.line(image, (cx1, cy1), (cx2, cy2), (0, 255, 0), 2)
                    cv2.circle(image, (cx1, cy1), 8, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (cx2, cy2), 8, (0, 0, 255), cv2.FILLED)
        
        # Bilgileri göster
        cv2.putText(image, f"Exercise: {self.__class__.__name__}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(image, f"Count: {self.counter}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        return image

    def get_joint_angle(self, landmarks):
        raise NotImplementedError("This method must be implemented in derived classes")

class Deadlift(BaseExercise):
    def __init__(self):
        super().__init__()
        self.detection_threshold = 160
        self.joint_visibility = [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE
        ]
        self.connections = [
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
            (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE)
        ]
        
    def get_joint_angle(self, landmarks):
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
              landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, 
               landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        
        angle = self.calculate_angle(shoulder, hip, knee)
        position = (int(hip[0] * 640), int(hip[1] * 480 + 50))
        return angle, position

class BicepsCurl(BaseExercise):
    def __init__(self):
        super().__init__()
        self.detection_threshold = 160
        self.joint_visibility = [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST
        ]
        self.connections = [
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
            (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST)
        ]
        
    def get_joint_angle(self, landmarks):
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, 
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        
        angle = self.calculate_angle(shoulder, elbow, wrist)
        position = (int(elbow[0] * 640), int(elbow[1] * 480 + 20))
        return angle, position

class Squat(BaseExercise):
    def __init__(self):
        super().__init__()
        self.detection_threshold = 160
        self.joint_visibility = [
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE,
            mp_pose.PoseLandmark.LEFT_ANKLE
        ]
        self.connections = [
            (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE),
            (mp_pose.PoseLandmark.LEFT_KNEE, mp_pose.PoseLandmark.LEFT_ANKLE)
        ]
        
    def get_joint_angle(self, landmarks):
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
              landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, 
               landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, 
                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        
        angle = self.calculate_angle(hip, knee, ankle)
        position = (int(knee[0] * 640), int(knee[1] * 480 + 50))
        return angle, position

class Pushup(BaseExercise):
    def __init__(self):
        super().__init__()
        self.detection_threshold = 90
        self.joint_visibility = [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_ELBOW,
            mp_pose.PoseLandmark.LEFT_WRIST
        ]
        self.connections = [
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
            (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST)
        ]
        
    def get_joint_angle(self, landmarks):
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, 
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, 
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        
        angle = self.calculate_angle(shoulder, elbow, wrist)
        position = (int(elbow[0] * 640), int(elbow[1] * 480 + 20))
        return angle, position

class Situp(BaseExercise):
    def __init__(self):
        super().__init__()
        self.detection_threshold = 90
        self.joint_visibility = [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE
        ]
        self.connections = [
            (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_HIP),
            (mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.LEFT_KNEE)
        ]
        
    def get_joint_angle(self, landmarks):
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
              landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, 
               landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        
        angle = self.calculate_angle(shoulder, hip, knee)
        position = (int(hip[0] * 640), int(hip[1] * 480 + 50))
        return angle, position
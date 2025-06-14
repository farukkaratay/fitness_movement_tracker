import cv2
import numpy as np
from exercises import Deadlift, BicepsCurl, Squat, Pushup, Situp

def show_selection_screen():
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    
    cv2.putText(img, "FITNESS HAREKET SAYACI", (50, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.putText(img, "1 - Deadlift", (50, 120), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, "2 - Biceps Curl", (50, 160), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, "3 - Squat", (50, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, "4 - Pushup", (50, 240), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, "5 - Situp", (50, 280), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.putText(img, "Secim yapmak icin numara tusuna basin", (50, 350), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
    
    cv2.imshow('Fitness Takip', img)
    key = cv2.waitKey(0)
    
    exercises = {
        ord('1'): Deadlift(),
        ord('2'): BicepsCurl(),
        ord('3'): Squat(),
        ord('4'): Pushup(),
        ord('5'): Situp()
    }
    
    return exercises.get(key, None)

def main():
    exercise = show_selection_screen()
    
    if not exercise:
        print("Gecersiz secim!")
        return
    
    cap = cv2.VideoCapture(0)
    exercise.init_counter()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Hareketi işle
        processed_frame = exercise.process_frame(frame)
        
        # Sonuçları göster
        cv2.imshow('Fitness Takip', processed_frame)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
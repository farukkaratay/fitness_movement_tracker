# Fitness Movement Tracker (Pose Estimation ile Egzersiz Sayacı)



Bu proje, **bilgisayar kamerası** aracılığıyla kullanıcının **vücut pozisyonunu gerçek zamanlı** olarak izleyen, analiz eden ve belirli fitness egzersizlerinin **tekrar sayılarını otomatik olarak hesaplayan** bir sistemdir. 

Google tarafından geliştirilen **MediaPipe Pose** iskelet algılama modeli kullanılarak, vücut üzerindeki **belirli eklem noktaları** tespit edilir ve bu noktalar arasındaki **açıların değişimi** değerlendirilerek bir hareketin tamamlanıp tamamlanmadığı anlaşılır. 

Böylece kullanıcı, egzersiz sırasında herhangi bir manuel girişe gerek kalmadan **doğru tekrar sayımı** elde edebilir. Sistem, görsel işleme için **OpenCV** kullanır ve her egzersiz türü için özel olarak tanımlanmış kurallar sayesinde hareketlerin doğruluğu ve geçerliliği hassas bir şekilde kontrol edilir.


## İçindekiler


1. [Özellikler](#özellikler)  
2. [Proje Yapısı](#proje-yapısı)  
3. [Kurulum ve Çalıştırma](#kurulum-ve-çalıştırma)  
4. [Kullanım](#kullanım)  

---

## Özellikler

- Gerçek zamanlı kamera ile vücut takibi  
- Otomatik tekrar sayacı  
- Beş farklı egzersiz:  
  - Deadlift  
  - Biceps Curl  
  - Squat  
  - Pushup  
  - Situp 
- Konsol ekranında kullanıcı seçimi  
- MediaPipe ile iskelet izleme  
- Açılara dayalı tekrar algılama  

---

## Proje Yapısı

├── fitness_tracker.py 

├── exercises.py 

└── README.md


- `fitness_tracker.py`: Kullanıcının seçim ekranını gösterir, seçilen egzersiz sınıfını başlatır ve kameradan gelen görüntüleri ilgili egzersiz sınıfına iletir.  
- `exercises.py`: `BaseExercise` sınıfı ve türetilmiş egzersiz sınıflarını içerir (Deadlift, BicepsCurl, Squat, Pushup, Situp). Her sınıf, izlenecek eklem noktaları, açı hesaplama ve tekrar sayma mantığını tanımlar.  


---

## Kurulum ve Çalıştırma


1. **Gerekli kütüphaneleri yükleyin.**
```bash
   pip install opencv-python mediapipe numpy
```
2. **Projeyi kopyalayın veya klonlayın.**
```bash
  git clone <repository-url>
  cd <repository-folder>
```
3. **Uygulamayı çalıştırın.**
```bash
  python fitness_tracker.py
```
---

## Kullanım

Program başlatıldığında konsolda bir seçim ekranı görüntülenir.

Aşağıdaki tuşlardan birini girin ve `Enter` tuşuna basın:

*1* – Deadlift
 
*2* – Biceps Curl

*3* – Squat

*4* – Pushup

*5* – Situp


Seçimin ardından kamera açılır ve egzersiz takibi başlar.  
Ekranda:

- Egzersiz ismi  
- Açı bilgisi  
- Mevcut tekrar sayısı  

görüntülenir.

Uygulamayı kapatmak için, kamera açıkken `q` tuşuna basın.




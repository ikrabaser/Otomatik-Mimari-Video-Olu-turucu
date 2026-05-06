# Otomatik Mimari Video Oluşturucu

<img width="795" height="672" alt="image" src="https://github.com/user-attachments/assets/fc0863c7-34fe-467a-babf-cd0a48fe4e36" />

Python ile geliştirilmiş otomatik video oluşturma projesidir. Unsplash API üzerinden belirlenen anahtar kelimeye göre görseller indirir, bu görselleri MoviePy ile birleştirerek otomatik bir video oluşturur ve isteğe bağlı olarak arka plan müziği ekler.

## Özellikler

- Unsplash API ile otomatik görsel indirme
- Anahtar kelimeye göre görsel arama
- Görsellerden slideshow tarzı video oluşturma
- Arka plan müziği ekleme
- Otomatik MP4 çıktısı oluşturma
- Eski görselleri otomatik temizleme

## Kullanılan Teknolojiler

- Python
- MoviePy
- Requests
- python-dotenv
- Unsplash API

## Kurulum

```bash
pip install -r requirements.txt
```

`.env` dosyası oluştur:

```env
UNSPLASH_ACCESS_KEY=your_api_key
```

## Çalıştırma

```bash
python main.py
```

## Proje Yapısı

```bash
project/
│
├── images/
├── music/
│   └── music.mp3
├── .env
├── main.py
└── video.mp4
```

## Çıktı

Program çalıştırıldığında:
- Görseller otomatik indirilir
- Video oluşturulur
- Arka plan müziği eklenir
- `video.mp4` çıktısı alınır

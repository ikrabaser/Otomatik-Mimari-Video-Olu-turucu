import os
import requests
from dotenv import load_dotenv
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips


load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
MUSIC_PATH = os.path.join(BASE_DIR, "music", "music.mp3")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "video.mp4")

SEARCH_QUERY = "architecture"
IMAGE_COUNT = 10
IMAGE_DURATION = 3
FPS = 24


def clear_old_images():
    if not os.path.exists(IMAGE_FOLDER):
        return

    for file_name in os.listdir(IMAGE_FOLDER):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            os.remove(os.path.join(IMAGE_FOLDER, file_name))


def download_images():
    if not UNSPLASH_ACCESS_KEY:
        print("Unsplash API key bulunamadı.")
        print(".env dosyasına UNSPLASH_ACCESS_KEY değerini eklemelisin.")
        return []

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": SEARCH_QUERY,
        "orientation": "portrait",
        "per_page": IMAGE_COUNT,
        "client_id": UNSPLASH_ACCESS_KEY,
    }

    print("Unsplash'tan görseller alınıyor...")

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        print("Unsplash isteği başarısız oldu:")
        print(error)
        return []
    except ValueError:
        print("Unsplash cevabı JSON formatında değil.")
        print(response.text[:500])
        return []

    if "errors" in data:
        print("Unsplash API hata döndürdü:")
        print(data["errors"])
        return []

    photos = data.get("results", [])

    if not photos:
        print("Görsel bulunamadı.")
        return []

    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    clear_old_images()

    image_paths = []

    for index, photo in enumerate(photos, start=1):
        image_url = photo.get("urls", {}).get("regular")

        if not image_url:
            continue

        filename = os.path.join(IMAGE_FOLDER, f"image_{index}.jpg")

        try:
            image_response = requests.get(image_url, timeout=20)
            image_response.raise_for_status()

            with open(filename, "wb") as file:
                file.write(image_response.content)

            image_paths.append(filename)
            print(f"{index}. görsel indirildi: {filename}")

        except requests.RequestException as error:
            print(f"{index}. görsel indirilemedi:")
            print(error)

    print(f"Toplam {len(image_paths)} görsel indirildi.")
    return image_paths


def create_video(image_paths):
    if not image_paths:
        print("Video oluşturmak için görsel bulunamadı.")
        return

    clips = []
    audio = None
    video = None

    try:
        for path in image_paths:
            clip = ImageClip(path).set_duration(IMAGE_DURATION)
            clips.append(clip)

        print("Video hazırlanıyor...")
        video = concatenate_videoclips(clips, method="compose")

        if os.path.exists(MUSIC_PATH):
            print("Arka plan müziği ekleniyor...")
            audio = AudioFileClip(MUSIC_PATH).volumex(0.8)

            if audio.duration > video.duration:
                audio = audio.subclip(0, video.duration)

            video = video.set_audio(audio)
        else:
            print("Müzik dosyası bulunamadı. Video sessiz oluşturulacak.")
            print(f"Beklenen müzik yolu: {MUSIC_PATH}")

        print("Video dışa aktarılıyor...")
        video.write_videofile(OUTPUT_VIDEO, fps=FPS)

        print(f"Video oluşturuldu: {OUTPUT_VIDEO}")

    finally:
        for clip in clips:
            clip.close()

        if audio:
            audio.close()

        if video:
            video.close()


def main():
    image_paths = download_images()
    create_video(image_paths)


if __name__ == "__main__":
    main()
import os
from PIL import Image
from instagrapi import Client
from dotenv import load_dotenv

def combine_images_2x2(image_paths, output_path="combined.jpg", resize_to=(512, 512)):
    """
    image_paths: [좌상단, 우상단, 좌하단, 우하단] 이미지 경로 리스트
    output_path: 저장할 파일 경로
    resize_to: (너비, 높이)로 각 이미지를 조정
    """
    if len(image_paths) != 4:
        raise ValueError("이미지 경로는 4개여야 합니다.")
    images = [Image.open(p).resize(resize_to) for p in image_paths]
    grid_size = (resize_to[0]*2, resize_to[1]*2)
    combined = Image.new("RGB", grid_size, (255,255,255))
    # 좌상단
    combined.paste(images[0], (0, 0))
    # 우상단
    combined.paste(images[1], (resize_to[0], 0))
    # 좌하단
    combined.paste(images[2], (0, resize_to[1]))
    # 우하단
    combined.paste(images[3], (resize_to[0], resize_to[1]))
    combined.save(output_path)
    return output_path

def post_to_instagram(image_path, caption):
    load_dotenv()
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    cl = Client()
    cl.login(username, password)
    cl.photo_upload(image_path, caption)
    print("Instagram 업로드 완료!")

if __name__ == "__main__":
    image_paths = [
        "01.png",
        "02.png",
        "03.png",
        "04.png"
    ]
    combined_path = combine_images_2x2(image_paths, output_path="final_4cut.jpg", resize_to=(512, 512))
    print(f"이미지 결합 완료: {combined_path}")

    caption = "오늘의 AI 4컷 만화! #ai #4컷 #키티"
    post_to_instagram(combined_path, caption)
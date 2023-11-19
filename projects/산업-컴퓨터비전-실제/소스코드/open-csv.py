import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

def rotate_image(image, angle):
    """이미지를 주어진 각도만큼 회전시킵니다."""
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    return cv2.warpAffine(image, M, (cols, rows))

def translate_image(image, x, y):
    """이미지를 주어진 x, y 값만큼 이동시킵니다."""
    rows, cols = image.shape[:2]
    M = np.float32([[1, 0, x], [0, 1, y]])
    return cv2.warpAffine(image, M, (cols, rows))

def scale_image(image, scale):
    """이미지를 주어진 비율만큼 확대 또는 축소합니다."""
    return cv2.resize(image, None, fx=scale, fy=scale)

def flip_image(image, axis):
    """이미지를 주어진 축으로 반전시킵니다."""
    return cv2.flip(image, axis)

def crop_image(image, x, y, w, h):
    """이미지를 주어진 좌표와 크기에 맞게 자릅니다."""
    return image[y:y+h, x:x+w]

def add_noise(image):
    """이미지에 노이즈를 추가합니다."""
    noise = np.zeros(image.shape, np.uint8)
    cv2.randn(noise, (0, 0, 0), (50, 50, 50))
    return cv2.add(image, noise)

def cvtColor(images, x):
    hsv = cv2.cvtColor(images, cv2.COLOR_BGR2HSV)
    # 색상 변환
    hue_shift = 30
    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180

    # HSV 채널을 BGR 채널로 변환
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def gaussianBlur(images, x):
    # 가우시안 블러 적용
    ksize = (x, x)
    sigmaX = 300
    return cv2.GaussianBlur(images, ksize,sigmaX)

def plot_images(images, titles):
    """이미지를 그래프로 출력합니다."""
    fig, axs = plt.subplots(1, len(images), figsize=(15, 15))
    for i, image in enumerate(images):
        axs[i].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        axs[i].set_title(titles[i])
        axs[i].axis('off')
    plt.show()


# 학습용 이미지가 있는 디렉토리 경로
dir_path = 'D:/02.CBNU/캡스톤/개인발표/sample'

# 데이터 증량을 위한 파라미터 설정
angle = 30
x = 50
y = 50
scale = 2
axis = 1
x1 = 20
y1 = 20
w = 100
h = 100

images = []
titles = []

# 이미지 파일 불러오기
for file_name in os.listdir(dir_path):
    print(file_name)
    image_path = os.path.join(dir_path, file_name)
    image = cv2.imread('./sample/lena.jpg')

    images.append(image)
    titles.append('원본')

    # 이미지 회전
    rotated_image = rotate_image(image, angle)
    images.append(rotated_image)
    titles.append('회전')

    # 이미지 이동
    translated_image = translate_image(image, x, y)
    images.append(translated_image)
    titles.append('이동')

    # 이미지 확대 및 축소
    scaled = scale_image(image, scale)
    images.append(scaled)
    titles.append('확대 및 축소')

    # 이미지 반전
    flipped_image = flip_image(image, axis)
    images.append(flipped_image)
    titles.append('반전')

    # 이미지 자르기
    cropped_image = crop_image(image, x1, y1, w, h)
    images.append(cropped_image)
    titles.append('자르기')

    # 이미지 노이즈 추가
    noisy_image = add_noise(image)
    images.append(noisy_image)
    titles.append('노이즈')

    # 색조 변경
    cvt_image = cvtColor(image, 30)
    images.append(cvt_image)
    titles.append('채도')

    # 가우시안 블러
    blur_image = gaussianBlur(image, 5)
    images.append(blur_image)
    titles.append('가우시안블러')

# 이미지 출력
plot_images(images, titles)
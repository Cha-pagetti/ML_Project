# 📌 Assets 디렉토리 파일 정리

## 원본 데이터

### ✔ mnist_train.npz
- **설명**: 원본 MNIST 데이터셋
- **형식**: 28x28 흑백 이미지
- **생성 코드**: `assets/gen_mnist.ipynb`
- **용도**: 기본 학습 데이터

---

## 증강 데이터 (RGB 컬러)

### ✔ mnist_aug_color.npz
- **설명**: 6가지 증강 기법이 모두 적용된 RGB 데이터
- **생성 코드**: `data_augmentation/aug_font_color_full.ipynb`
- **증강 기법**: 
  - 회전 (Rotation)
  - 블러 (Blur)
  - 폰트 크기 (Font Size)
  - 폰트 스타일 (Font Weight)
  - 위치 변형 (Position)
  - 색상 (Color) - 7가지 무지개 색상
- **형식**: 28x28x3 RGB 이미지
- **특징**: 모든 증강 기법 100% 적용
- **용도**: 강한 증강이 필요한 컬러 이미지 학습

### ✔ mnist_aug_color_partial.npz
- **설명**: 색상 필수 + 부분 증강 적용된 RGB 데이터
- **생성 코드**: `data_augmentation/aug_font_color_partial.ipynb`
- **증강 방식**: 
  - 색상: **항상 적용** (필수)
  - 나머지 4개 기법: 1~3개 랜덤 선택
- **형식**: 28x28x3 RGB 이미지
- **특징**: 
  - 색상 다양성 100% 보장
  - 과도한 증강 방지 (최대 3개 기법)
  - 자연스러운 변형
- **용도**: 적절한 변형이 필요한 컬러 이미지 학습

---

## 학습 모델

### ✔ mnist_ml_model.pkl
- **설명**: 학습된 머신러닝 모델
- **생성 코드**: `classify/mnist_train.ipynb`
- **형식**: Pickle 파일
- **용도**: 학습된 모델 재사용 및 테스트

---

## 리소스 파일

### ✔ *.ttf (폰트 파일)
- **파일 목록**:
  - MaruBuri-Bold.ttf
  - MaruBuri-ExtraLight.ttf
  - MaruBuri-Light.ttf
  - MaruBuri-Regular.ttf
  - MaruBuri-SemiBold.ttf
- **용도**: 데이터 증강 시 폰트 스타일 변형 적용

### ✔ gen_mnist.ipynb
- **설명**: 원본 MNIST 데이터 생성 노트북
- **출력**: `mnist_train.npz`

---

## 파일 구조

```
assets/
├── 데이터셋
│   ├── mnist_train.npz              # 원본 흑백 데이터
│   ├── mnist_aug_color.npz          # RGB 완전 증강
│   └── mnist_aug_color_partial.npz  # RGB 부분 증강
│
├── 모델
│   └── mnist_ml_model.pkl           # 학습된 모델
│
├── 리소스
│   ├── MaruBuri-Bold.ttf
│   ├── MaruBuri-ExtraLight.ttf
│   ├── MaruBuri-Light.ttf
│   ├── MaruBuri-Regular.ttf
│   └── MaruBuri-SemiBold.ttf
│
└── 생성 코드
    └── gen_mnist.ipynb              # 원본 데이터 생성
```

---

## 데이터셋 선택 가이드

| 목적 | 추천 파일 | 이미지 형식 |
|------|----------|------------|
| 기본 학습 | `mnist_train.npz` | 28x28 흑백 |
| 컬러 강한 증강 | `mnist_aug_color.npz` | 28x28x3 RGB |
| 컬러 적절한 증강 | `mnist_aug_color_partial.npz` | 28x28x3 RGB |

---

## 데이터 로드 예시

```python
import numpy as np

# 원본 흑백 데이터
data = np.load('assets/mnist_train.npz')
images = data['train_images']  # Shape: (N, 28, 28)
labels = data['train_labels']  # Shape: (N,)

# RGB 컬러 데이터
color_data = np.load('assets/mnist_aug_color_partial.npz')
rgb_images = color_data['train_images']  # Shape: (N, 28, 28, 3)
rgb_labels = color_data['train_labels']  # Shape: (N,)

print(f"흑백 이미지: {images.shape}")
print(f"컬러 이미지: {rgb_images.shape}")
```

---

## 관련 문서

- 데이터 증강 코드 상세 설명: `../data_augmentation/data_augmentation.md`
- 학습 및 테스트 코드: `../classify/`

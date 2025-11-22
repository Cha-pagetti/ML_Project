# 📌 Data Augmentation 코드 정리

## 증강 코드 (흑백)

### ✔ aug_font.ipynb
- **설명**: 5가지 증강 기법을 모두 적용한 흑백 데이터 생성
- **증강 기법**:
  1. 회전 (Rotation): -20° ~ 20°
  2. 블러 (Blur): Gaussian blur 0 ~ 0.8
  3. 폰트 크기 (Font Size): 20 ~ 30
  4. 폰트 스타일 (Font Weight): 5가지 폰트 변형
  5. 위치 변형 (Position): X: -8~8, Y: -6~6
- **출력 형식**: 28x28 흑백 이미지
- **출력 파일**: ❌ 현재 미생성 (코드만 존재)
- **용도**: 완전 증강 흑백 데이터 생성용

### ✔ aug_font_partial.ipynb
- **설명**: 부분 증강 흑백 데이터 생성 (각 기법 50% 확률)
- **증강 방식**: 5개 기법 각각 1/2 확률로 독립 적용
- **특징**:
  - 각 기법이 독립적으로 50% 확률로 적용
  - 모든 기법 적용 가능 (확률: 3.125%)
  - 아무것도 적용 안 될 수 있음 (확률: 3.125%)
- **출력 형식**: 28x28 흑백 이미지
- **출력 파일**: ❌ 현재 미생성 (코드만 존재)
- **용도**: 자연스러운 변형 흑백 데이터 생성용

---

## 증강 코드 (컬러)

### ✔ aug_font_color_full.ipynb
- **설명**: 6가지 증강 기법을 모두 적용한 RGB 데이터 생성
- **증강 기법**:
  1. 회전 (Rotation)
  2. 블러 (Blur)
  3. 폰트 크기 (Font Size)
  4. 폰트 스타일 (Font Weight)
  5. 위치 변형 (Position)
  6. **색상 (Color)**: 7가지 무지개 색상 (전경/배경 조합)
- **출력 형식**: 28x28x3 RGB 이미지
- **출력 파일**: ✅ `../assets/mnist_aug_color.npz`
- **용도**: 완전 증강 컬러 데이터 생성

### ✔ aug_font_color_partial.ipynb
- **설명**: 색상 필수 + 부분 증강 RGB 데이터 생성
- **증강 방식**:
  - **색상**: 항상 적용 (7가지 무지개 색상)
  - **나머지 4개 기법**: 1~3개 랜덤 선택 (`random.sample()` 사용)
- **핵심 로직**:
  ```python
  num_augmentations = random.randint(1, 3)  # 1, 2, 3 중 선택
  augmentation_indices = random.sample(range(4), num_augmentations)
  ```
- **특징**:
  - 색상은 100% 적용 보장
  - 회전/블러/크기/위치 중 최소 1개, 최대 3개 적용
  - 모든 기법 적용 확률: 0%
  - 색상만 적용 확률: 0%
- **출력 형식**: 28x28x3 RGB 이미지
- **출력 파일**: ✅ `../assets/mnist_aug_color_partial.npz`
- **용도**: 색상 다양성 + 적절한 변형 데이터 생성

---

## 코드 구조 요약

```
data_augmentation/
├── aug_font.ipynb                # 흑백 완전 증강 (5개 기법)
├── aug_font_partial.ipynb        # 흑백 부분 증강 (각 50% 확률)
├── aug_font_color_full.ipynb     # RGB 완전 증강 (6개 기법)
└── aug_font_color_partial.ipynb  # RGB 부분 증강 (색상 필수 + 1-3개)
```

---

## 생성되는 데이터셋

| 코드 | 출력 파일 | 상태 | 형식 |
|------|----------|------|------|
| `aug_font.ipynb` | - | ❌ 미생성 | 28x28 흑백 |
| `aug_font_partial.ipynb` | - | ❌ 미생성 | 28x28 흑백 |
| `aug_font_color_full.ipynb` | `mnist_aug_color.npz` | ✅ 생성됨 | 28x28x3 RGB |
| `aug_font_color_partial.ipynb` | `mnist_aug_color_partial.npz` | ✅ 생성됨 | 28x28x3 RGB |

---

## 증강 기법 비교

| 기법 | Full | Partial (흑백) | Color Full | Color Partial |
|------|------|---------------|------------|---------------|
| 회전 | ✅ 항상 | 🎲 50% | ✅ 항상 | 🎲 1-3개 중 |
| 블러 | ✅ 항상 | 🎲 50% | ✅ 항상 | 🎲 1-3개 중 |
| 크기 | ✅ 항상 | 🎲 50% | ✅ 항상 | 🎲 1-3개 중 |
| 폰트 | ✅ 항상 | 🎲 50% | ✅ 항상 | ✅ 항상 |
| 위치 | ✅ 항상 | 🎲 50% | ✅ 항상 | 🎲 1-3개 중 |
| 색상 | ❌ | ❌ | ✅ 항상 | ✅ 항상 |

---

## 사용 가이드

### 데이터셋 생성하기

```python
# 1. 해당 노트북 열기
# 2. 파라미터 설정 확인/수정
ROTATION_RANGE = (-20, 20)
FONT_SIZE_RANGE = (20, 30)
POSITION_X_RANGE = (-8, 8)
POSITION_Y_RANGE = (-6, 6)
BLUR_RADIUS_RANGE = (0, 0.8)
VARIATIONS_PER_DIGIT = 3

# 3. 전체 셀 실행
# 4. assets/ 디렉토리에 .npz 파일 생성 확인
```

### 생성된 데이터 로드하기

```python
import numpy as np

# RGB 컬러 데이터 로드
data = np.load('../assets/mnist_aug_color_partial.npz')
images = data['train_images']  # Shape: (N, 28, 28, 3)
labels = data['train_labels']  # Shape: (N,)

print(f"이미지 개수: {len(images)}")
print(f"이미지 형태: {images.shape}")
```

"""
MNIST 데이터셋 병합 도구

GUI를 통해 여러 .npz 파일을 선택하고 하나로 병합합니다.
- 이미지 shape가 다르면 병합 실패
- train_images와 train_labels 키를 사용
"""

import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import os


def select_files():
    """GUI로 npz 파일들을 선택"""
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨김
    
    file_paths = filedialog.askopenfilenames(
        title="병합할 .npz 파일들을 선택하세요 (2개 이상)",
        filetypes=[("NumPy files", "*.npz"), ("All files", "*.*")],
        initialdir=os.path.dirname(os.path.abspath(__file__))
    )
    
    return list(file_paths)


def load_and_validate_datasets(file_paths):
    """
    데이터셋을 로드하고 검증
    
    Returns:
        list: (images, digit_labels, fg_labels, bg_labels, filename) 튜플들의 리스트
    """
    datasets = []
    first_shape = None
    
    print("\n" + "="*60)
    print("📂 데이터셋 로드 및 검증")
    print("="*60)
    
    for i, file_path in enumerate(file_paths, 1):
        filename = os.path.basename(file_path)
        print(f"\n[{i}/{len(file_paths)}] {filename}")
        
        try:
            # npz 파일 로드
            data = np.load(file_path)
            
            # 키 확인
            required_keys = ['train_images', 'digit_labels', 'fg_color_labels', 'bg_color_labels']
            if not all(key in data for key in required_keys):
                raise ValueError(f"❌ 필수 키가 없습니다. 필요: {required_keys}\n   실제: {list(data.keys())}")
            
            images = data['train_images']
            digit_labels = data['digit_labels']
            fg_labels = data['fg_color_labels']
            bg_labels = data['bg_color_labels']
            
            # Shape 확인
            print(f"   Images: {images.shape}, dtype: {images.dtype}")
            print(f"   Digit Labels: {digit_labels.shape}, dtype: {digit_labels.dtype}")
            print(f"   FG Color Labels: {fg_labels.shape}, dtype: {fg_labels.dtype}")
            print(f"   BG Color Labels: {bg_labels.shape}, dtype: {bg_labels.dtype}")
            
            # 첫 번째 파일의 shape를 기준으로 설정
            if first_shape is None:
                first_shape = images.shape[1:]  # (28, 28) 또는 (28, 28, 3)
                print(f"   ✅ 기준 shape 설정: {first_shape}")
            else:
                # 나머지 파일들은 shape 검증
                if images.shape[1:] != first_shape:
                    raise ValueError(
                        f"❌ Shape 불일치!\n"
                        f"   기준 shape: {first_shape}\n"
                        f"   현재 shape: {images.shape[1:]}\n"
                        f"   → 모든 데이터셋의 이미지 크기가 동일해야 합니다."
                    )
                print(f"   ✅ Shape 일치: {first_shape}")
            
            # 레이블 개수 확인
            if not (len(images) == len(digit_labels) == len(fg_labels) == len(bg_labels)):
                raise ValueError(
                    f"❌ 이미지와 레이블 개수 불일치!\n"
                    f"   Images: {len(images)}, Digit: {len(digit_labels)}, FG: {len(fg_labels)}, BG: {len(bg_labels)}"
                )
            
            datasets.append((images, digit_labels, fg_labels, bg_labels, filename))
            print(f"   ✅ 로드 성공: {len(images)}개 샘플")
            
        except Exception as e:
            print(f"   ❌ 오류 발생: {e}")
            raise
    
    return datasets


def merge_datasets(datasets):
    """데이터셋들을 병합"""
    print("\n" + "="*60)
    print("🔄 데이터셋 병합 중...")
    print("="*60)
    
    all_images = []
    all_digit_labels = []
    all_fg_labels = []
    all_bg_labels = []
    
    for images, digit_labels, fg_labels, bg_labels, filename in datasets:
        all_images.append(images)
        all_digit_labels.append(digit_labels)
        all_fg_labels.append(fg_labels)
        all_bg_labels.append(bg_labels)
        print(f"   추가: {filename} ({len(images)}개)")
    
    # numpy 배열로 연결
    merged_images = np.concatenate(all_images, axis=0)
    merged_digit_labels = np.concatenate(all_digit_labels, axis=0)
    merged_fg_labels = np.concatenate(all_fg_labels, axis=0)
    merged_bg_labels = np.concatenate(all_bg_labels, axis=0)
    
    print(f"\n   ✅ 병합 완료!")
    print(f"   총 이미지: {merged_images.shape}")
    print(f"   총 숫자 레이블: {merged_digit_labels.shape}")
    print(f"   총 전경색 레이블: {merged_fg_labels.shape}")
    print(f"   총 배경색 레이블: {merged_bg_labels.shape}")
    
    return merged_images, merged_digit_labels, merged_fg_labels, merged_bg_labels


def save_merged_dataset(images, digit_labels, fg_labels, bg_labels, source_files):
    """병합된 데이터셋을 저장"""
    root = tk.Tk()
    root.withdraw()
    
    # 기본 파일명 생성
    default_name = "merged_dataset.npz"
    
    save_path = filedialog.asksaveasfilename(
        title="병합된 데이터셋 저장",
        defaultextension=".npz",
        filetypes=[("NumPy files", "*.npz")],
        initialfile=default_name,
        initialdir=os.path.dirname(source_files[0])
    )
    
    if not save_path:
        print("\n⚠️  저장 취소됨")
        return None
    
    # 저장
    np.savez_compressed(
        save_path,
        train_images=images,
        digit_labels=digit_labels,
        fg_color_labels=fg_labels,
        bg_color_labels=bg_labels
    )
    
    file_size_mb = os.path.getsize(save_path) / 1024 / 1024
    
    print("\n" + "="*60)
    print("💾 저장 완료!")
    print("="*60)
    print(f"   파일 경로: {save_path}")
    print(f"   파일 크기: {file_size_mb:.2f} MB")
    print(f"   이미지 수: {len(images)}")
    print("="*60)
    
    return save_path


def main():
    """메인 함수"""
    print("="*60)
    print("🔀 MNIST 데이터셋 병합 도구")
    print("="*60)
    
    try:
        # 1. 파일 선택
        file_paths = select_files()
        
        if len(file_paths) < 2:
            messagebox.showerror(
                "오류",
                "최소 2개 이상의 파일을 선택해야 합니다."
            )
            print("\n❌ 최소 2개 이상의 파일을 선택해야 합니다.")
            return
        
        print(f"\n선택된 파일: {len(file_paths)}개")
        for i, path in enumerate(file_paths, 1):
            print(f"  {i}. {os.path.basename(path)}")
        
        # 2. 데이터셋 로드 및 검증
        datasets = load_and_validate_datasets(file_paths)
        
        # 3. 병합
        merged_images, merged_digit_labels, merged_fg_labels, merged_bg_labels = merge_datasets(datasets)
        
        # 4. 저장
        save_path = save_merged_dataset(merged_images, merged_digit_labels, merged_fg_labels, merged_bg_labels, file_paths)
        
        if save_path:
            messagebox.showinfo(
                "완료",
                f"데이터셋 병합 완료!\n\n"
                f"파일: {os.path.basename(save_path)}\n"
                f"총 샘플: {len(merged_images)}개"
            )
            print("\n✅ 모든 작업 완료!")
        
    except Exception as e:
        error_msg = f"오류 발생:\n{str(e)}"
        messagebox.showerror("오류", error_msg)
        print(f"\n❌ {error_msg}")
        raise


if __name__ == "__main__":
    main()

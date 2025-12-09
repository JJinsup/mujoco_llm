# 🤖 MuJoCo + LLM 실습 리포지토리  
_2025 동계 VLA 특강 실습 자료_

본 리포지토리는 **MuJoCo 기반 로봇 시뮬레이션**, **경량화 LLM(VLA) 모델 실습**,  
그리고 **On-Device RAG·Fine-tuning** 실험을 포함한 학습용 코드와 가이드를 제공합니다.

한국의 국민대학교 **Wireless Intelligent Technology Lab (WIT LAB)**  
2025 동계 특강 *"From Simulation to Reality: VLA 모델로 제어하는 로봇팔"* 실습 자료 기반입니다.

---

## 📦 Repository Structure
│── assets/ # 시뮬레이션 리소스 (URDF, XML 등)
│── learn_LLM/ # LLM 실습: RAG, Fine-tuning, datagen
│ ├── datagen.ipynb
│ ├── finetuning.ipynb
│ ├── ollama_RAG.ipynb
│ ├── outputs/ # LoRA 결과물(자동 생성)
│ ├── src/ # PDF, 이미지 등 분석 자료
│ └── yolo_GEMINI.ipynb
│
│── tutorial/ # MuJoCo 실습 자료
│ ├── mujoco_simple.ipynb
│ ├── mujoco_pendulum.ipynb
│ ├── mujoco_inverted_pendulum.ipynb
│ └── ppo_cartpole_mujoco.zip
│
│── utils/ # 시뮬레이션 및 시각화 유틸
│ ├── mujoco_renderer.py
│ ├── lidar_visualizer.py
│ ├── scene_creator.py
│ └── camera_recorder.py
│
└── scripts/ # 설치/실행 스크립트

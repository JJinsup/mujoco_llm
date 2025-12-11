import threading
import json
import yaml
import os
import re
from queue import Queue
from dotenv import load_dotenv
from google import genai
from google.genai import types

# YOLO
from ultralytics import YOLO
import cv2


load_dotenv()


# ============================================
# GEMINI LLM RUNNER FOR TURTLEBOT3
# ============================================

class GeminiTb3:
    def __init__(self, prompt_path, model="gemini-2.5-flash", command_queue=None):
        self.command_queue = command_queue if command_queue else Queue()

        # Load prompt.yaml
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.system_instruction = yaml.safe_load(f)["template"]

        # Gemini client
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.model_name = model

        # threads
        self.thread = None
        self.stop_event = threading.Event()

    # ----------------------------------------
    def run_gemini(self, question, detection_json):
        """Gemini에게 분석 요청"""
        user_content = f"""
# 감지된 객체 정보(JSON):
{detection_json}

# 질문:
{question}
"""
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.1
                ),
                contents=user_content
            )
            return response.text
        except Exception as e:
            return f"Gemini Error: {e}"
    # ----------------------------------------
    def _extract_target_from_question(self, question: str) -> str | None:
        if "하트" in question:
            return "heart"
        if "스페이드" in question:
            return "spade"
        if "클로버" in question or "클럽" in question:
            return "club"
        if "다이아" in question or "다이아몬드" in question:
            return "diamond"
        return None

    # ----------------------------------------
    def talk(self, sim):
        while not self.stop_event.is_set():
            try:
                question = input("\n💬 Human: ")

                # 1) YOLO 결과
                det_dict = sim.yolo_detect_dict()
                det_json = json.dumps(det_dict, ensure_ascii=False, indent=2)

                # 1.5) 질문 안에 목표 카드 있는지 확인
                target = self._extract_target_from_question(question)
                if target and target not in det_dict:
                    # 아직 안 보이면 탐색 액션 한 번 추가
                    print(f"➡️ '{target}' 카드가 안 보여서 제자리 회전으로 둘러볼게요.")
                    self.command_queue.put("제자리 회전")

                # 2) LLM 호출
                answer = self.run_gemini(question, det_json)
                print(f"\n🤖 Gemini:\n{answer}\n")

                # 3) LLM이 낸 Action도 그대로 반영
                action_match = re.search(r"Action:\s*([^\n]+)", answer)
                action = action_match.group(1).strip() if action_match else ""

                if action:
                    print(f"➡️ Extracted Action: {action}")
                    self.command_queue.put(action)

            except EOFError:
                break
    # ----------------------------------------
    # Gemini + YOLO 스레드 시작
    def start(self, sim):
        self.thread = threading.Thread(target=self.talk, args=(sim,), daemon=True)
        self.thread.start()
        

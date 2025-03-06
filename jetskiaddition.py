import pyautogui
import easyocr
import cv2
import time
import numpy as np
import re
from PIL import ImageGrab

reader = easyocr.Reader(['en'])

# Define screen regions (adjust based on your resolution)
problem_region = (1188, 686, 1429, 738)  # Region for the math problem
answer_boxes = [
    (1139, 756, 1195, 807),  # First answer box
    (1229, 763, 1285, 807),  # Second answer box
    (1319, 763, 1375, 807),  # Third answer box
    (1409, 763, 1465, 807)   # Fourth answer box
]
click_positions = [
    (1140, 763),  # Click position for first answer
    (1230, 763),  # Click position for second answer
    (1320, 763),  # Click position for third answer
    (1410, 763)   # Click position for fourth answer
]

def capture_text(region):
    """Capture a screen region and extract text using EasyOCR."""
    screenshot = ImageGrab.grab(bbox=region)
    gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    
    result = reader.readtext(gray)
    
    text = " ".join([r[1] for r in result]).strip()
    
    print(f"Detected text: {text}")
    
    filtered_text = re.sub(r'[^0-9+]', '', text)  # Only keep numbers and '+'
    
    return filtered_text

def solve_problem(problem):
    numbers = [int(num) for num in problem.split("+") if num.strip().isdigit()]
    return sum(numbers) if len(numbers) == 2 else None

def find_correct_answer(correct_answer):
    for i, box in enumerate(answer_boxes):
        answer_text = capture_text(box)
        
        
        if answer_text.isdigit() and int(answer_text) == correct_answer:
            return i
    return None

def jet_ski_bot():
    print("Starting Jet Ski Addition bot in 3 seconds...")
    time.sleep(3)

    while True:
        try:
            # Read and solve the problem
            problem_text = capture_text(problem_region)
            print(f"Problem detected: {problem_text}")
            correct_answer = solve_problem(problem_text)

            if correct_answer is not None:
                print(f"Correct Answer: {correct_answer}")

                correct_index = find_correct_answer(correct_answer)

                if correct_index is not None:
                    pyautogui.click(click_positions[correct_index])
                else:
                    print("Could not find the correct answer in options.")
            else:
                print("Could not solve the problem correctly.")

            # Small delay before next loop
            time.sleep(0.05)

        except KeyboardInterrupt:
            print("Bot stopped by user.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    jet_ski_bot()

import pyautogui
import keyboard
import time
import random
import requests
import json

# Speed of mouse movement

def get_direction(output,speed):
    count = 0
    if output == 'f':
        output = input('enter the direction')  
        return True
    elif output == 'up':
        count = 0
        pyautogui.move(0, -speed)  # Move mouse up
        return True
    elif output == 'left':
        count = 0
        pyautogui.move(-speed, 0)  # Move mouse left
        return True
    elif output == 'right':
        count = 0
        pyautogui.move(0, speed)   # Move mouse down
        return True
    elif output == 'down':
        count = 0
        pyautogui.move(speed, 0)   # Move mouse right
        return True
    elif output == 'enter' and count == 0:
        count+=1
        pyautogui.click()
        return True
    elif output == 'enter' and count == 1:
        count+=1
        pyautogui.doubleClick()
        return True        
    elif output == 'q':  # Stop the loop when 'q' is pressed
        return False

# Infinite loop for mouse movement until 'q' is pressed
while True:    
    direction = random.choice(['left','right','up','down','enter','q'])
    if not get_direction(direction,speed=10):
        break

# import pyautogui
# import time
# import threading

# # Set the amount to move the cursor
# move_amount = 30

# # Shared variable to store the current direction
# current_direction = 'up'
# direction_lock = threading.Lock()

# def get_direction():
#     return random.choice(['up','down','left','right','enter'])
    

# def direction_worker():
#     global current_direction
#     while True:
#         new_direction = get_direction()
#         with direction_lock:
#             current_direction = new_direction
#         time.sleep(1)  # Update every 1 second or as needed

# # Start the direction worker thread
# thread = threading.Thread(target=direction_worker, daemon=True)
# thread.start()

# while True:
#     with direction_lock:
#         direction = current_direction

#     if direction == 'up':
#         pyautogui.move(0, -move_amount)
#     elif direction == 'down':
#         pyautogui.move(0, move_amount)
#     elif direction == 'left':
#         pyautogui.move(-move_amount, 0)
#     elif direction == 'right':
#         pyautogui.move(move_amount, 0)
#     elif direction == 'enter':
#         pyautogui.leftClick()

#     time.sleep(0.1) 
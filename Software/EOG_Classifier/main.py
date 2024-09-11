import time
import serial
from collections import deque
import re
import torch
import numpy as np
from variables import BAUD_RATE,SAMPLE_RATE,COM
from utils import print_values_using_BiLSTM,print_values_using_threshold,get_samples


samples_horizontal= deque(maxlen=SAMPLE_RATE)
samples_vertical = deque(maxlen=SAMPLE_RATE)

# Initialize serial communication
ser = serial.Serial(COM, BAUD_RATE, timeout=0.1) 

features_data = dict()

flag = 0
count = 0


        

if __name__ == "__main__":
    time.sleep(3)
    choose_val = input('1 for Model and 2 for tresholding: ')
    if int(choose_val) == 1:
        get_samples(ser,num_samples=60,num_epochs=200,lr=0.001)
        model = torch.load(f='models/lstm_model.pth')
        while True: 
            count+=1
            data = re.sub(r"""b'|'""",'',str(ser.readline().strip())).split(',')
            print_values_using_BiLSTM(data,flag,samples_vertical,model)
            
            
    elif int(choose_val) == 2:
        while True: 
            count+=1
            data = re.sub(r"""b'|'""",'',str(ser.readline().strip())).split(',')
            print_values_using_threshold(data,flag,samples_vertical)
            

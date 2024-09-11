import numpy as np
import torch
from variables import SAMPLE_RATE
from model import BiLSTMClassifier
import re
import random
import torch.nn as nn
import torch.optim as optim


def print_values_using_BiLSTM(data,flag,samples_vertical,model):
    try:
        samples_vertical.append(float(data[2]))
    except:
        print('not converted')
        samples_vertical.append(0)
    if len(samples_vertical) == SAMPLE_RATE:
        arr = np.array(list(samples_vertical))
        arr_tensor = torch.tensor(arr,dtype=torch.float32)
        arr_tensor = arr_tensor.view(1,*arr_tensor.shape,1)
        output = model(arr_tensor)
        _,predicted = torch.max(output.data,1)
        val = predicted.item()
        if val == 0 and flag == 0:
            flag = 1
            print('BLINK')
        elif val == 1 and flag == 0:
            flag = 1
            print('UP')
        elif val == 2 and flag == 0:
            flag = 1
            print('DOWN')
        elif val == 3:
            flag = 0
            print('NOTHING')
        samples_vertical.clear()
            
def get_samples(ser,num_samples,num_epochs,lr):
    data_dict = dict()
    count = 0
    samples = []
    val_1 = num_samples//4
    val_2 = num_samples//2
    val_3 = (3*num_samples)//4
    val_4 = num_samples
    while True:
        data = re.sub(r"""b'|'""",'',str(ser.readline().strip())).split(',')
        samples.append(float(data[2]))
        if len(samples) == SAMPLE_RATE:
            if count<=val_1:
                if count == 0:
                    print('Keep blinking')
                samples_ver = np.array(samples+[0])
                data_dict[count] = samples_ver
                count+=1
                print('---------')
                samples.clear()
            elif count > val_1 and count <=val_2:
                if count == val_1 + 1:
                    print('Keep looking up')
                samples_ver = np.array(samples+[1])
                data_dict[count] = samples_ver
                count+=1
                print('---------')
                samples.clear()
            elif count > val_2 and count <=val_3:
                if count == val_2+1:
                    print('Keep looking down')
                samples_ver = np.array(samples+[2])
                data_dict[count] = samples_ver
                count+=1
                print('----------')
                samples.clear()
            elif count > val_3 and count <=val_4:
                if count == val_3+1:
                    print('Do Nothing')
                samples_ver = np.array(samples+[3])
                data_dict[count] = samples_ver
                count+=1
                print('-----------')
                samples.clear()
            elif count > val_4:
                data = list(data_dict.values())
                data = [*data[0+5:val_1-5],*data[val_1+5:val_2-5],*data[val_2+5:val_3-5],*data[val_3+5:val_4-5],data[-1]]
                data = np.array(data)
                random.shuffle(data)
                X = data[:, :-1]  
                y = data[:, -1] 
                
                X = X.reshape(X.shape[0], X.shape[1], 1)
                X = torch.tensor(X, dtype=torch.float32)
                y = torch.tensor(y, dtype=torch.long)
                
                
                train_data = torch.utils.data.TensorDataset(X, y)
                
                
                train_loader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True)
                
                input_size = 1      
                hidden_size = 64
                num_layers = 2      
                num_classes = len(torch.unique(y))  
                learning_rate = lr
                num_epochs = num_epochs

                model = BiLSTMClassifier(input_size, hidden_size, num_classes, num_layers)
                criterion = nn.CrossEntropyLoss()
                optimizer = optim.Adam(model.parameters(), lr=learning_rate)
                
                device = torch.device('cpu')
                model.to(device)
                
                for epoch in range(num_epochs):
                    model.train()
                    for i, (signals, labels) in enumerate(train_loader):
                        signals = signals.to(device)
                        labels = labels.to(device)

                        outputs = model(signals)
                        loss = criterion(outputs, labels)

                        optimizer.zero_grad()
                        loss.backward()
                        optimizer.step()

                    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
                    
                torch.save(model,'models/lstm_model.pth')
                break

def print_values_using_threshold(data,flag,samples_vertical):
    try:
        samples_vertical.append(float(data[2]))
    except:
        print('not converted')
        samples_vertical.append(0)
    if len(samples_vertical) == SAMPLE_RATE:
        samples_ver = np.array(samples_vertical)
        sample_max = np.max(samples_ver)
        sample_min = np.min(samples_ver)
        if sample_max > 200 and sample_min<-300 and flag == 0:
            
            print('BLINK')
        elif sample_max > 200 and sample_min > -300  and flag == 0:
            flag =1 
            print('UP')
        elif sample_min < -200 and sample_max < 200  and flag == 0:
            flag = 1
            print('DOWN')
        else:
            flag = 0
            print('NOTHING')
        samples_vertical.clear()
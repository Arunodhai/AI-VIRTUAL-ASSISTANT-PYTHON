import json
from nltk_utils import tokenize,stem,bag_of_words
import numpy as np
import torch
import torch.nn as nn #nn module to help us in creating and training of the neural network.
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

with open('intents.json','r') as f :
    intents = json.load(f)

all_words = []
tags = []
xy = []  #to hold both tags and patterns
for intent in intents['intents'] :
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w=tokenize(pattern)
        all_words.extend(w) # we use extend() insted of append() because w is also an array.
        xy.append((w,tag))

ignore_word = ['?','!','.',',']
all_words=[stem(w) for w in all_words if w not in ignore_word]
all_words=sorted(set(all_words))
tags=sorted(set(tags))

x_train = []   #stores all the bag of words
y_train = []   #stores associate number for each tag

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words) #creates a bag
    x_train.append(bag) #stores the bag.

    label = tags.index(tag)
    y_train.append(label)

x_train = np.array(x_train)
y_train = np.array(y_train)

class ChatDataset(Dataset):            #inherits the Dataset class
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]  #returns a tuple

    def __len__(self):
        return self.n_samples

batch_size = 8      #batch size is a number of samples processed before the model is updated.
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0]) #we could use x_train[any value] because all have same length.
learning_rate = .001
num_epochs = 1000           #An epoch means training the neural network with all the training data for one cycle.

dataset = ChatDataset()  #pytorch dataset.
train_loader = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True, num_workers=0) #fetches data from a Dataset and serves the data up in batches, num_workers=2 is for multithreading/multiprocessing.

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  #checks if gpu is available.
#The CUDA is platform for parallel computing using special GPU (graphics processing unit) by NVIDIA.
# that enables dramatic increases in computing performance by harnessing the power of the graphics processing unit (GPU).

model = NeuralNet(input_size,hidden_size,output_size).to(device)


criterion = nn.CrossEntropyLoss()               #Cross-entropy loss, or log loss, measures the performance of a classification model whose output is a probability value between 0 and 1
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels= labels.to(device)

        #forward
        outputs = model(words)
        loss = criterion(outputs,labels)

        #backward and optimizer step
        optimizer.zero_grad()               #when you start your training loop, ideally you should zero out the gradients so that you do the parameter update correctly. Otherwise, the gradient would be a combination of the old gradient, which you have already used to update your model parameters, and the newly-computed gradient.
        loss.backward()                     #When you call loss.backward(), all it does is compute gradient of loss w.r.t all the parameters in loss that have requires_grad = True and store them in parameter.grad attribute for every parameter.
        optimizer.step()                    #updates all the parameters based on parameter.grad

    if (epoch+1) % 100 == 0 :
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "data.pth" #.pth for pytorch
torch.save(data, FILE)

print(f"Training complete. File saved to {FILE}")






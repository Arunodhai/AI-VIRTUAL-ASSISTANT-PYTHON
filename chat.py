import random
import json
import torch
import functionalities
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from playsound import playsound
import help
import Features

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]  #The role of the Hidden Layers is to identify features from the input data and use these to correlate between a given input and the correct output.
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]


model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name="ALFRED"
playsound("assistant_on.wav")
print("\n\n")
print(r"""                                          █████╗ ██╗     ███████╗██████╗ ███████╗██████╗      █████╗ ██╗
                                         ██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██║
                                         ███████║██║     █████╗  ██████╔╝█████╗  ██║  ██║    ███████║██║
                                         ██╔══██║██║     ██╔══╝  ██╔══██╗██╔══╝  ██║  ██║    ██╔══██║██║
                                         ██║  ██║███████╗██║     ██║  ██║███████╗██████╔╝    ██║  ██║██║
                                         ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝
                                                                                                                          """)
print("Let's chat!. Type 'quit' to exit.\nType '--help' for user manual.")
functionalities.wishMaster()
functionalities.speak(f"My name is {bot_name}. Your AI assistant.")
functionalities.speak("Let's chat!. Type 'quit' to exit.")
functionalities.speak("What can I do for you ?")

while True:
    sentence = input("\nYou: ")
    _query = sentence[:]
    if sentence == 'quit':
        playsound("assistant_off.wav")
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])                 #reshapes into : [x,x,x,x,x,x,x] format
    X = torch.from_numpy(X)                      #creating a tensor from a numpy array. A Tensor is a multidimensional NumPy array in which we store our input data.

    output = model(X)
    _, predicted = torch.max(output,dim=1)       #Returns the maximum value of all elements in the input tensor.
    tag = tags[predicted.item()]                 #Returns the value of this tensor as a standard Python number. This only works for tensors with one element.

    probs = torch.softmax(output,dim=1)         #Applies the Softmax function to an n-dimensional input Tensor rescaling them so that the elements of the n-dimensional output Tensor lie in the range [0,1] and sum to 1.
    prob = probs[0][predicted.item()]           #actual probability for this predicted tag.


    for intent in intents["intents"]:
        if tag == intent["tag"]:
            response = random.choice(intent['responses'])

            res=Features.features(_query,response)

            if res==0:
                if prob > 0.75:
                    print(f"{bot_name}: {response}")
                    functionalities.speak(response)
                    if "Well I can do so many things for you." in response:
                        help.manual()

                else:
                    print(f"{bot_name}: I don't understand...")
                    functionalities.speak("I don't understand...")










import random
import json
from gtts import gTTS
import os
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#device = 'cpu'

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

language = 'en'
FILE = "data.pth"
data = torch.load(FILE, map_location='cpu')

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "I do not understand..."


# def gtts_speech(response):
#     myobj = gTTS(text=response, lang=language, slow=False, tld='com.sg')
#     myobj.save("welcome.mp3")
#     os.system("mpg321 welcome.mp3")


# if __name__ == "__main__":
#     print("Let's chat! (type 'quit' to exit)")
#     while True:
#         # sentence = "do you use credit cards?"
#         sentence = input("You: ")
#         if sentence == "quit":
#             break

#         resp = get_response(sentence)
#         gtts_speech(resp)
#         print(resp)

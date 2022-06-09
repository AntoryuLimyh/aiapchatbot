from flask import Flask, render_template, request, jsonify
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

from chat import get_response
from gtts import gTTS


app = Flask(__name__)
language = 'en'


def gtts_speech(response):
   myobj = gTTS(text=response, lang=language, slow=True, tld='com.sg')
   myobj.save("welcome.mp3")
   os.system("mpg321 welcome.mp3")


@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
   
    response = get_response(text)
    message = {"answer": response}
    gtts_speech(response)
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)

from resemblyzer import preprocess_wav, VoiceEncoder
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    #
    return {"Exito": "Ha sido un exito"}


if __name__ == '__main__':
    app.run(debug=True)
from resemblyzer import preprocess_wav, VoiceEncoder
from flask import Flask
from pathlib import Path
import numpy as np

app = Flask(__name__)

wav_fpath1 = Path("utils/", "voice1.mp3")
wav_fpath2 = Path("utils/", "voice2.mp3")

wav1 = preprocess_wav(wav_fpath1)
wav2 = preprocess_wav(wav_fpath2)

encoder = VoiceEncoder("cpu")

speaker_wavs = [wav1, wav2]

@app.route("/verify", methods=["POST"])
def main():
    speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
    result = speaker_embeds[0] @ speaker_embeds[1]
    return {"Exito": np.float64(result)}


if __name__ == '__main__':
    app.run(debug=True)
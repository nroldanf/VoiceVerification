from resemblyzer import preprocess_wav, VoiceEncoder
from flask import Flask, request
from pathlib import Path
import numpy as np
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "utils/"

# wav_fpath1 = Path("utils/", "voice1.mp3")
# wav_fpath2 = Path("utils/", "voice2.mp3")

# wav2 = preprocess_wav(wav_fpath2)

encoder = VoiceEncoder("cpu")


@app.route("/verify", methods=["POST"])
def main():

    file_var1 = request.files["audio1"]
    file_var2 = request.files["audio2"]

    file_extension1 = file_var1.filename.split(".")[-1]
    file_extension2 = file_var2.filename.split(".")[-1]
    
    if not file_extension1 in ["mp3", "wav"] and not file_extension2 in ["mp3", "wav"]:
        return {"Error": "Formato inválido. Use mp3 o wav."}

    file_name1 = "voice1.{}".format(file_extension1)
    file_name2 = "voice2.{}".format(file_extension2)

    wav_fpath1 = os.path.join(app.config['UPLOAD_FOLDER'], file_name1)
    wav_fpath2 = os.path.join(app.config['UPLOAD_FOLDER'], file_name2)

    file_var1.save(wav_fpath1)
    file_var2.save(wav_fpath2)

    wav1 = preprocess_wav(wav_fpath1)
    wav2 = preprocess_wav(wav_fpath2)
    speaker_wavs = [wav1, wav2]

    speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
    result = speaker_embeds[0] @ speaker_embeds[1]
    return {"Exito": np.float64(result)}


if __name__ == '__main__':
    app.run(debug=True)
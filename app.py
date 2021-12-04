from flask import Flask, request, abort, send_from_directory
from transformers import AutoModelForMaskedLM, pipeline

from model.config import MASK_TOKEN, MUSIC_MLM
from model.tokenizer import tokenizer

app = Flask(__name__, static_url_path='', static_folder='ui/build')

model = AutoModelForMaskedLM.from_pretrained(MUSIC_MLM)
unmask = pipeline('fill-mask', model=model, tokenizer=tokenizer, top_k=10)


@app.route("/api/unmask", methods=['POST'])
def unmask_handler():
    data = request.get_json(force=True)
    if 'sentence' not in data:
        abort(400, "sentence required")
    sentence = str(data['sentence'])
    if sentence.count(MASK_TOKEN) != 1:
        abort(400, f"sentence must have one occurrence of {MASK_TOKEN}.")
    return {"result": unmask(sentence)}


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    app.run()

from flask import Flask, request, abort
from transformers import AutoModelForMaskedLM, pipeline

from model.tokenizer import tokenizer

MASK_TOKEN = "[MASK]"

app = Flask(__name__)

model = AutoModelForMaskedLM.from_pretrained('jacksonargo/music-production-qa')
unmask = pipeline('fill-mask', model=model, tokenizer=tokenizer)


@app.route("/api/unmask", methods=['POST'])
def unmask_handler():
    data = request.get_json(force=True)
    if 'sentence' not in data:
        abort(400, "sentence required")
    sentence = str(data['sentence'])
    if sentence.count(MASK_TOKEN) != 1:
        abort(400, f"sentence must have one occurrence of {MASK_TOKEN}.")
    return {"result": unmask(sentence)}

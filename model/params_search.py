import json

from transformers import AutoModelForMaskedLM, TrainingArguments, Trainer

from config import DISTILBERT_BASE_UNCASED
from data_collator import data_collator
from data_split import train_sentences
from tokenizer import tokenize_sentences

LEARNING_RATES = [5e-5, 3e-5, 2e-5]
BATCH_SIZES = [16, 32]
NUM_EPOCHS = [2, 3, 5]


class SearchParams:
    def __init__(self, learning_rate: float, batch_size: int, num_epoch: int):
        self.params = {"learning_rate": learning_rate, "batch_size": batch_size, "num_epoch": num_epoch}
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.num_epoch = num_epoch
        self.string = f"num_epoch={self.num_epoch}/batch_size={self.batch_size}/learning_rate={self.learning_rate}"
        self.save_model_path = f"param_search_checkpoints/{self.string}/"


params_list = []
for num_epoch in NUM_EPOCHS:
    for batch_size in BATCH_SIZES:
        for learning_rate in LEARNING_RATES:
            params_list.append(SearchParams(learning_rate, batch_size, num_epoch))

train_tokens = tokenize_sentences(train_sentences[0:100])
eval_tokens = tokenize_sentences(train_sentences[100:200])

count = 0
for params in params_list:
    count += 1
    print(f"Evaluating {params.string} ({count}/{len(params_list)}")
    trainer = Trainer(
        model=AutoModelForMaskedLM.from_pretrained(DISTILBERT_BASE_UNCASED),
        args=TrainingArguments(
            evaluation_strategy="epoch",
            num_train_epochs=params.num_epoch,
            per_device_eval_batch_size=params.batch_size,
            per_device_train_batch_size=params.batch_size,
            learning_rate=params.learning_rate,
            output_dir="param_search_training"
        ),
        train_dataset=train_tokens,
        eval_dataset=eval_tokens,
        data_collator=data_collator,
    )
    trainer.train()
    trainer.save_model(params.save_model_path)
    evaluation = trainer.evaluate()
    with open(f"{params.save_model_path}/evaluation.json", "w") as fp:
        json.dump({"params": params.params, "evaluation": evaluation}, fp)

import torch
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizer, DistilBertForMaskedLM, TrainingArguments, Trainer, \
    DataCollatorForLanguageModeling, DistilBertConfig

DISTILBERT_BASE_UNCASED = 'distilbert-base-uncased'


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)


MAX_LENGTH = 64  # up to 512
LEARNING_RATE = 0.01
WEIGHT_DECAY = 0.1
MASK_PROBABILITY = 0.15

modelConfig = DistilBertConfig(
    n_layers=2,
    n_heads=4,
    dropout=0.1,
    attention_dropout=0.1,
    activation="gelu",
)

with open('data/03_sentence_per_line/corpus.txt', encoding='utf-8') as fp:
    sentences = fp.read().split('\n')

tokenizer = DistilBertTokenizer.from_pretrained(DISTILBERT_BASE_UNCASED, model_max_length=MAX_LENGTH)
train_sentences, eval_sentences = train_test_split(sentences)
train_tokenized = Dataset(tokenizer(train_sentences, padding="max_length", truncation=True))
eval_tokenized = Dataset(tokenizer(eval_sentences, padding="max_length", truncation=True))

model = DistilBertForMaskedLM.from_pretrained(DISTILBERT_BASE_UNCASED, config=modelConfig)

training_args = TrainingArguments(
    evaluation_strategy="epoch",
    learning_rate=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY,
    output_dir="full_model_output"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=eval_tokenized,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=MASK_PROBABILITY),
)

trainer.train()

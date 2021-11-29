from sklearn.model_selection import train_test_split
from transformers import DistilBertForMaskedLM, Trainer, DataCollatorForLanguageModeling

from model.config import DISTILBERT_BASE_UNCASED, MASK_PROBABILITY, modelConfig, training_args
from model.tokenizer import tokenize_sentences, tokenizer

with open('data/03_sentence_per_line/corpus.txt', encoding='utf-8') as fp:
    sentences = fp.read().split('\n')

train_sentences, eval_sentences = train_test_split(sentences)
train_tokenized = tokenize_sentences(train_sentences)
eval_tokenized = tokenize_sentences(eval_sentences)

model = DistilBertForMaskedLM.from_pretrained(DISTILBERT_BASE_UNCASED, config=modelConfig)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized,
    eval_dataset=eval_tokenized,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=MASK_PROBABILITY),
)

trainer.train()


from transformers import TrainingArguments

BERT_BASE_UNCASED = 'bert-base-uncased'
DISTILBERT_BASE_UNCASED = 'distilbert-base-uncased'
MUSIC_MLM = 'jacksonargo/music-mlm'
MASK_TOKEN='[MASK]'
MASK_PROBABILITY = 0.15

MAX_LENGTH = 64
LEARNING_RATE = 5e-5
BATCH_SIZE = 16
NUM_EPOCH = 5

training_args = TrainingArguments(
    evaluation_strategy="epoch",
    num_train_epochs=NUM_EPOCH,
    per_device_eval_batch_size=BATCH_SIZE,
    per_device_train_batch_size=BATCH_SIZE,
    learning_rate=LEARNING_RATE,
    output_dir="full_model_output"
)

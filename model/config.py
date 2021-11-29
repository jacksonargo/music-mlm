from transformers import TrainingArguments, DistilBertConfig

DISTILBERT_BASE_UNCASED = 'distilbert-base-uncased'

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

training_args = TrainingArguments(
    evaluation_strategy="epoch",
    num_train_epochs=5,
    per_device_eval_batch_size=32,
    per_device_train_batch_size=32,
    learning_rate=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY,
    output_dir="full_model_output"
)

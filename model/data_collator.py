from transformers import DataCollatorForLanguageModeling
from tokenizer import tokenizer

MASK_PROBABILITY = 0.15

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=MASK_PROBABILITY)

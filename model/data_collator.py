from transformers import DataCollatorForLanguageModeling

from model.config import MASK_PROBABILITY
from model.tokenizer import tokenizer

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm_probability=MASK_PROBABILITY)

import torch
from transformers import DistilBertTokenizer

from model.config import DISTILBERT_BASE_UNCASED, MAX_LENGTH


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)


tokenizer = DistilBertTokenizer.from_pretrained(DISTILBERT_BASE_UNCASED, model_max_length=MAX_LENGTH)


def tokenize_sentences(sentences):
    return Dataset(tokenizer(sentences, padding="max_length", truncation=True, return_special_tokens_mask=True))

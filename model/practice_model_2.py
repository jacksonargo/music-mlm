import torch
from tqdm import tqdm  # for our progress bar
from transformers import AdamW
from transformers import BertTokenizer, BertForMaskedLM

MASK_PROBABILITY = 0.15
MAX_SENTENCE_LENGTH = 512
BATCH_SIZE = 16

TOKEN_CLS = 101
TOKEN_SEP = 102
TOKEN_MASK = 103
TOKEN_PAD = 0


class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings.input_ids)


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

with open('practice_data/content.txt', 'r') as fp:
    # this data has every sentence on a new line,
    inputSentences = fp.read().split('\n')  # so we split by new line

inputTensors = tokenizer(
    inputSentences,
    return_tensors='pt',
    max_length=MAX_SENTENCE_LENGTH,
    truncation=True,
    padding='max_length')

inputTensors['labels'] = inputTensors.input_ids.detach().clone()

maskingTensors = (torch.rand(inputTensors.input_ids.shape) < MASK_PROBABILITY) * \
                 (inputTensors.input_ids != TOKEN_CLS) * \
                 (inputTensors.input_ids != TOKEN_SEP) * \
                 (inputTensors.input_ids != TOKEN_PAD)

maskedIndices = [torch.flatten(mask.nonzero()).tolist() for mask in maskingTensors]
for i in range(inputTensors.input_ids.shape[0]):
    inputTensors.input_ids[i, maskedIndices[i]] = TOKEN_MASK

dataset = Dataset(inputTensors)

dataLoader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)
model.train()

optimizer = AdamW(model.parameters(), lr=5e-5)
epochs = 2
for epoch in range(epochs):
    loop = tqdm(dataLoader, leave=True)
    for batch in loop:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(
            input_ids,
            attention_mask=attention_mask,
            labels=labels)

        loss = outputs.loss
        loss.backward()
        optimizer.step()
        loop.set_description(f'Epoch {epoch}')
        loop.set_postfix(loss=loss.item())

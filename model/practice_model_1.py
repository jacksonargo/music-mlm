import torch
from transformers import BertTokenizer, BertForMaskedLM

text = ("After Abraham Lincoln won the November 1860 presidential "
        "election on an anti-slavery platform, an initial seven "
        "slave states declared their secession from the country "
        "to form the Confederacy. War broke out in April 1861 "
        "when secessionist forces attacked Fort Sumter in South "
        "Carolina, just over a month after Lincoln's "
        "inauguration.")

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForMaskedLM.from_pretrained('bert-base-uncased')

# TODO: refactor to inputTensors
inputTensors = tokenizer(text, return_tensors='pt')
inputTensors['labels'] = inputTensors.input_ids.detach().clone()

MASK_PROBABILITY = 0.15
TOKEN_CLS = 101
TOKEN_SEP = 102
TOKEN_MASK = 103

maskingTensor = (torch.rand(inputTensors.input_ids.shape) < MASK_PROBABILITY) * \
                (inputTensors.input_ids != TOKEN_CLS) * \
                (inputTensors.input_ids != TOKEN_SEP)

maskedIndices = torch.flatten((maskingTensor[0]).nonzero()).tolist()
inputTensors.input_ids[0, maskedIndices] = TOKEN_MASK
outputTensors = model(**inputTensors)
outputTensors.keys()

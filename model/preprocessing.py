import io
import os
import typing

import nltk.data

sentenceTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def concat_files(srcpath: str, destpath: str):
    srcpath = os.fsencode(srcpath)
    destpath = os.fsencode(destpath)
    os.makedirs(destpath, exist_ok=True)

    output_path = os.path.join(destpath, os.fsencode("corpus.txt"))
    with open(output_path, "w", encoding='utf-8') as writer:
        for filePath in os.listdir(srcpath):
            file_name = os.path.basename(os.fsdecode(filePath))
            if not file_name.endswith(".txt"):
                continue
            with open(os.path.join(srcpath, filePath), encoding='utf-8') as reader:
                writer.write(reader.read())


def extract_pdf_text(fp: io.FileIO) -> str:
    "\n\n".join(pdftotext.PDF(fp))


def sentence_per_line(text: str) -> str:
    result = sentenceTokenizer.tokenize(text)
    return "\n".join([k.replace("\n", " ") for k in result])


def chunk(text: str, size: int) -> [str]:
    cur_chunk = ""
    result = []
    split = text.split("\n")
    for line in split:
        if len(bytes(cur_chunk, 'utf-8')) + len(bytes(line, 'utf-8')) > size:
            result.append(cur_chunk)
            cur_chunk = ""
        cur_chunk += line
    result.append(cur_chunk)
    return result


def transform_corpus(srcpath: str, destpath: str, fn: typing.Callable[[str], str]):
    srcpath = os.fsencode(srcpath)
    destpath = os.fsencode(destpath)
    os.makedirs(destpath, exist_ok=True)
    with open(os.path.join(destpath, os.fsencode("corpus.txt")), "w", encoding='utf-8') as writer:
        with open(os.path.join(srcpath, os.fsencode("corpus.txt")), encoding='utf-8') as reader:
            writer.write(fn(reader.read()))


concat_files(
    srcpath="../data/01_extraction",
    destpath="../data/02_concatenate")

transform_corpus(
    srcpath="../data/02_concatenate",
    destpath="../data/03_sentence_per_line",
    fn=sentence_per_line)

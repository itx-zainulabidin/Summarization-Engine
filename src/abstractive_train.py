from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import load_dataset
import os

MODEL = os.environ.get('SUMMARIZER_MODEL', 'facebook/bart-large')
DATA_TRAIN = os.environ.get('TRAIN_DATA', 'data/train.jsonl')
DATA_VAL = os.environ.get('VAL_DATA', 'data/val.jsonl')

def preprocess(example, tokenizer, max_input=1024, max_output=256):
    inputs = example.get('instruction','') + '\n\n' + example.get('input','')
    model_inputs = tokenizer(inputs, max_length=max_input, truncation=True)
    labels = tokenizer(example['output'], max_length=max_output, truncation=True)
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

def main():
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    ds = load_dataset('json', data_files={'train':DATA_TRAIN, 'validation':DATA_VAL})
    ds = ds.map(lambda ex: preprocess(ex, tokenizer), batched=False, remove_columns=ds['train'].column_names)
    training_args = TrainingArguments(output_dir='models/abstractive', per_device_train_batch_size=1, num_train_epochs=1, fp16=False)
    trainer = Trainer(model=model, args=training_args, train_dataset=ds['train'], eval_dataset=ds['validation'])
    trainer.train()
if __name__ == '__main__':
    main()

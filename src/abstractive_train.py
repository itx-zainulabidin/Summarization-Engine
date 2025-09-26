from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments
from datasets import load_dataset
import os

MODEL = os.environ.get('SUMMARIZER_MODEL', 'facebook/bart-large')
DATA_TRAIN = os.environ.get('TRAIN_DATA', 'data/train.jsonl')
DATA_VAL = os.environ.get('VAL_DATA', 'data/val.jsonl')

def preprocess(example, tokenizer, max_input=1024, max_output=256):
    """
    Preprocess a single example for summarization fine-tuning.

    Args:
        example (dict): One record from the dataset.
            Expected keys:
                - 'instruction': Task description (optional)
                - 'input': Source text to summarize
                - 'output': Reference summary
        tokenizer (AutoTokenizer): Hugging Face tokenizer
        max_input (int): Maximum token length for input text
        max_output (int): Maximum token length for target summary

    Returns:
        dict: Encoded input and labels for the model.
    """
    
    inputs = example.get('instruction','') + '\n\n' + example.get('input','')
    model_inputs = tokenizer(inputs, max_length=max_input, truncation=True)
    labels = tokenizer(example['output'], max_length=max_output, truncation=True)
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

def main():
    """
    Main training loop for abstractive summarization.
    Loads tokenizer, model, dataset, applies preprocessing, and trains with Hugging Face Trainer.
    """
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL)
    ds = load_dataset('json', data_files={'train':DATA_TRAIN, 'validation':DATA_VAL})
    ds = ds.map(lambda ex: preprocess(ex, tokenizer), batched=False, remove_columns=ds['train'].column_names)
    training_args = TrainingArguments(output_dir='models/abstractive', per_device_train_batch_size=1, num_train_epochs=1, fp16=False)
    trainer = Trainer(model=model, args=training_args, train_dataset=ds['train'], eval_dataset=ds['validation'])
    trainer.train()
if __name__ == '__main__':
    main()

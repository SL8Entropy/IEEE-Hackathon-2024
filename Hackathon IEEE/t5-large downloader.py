from transformers import T5ForConditionalGeneration, T5Tokenizer

# Download and cache the model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-large')
tokenizer = T5Tokenizer.from_pretrained('t5-large')

# Save them locally
model.save_pretrained('./t5-large-model')
tokenizer.save_pretrained('./t5-large-tokenizer')

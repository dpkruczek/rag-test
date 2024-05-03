from transformers import AutoModel, AutoTokenizer

model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Specify your save directory
save_directory = "./"

# Save the model and the tokenizer
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)
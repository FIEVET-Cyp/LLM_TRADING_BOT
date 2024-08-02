from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch    

model_path = 'path_to_save_model'
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()  # Set the model to evaluation mode

# Setup device for using GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

tokenizer = AutoTokenizer.from_pretrained('huawei-noah/TinyBERT_General_4L_312D')

def predict_score(article):
    # Tokenize the input article
    inputs = tokenizer(article, return_tensors="pt", max_length=10, truncation=True, padding=True)
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    # Perform prediction
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
        predicted_score = outputs.logits.squeeze().item()

    return predicted_score

# Example use of the function
article_example = "This is an example article for testing the model's prediction capability."
predicted_score_example = predict_score(article_example)
print("Predicted Score:", predicted_score_example)
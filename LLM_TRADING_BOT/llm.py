from transformers import BertTokenizer, BertForSequenceClassification
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, RandomSampler, TensorDataset
import json

# Load data from JSON files
with open('date_score.json', 'r') as file:
    date_score = json.load(file)
with open('article_data.json', 'r') as file:
    article_data = json.load(file)

# Prepare data lists for articles and scores
articles = []
scores = []
for key, value in article_data.items():
    if key in date_score:
        articles.extend(value)
        scores.extend([date_score[key]] * len(value))

# Convert scores to tensors
scores_tensor = torch.tensor(scores).float()

# Tokenization with a maximum length
max_length = 2  # Set a reasonable maximum length
tokenizer = AutoTokenizer.from_pretrained('huawei-noah/TinyBERT_General_4L_312D')
encoded_inputs = tokenizer(articles, max_length=max_length, padding=True, truncation=True, return_tensors='pt')

# Attention masks and data splits
attention_masks = encoded_inputs['attention_mask']
train_inputs, validation_inputs, train_labels, validation_labels, train_masks, validation_masks = train_test_split(
    encoded_inputs['input_ids'], scores_tensor, attention_masks, random_state=42, test_size=0.9999)  # Adjusted test size

# DataLoader setup
train_data = TensorDataset(train_inputs, train_masks, train_labels)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=2)  # Adjusted batch size

# Model setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForSequenceClassification.from_pretrained('huawei-noah/TinyBERT_General_4L_312D', num_labels=1)
model.to(device)

# Model training
model.train()
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)
for epoch in range(1):  # Number of epochs
    for step, batch in enumerate(train_dataloader):
        b_input_ids, b_attention_mask, b_labels = tuple(t.to(device) for t in batch)

        # Clear previous gradients
        model.zero_grad()

        # Perform a forward pass and calculate loss
        outputs = model(b_input_ids, attention_mask=b_attention_mask, labels=b_labels.unsqueeze(1))

        # Backward pass to adjust weights
        loss = outputs.loss
        loss.backward()

        # Update weights
        optimizer.step()

        # Print loss information
        print(f"Epoch {epoch}, Step {step}, Loss {loss.item()}")

    # Optionally save the model after every epoch
    model.save_pretrained(f'model_epoch_{epoch}')

# Save the model and optimizer state after training is complete
model.save_pretrained('path_to_save_model')
torch.save(optimizer.state_dict(), 'path_to_save_model/optimizer_state.pth')

# Evaluation
model.eval()
with torch.no_grad():
    output = model(validation_inputs.to(device))
    predicted_scores = output.logits.squeeze()
    print("Predicted scores:", predicted_scores)

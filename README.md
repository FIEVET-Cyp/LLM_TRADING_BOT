# LLM-TRADING-BOT

This bot utilizes ALGOGENE and KRAKEN for data retrieval and KRAKEN for executing trades.

## Overview

The primary objective of this algorithm is to use a BERT Classifier to analyze news articles and predict the direction of Bitcoin (BTC) prices. The system assigns scores to articles based on subsequent BTC price movements, allowing the classifier to learn and make predictions.

## Methodology

### Data Collection and Scoring:

1. **Data Collection**:
   - 27,000 articles from the past year are collected.

2. **Scoring**:
   - Each article is assigned a score:
     - If the BTC price increased after the publication of the article, the article receives a positive score.
     - If the BTC price decreased, the article receives a negative score.

### Model Training:

- The scored articles are used to train a BERT Classifier. This model learns to associate textual content with the subsequent BTC price movement.

### Prediction and Trading:

- The trained model is used to evaluate new news articles.
- Based on the model's output, indicating whether BTC prices are likely to rise or fall, the bot makes buy or sell decisions.

## Configuration

- **ALGOGENE**: Used for data retrieval.
- **KRAKEN**: Used for data retrieval and executing trades.

## Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/FIEVET-Cyp/LLM-TRADING-BOT.git
   cd LLM-TRADING-BOT

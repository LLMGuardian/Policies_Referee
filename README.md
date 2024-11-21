# Policies_Referee

Policies_Referee is a plug-in that uses static, manually crafted rules and patterns to act as a pre-display filter between user inputs and a large language model (LLM). The system analyzes the input prompts, checking for benign or malicious patterns. If the input is determined to be safe, it will be enriched with a set of pre-defined templates containing reminder rules before being passed to the LLM. The LLM then classifies the input into two categories: 0 for safe and 1 for malicious.

This plug-in is connected to the central unit LLMGuardian as a component to block and filter user inputs.

## Features

- Input validation using predefined static rules and pattern matching.
- Enrichment of safe prompts with reminder templates.
- Classification of inputs as safe (0) or malicious (1) using a fine-tuned LLM model.
- Designed to work seamlessly with any LLM that can be integrated with plug-ins. For this stage, it was only tested with the model llama3.1.

## Plugin Testing Dataset

This repository contains a custom dataset created to evaluate the plugin's performance in differentiating between benign and malicious prompts. It was created by combining two datasets:

### 1. Malicious Prompts Dataset

The malicious data was sourced from the Anthropic/hh-rlhf dataset. This dataset contains human-generated and annotated dialogues, aimed at identifying and testing harmful responses from AI systems. The dialogues are derived from red teaming efforts and are annotated to indicate harmfulness levels.

**Key Features Used:**
- `transcript`: A textual transcript of a conversation between a human adversary (red team member) and an AI assistant.
- `min_harmlessness_score_transcript`: A real value score indicating the harmlessness of the AI assistant’s response, with lower scores being more harmful.

**Data Processing Steps:**
- Filtered the dataset to select the 100 most harmful transcripts, based on the lowest `min_harmlessness_score_transcript`.
- Extracted only the initial request made by the human adversary in each transcript to focus on the potentially malicious prompts.

### 2. Benign Prompts Dataset

The benign prompts were obtained from the Prompt Injection Benign Evaluation Framework dataset available on Kaggle. Specifically, the `benign_deepset.csv` file was used, containing various non-malicious, benign prompts.

**Data Processing Steps:**
- Selected benign prompts from `benign_deepset.csv`.
- Matched the number of benign prompts to the 100 malicious prompts to ensure a balanced dataset.

### 3. Final Dataset Preparation

- Combined the malicious and benign datasets into a single dataset.
- The combined dataset was shuffled randomly to ensure a mixed distribution of benign and malicious prompts, avoiding any ordering biases.

## Acknowledgments

- **Malicious Data Source**: Anthropic/hh-rlhf dataset, focusing on human-generated red team dialogues to identify harmful AI responses.
- **Benign Data Source**: Prompt Injection Benign Evaluation Framework, utilizing the `benign_deepset.csv`.

## Get Started

Follow these steps to get the application up and running:

```bash
git clone https://github.com/LLMGuardian/Fine_Tuned_LLM_App.git
pip install -r requirements.txt
python src/app.py

import torch
from transformers import Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
from typing import Dict, List
import pandas as pd

class ModelTrainer:
    """Professional model trainer for resume-worthy feature"""
    
    def __init__(self):
        self.training_history = []
    
    def create_training_data(self) -> pd.DataFrame:
        """Create comprehensive training dataset"""
        training_data = [
            # True statements
            {"text": "The Earth orbits the Sun", "label": "true"},
            {"text": "Water boils at 100 degrees Celsius at sea level", "label": "true"},
            {"text": "COVID-19 vaccines are effective at preventing severe illness", "label": "true"},
            {"text": "Climate change is supported by scientific consensus", "label": "true"},
            {"text": "The Great Wall of China is visible from space", "label": "false"},
            
            # False statements
            {"text": "The Earth is flat", "label": "false"},
            {"text": "Vaccines cause autism", "label": "false"},
            {"text": "Moon landing was faked", "label": "false"},
            {"text": "5G towers spread COVID-19", "label": "false"},
            {"text": "Chemtrails are used for weather modification", "label": "false"},
            
            # Misleading statements
            {"text": "BREAKING: Secret cure for cancer discovered", "label": "misleading"},
            {"text": "They don't want you to know this truth", "label": "misleading"},
            {"text": "This one trick will make you rich overnight", "label": "misleading"},
            {"text": "Doctors hate this simple weight loss method", "label": "misleading"},
            
            # Unverifiable
            {"text": "Aliens built the pyramids", "label": "unverifiable"},
            {"text": "Bigfoot lives in the Pacific Northwest", "label": "unverifiable"},
        ]
        
        return pd.DataFrame(training_data)
    
    def compute_metrics(self, eval_pred):
        """Compute metrics for model evaluation"""
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        
        precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average='weighted')
        accuracy = accuracy_score(labels, predictions)
        
        return {
            'accuracy': accuracy,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    
    def train_model(self, model, tokenizer, output_dir="./models/fine-tuned"):
        """Train model with professional setup"""
        dataset = self.create_training_data()
        
        # Tokenize dataset
        def tokenize_function(examples):
            return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)
        
        tokenized_datasets = dataset.map(tokenize_function, batched=True)
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=10,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./logs',
            logging_steps=10,
            evaluation_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
            metric_for_best_model="accuracy",
        )
        
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_datasets,
            eval_dataset=tokenized_datasets,
            compute_metrics=self.compute_metrics,
        )
        
        # Log training start
        self.training_history.append({
            'timestamp': str(pd.Timestamp.now()),
            'model': model.config.model_type,
            'dataset_size': len(dataset),
            'status': 'started'
        })
        
        # Train model
        trainer.train()
        
        # Save model
        trainer.save_model()
        
        # Log training completion
        self.training_history[-1]['status'] = 'completed'
        self.training_history[-1]['final_metrics'] = trainer.evaluate()
        
        return trainer
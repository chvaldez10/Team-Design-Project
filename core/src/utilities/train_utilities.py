import torch
import wandb
import torch.nn as nn
import pytorch_lightning as pl
import os
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from src.dataset.breathing_dataset import BreathingDataset
from src.deep_learning_models.three_d_cnn import Basic3DCNN

def train_validate(model: Basic3DCNN, train_loader: BreathingDataset, val_loader: BreathingDataset, epochs: int, learning_rate: float, best_model_path: str, device: torch.device, verbose: bool = True) -> None:
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    # optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=0.0001)
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.9)
    best_loss = 1e+20

    early_stop_callback = EarlyStopping(
        monitor='val_loss',  # Monitor validation loss
        patience=5,           # Number of consecutive epochs without improvement
        verbose=True,
        mode='min'
    )

    wandb.init(
        project="enel-645-garbage-classifier",
        name="test-run",
        config={"learning_rate": 0.02, "architecture": "efficientNet_b4", "dataset": "CVPR_2024_dataset", "epochs": 12}
    )

    # Initialize PyTorch Lightning Trainer
    trainer = pl.Trainer(callbacks=[early_stop_callback]) if torch.cuda.is_available() else pl.Trainer()

    for epoch in range(epochs):
        model.train()
        train_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            inputs = inputs.permute(0, 2, 1, 3, 4)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        if verbose:
            print(f'Epoch {epoch + 1}, Train loss: {train_loss / len(train_loader):.3f}', end=' ')

        scheduler.step()

        model.eval()
        val_loss = 0.0
        val_corrects = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data)
        
        val_loss /= len(val_loader)
        val_accuracy = val_corrects.double() / len(val_loader.dataset)
        wandb.log({"val_loss": val_loss, "val_accuracy": val_accuracy})

        print(f'Epoch {epoch+1}, Train Loss: {val_loss / len(train_loader)}, Val Loss: {val_loss}, Val Accuracy: {val_accuracy}')

    if verbose:
        print('Finished Training')

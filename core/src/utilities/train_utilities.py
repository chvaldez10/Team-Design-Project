import os
import torch
import wandb
import torch.nn as nn
import torch.optim as optim
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from src.dataset.breathing_dataset import BreathingDataset
from src.deep_learning_models.three_d_cnn import Basic3DCNN


def train_epoch(model, train_loader, criterion, optimizer, device):
    """
    Train the model for one epoch.
    """
    model.train()
    total_loss = 0.0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions for model
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    return total_loss / len(train_loader)


def validate_model(model, val_loader, criterion, device):
    """
    Validate the model performance on the validation dataset.
    """
    model.eval()
    total_loss = 0.0
    total_corrects = 0

    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            inputs = inputs.permute(0, 2, 1, 3, 4)  # Adjust dimensions for model
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            total_corrects += torch.sum(preds == labels.data).item()
    
    avg_loss = total_loss / len(val_loader)
    accuracy = total_corrects / len(val_loader.dataset)
    
    return avg_loss, accuracy


def train_validate(model, train_loader, val_loader, epochs, learning_rate, best_model_path,
                   device, patience=3, verbose=True):
    """
    Train and validate the model.
    """
    model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.9)
    best_val_loss = float('inf')
    early_stop_counter = 0

    wandb.init(project="3d-cnn", name="detecting-breathing-patterns", config={"learning_rate": learning_rate, "architecture": "3d-cnn", "dataset": "breathing_dataset", "epochs": epochs})

    os.makedirs(os.path.dirname(best_model_path), exist_ok=True)

    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_accuracy = validate_model(model, val_loader, criterion, device)
        scheduler.step()

        if verbose:
            print(f'Epoch {epoch + 1}, Train Loss: {train_loss:.3f}, Val Loss: {val_loss:.3f}, Val Accuracy: {val_accuracy:.3f}')
        
        wandb.log({"epoch": epoch + 1, "train_loss": train_loss, "val_loss": val_loss, "val_accuracy": val_accuracy})

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            early_stop_counter = 0
            torch.save(model.state_dict(), best_model_path)
        else:
            early_stop_counter += 1
            if early_stop_counter >= patience:
                print("Early stopping triggered.")
                break

    if verbose:
        print("Finished Training.")

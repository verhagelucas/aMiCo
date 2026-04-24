import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import os
import numpy as np
from torchvision import models, transforms

# --- Step 1: Dataset with automatic resizing and transforms ---
class ImageFolderDataset(Dataset):
    def __init__(self, root_dir, image_size=(224,224), transform=None): #FIXME any reason why 224?
        self.root_dir = root_dir
        self.image_size = image_size
        self.transform = transform
        self.samples = []
        self.class_to_idx = {}
        classes = sorted(os.listdir(root_dir))
        for idx, class_name in enumerate(classes):
            self.class_to_idx[class_name] = idx
            class_dir = os.path.join(root_dir, class_name)
            for img_name in os.listdir(class_dir):
                self.samples.append((os.path.join(class_dir, img_name), idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        #print("read image", img_path)
        image = Image.open(img_path).convert("L")       #FIXME why RGB needed?
        if self.transform:
            image = self.transform(image)
        else:
            # Default transform: resize + tensor + normalize
            transform_default = transforms.Compose([
                transforms.Resize(self.image_size),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],    #FIXME why these 3 values specifically?
                                     std=[0.229, 0.224, 0.225]) 
            ])
            image = transform_default(image)
        return image, label

# --- Step 2: Prepare datasets and dataloaders ---
num_epochs = 4
datadir = "Mitosis Detection/DL/data-mitosis/topleft"
#datadir = "data-pro-meta-inter"
#datadir = "data-cat-dog"
#datadir = "data-hor-vert"
#datadir = "data-platelets"

print("datadir = " + datadir)

train_dataset = ImageFolderDataset(datadir + r'/train_topleft', image_size=(512,512))
val_dataset = ImageFolderDataset(datadir + r'/val_topleft', image_size=(512,512))

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Step 3: Load pre-trained ResNet18 ---
num_classes = len(train_dataset.class_to_idx)
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
# Replace final layer
model.fc = nn.Linear(model.fc.in_features, num_classes) #FIXME if you are replacing the final layer why are you using in_features
model = model.to(device)

criterion = nn.CrossEntropyLoss()   #TODO adjust weights
optimizer = optim.Adam(model.parameters(), lr=0.0005)

# --- Step 4: Training loop with validation ---
for epoch in range(num_epochs):
    print("ecpoch: ", epoch)
    # Training
    print("training started")
    model.train()
    running_loss = 0.0
    progress_counter = 0
    for images, labels in train_loader:
        print(progress_counter)
        progress_counter +=1
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()


    print("validation starting")
    # Validation
    model.eval()
    correct = 0
    total = 0
    val_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    train_loss_avg = running_loss / len(train_loader)
    val_loss_avg = val_loss / len(val_loader)
    val_accuracy = correct / total

    print(f"Epoch [{epoch+1}/{num_epochs}] "
          f"Train Loss: {train_loss_avg:.4f} "
          f"Val Loss: {val_loss_avg:.4f} "
          f"Val Accuracy: {val_accuracy:.4f}")
    
    print("saving model-" + str(epoch+1) + "...")
    torch.save(model.state_dict(), r"C:\Users\Student\Desktop\MmM\Code\Microscope_Control\Mitosis Detection\DL\simple_python_classifier\model-" + str(epoch+1) + r".pt2")



"""
# PREDICT

num_classes = len(train_dataset.class_to_idx)
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load("model-1.pt2"))
model = model.to(device)

# --- Step 5: Classify a new image ---
def classify_image(image_path, model, class_to_idx, image_size=(224,224)):
    model.eval()
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    image = transform(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        pred = torch.argmax(output, dim=1).item()
    idx_to_class = {v:k for k,v in class_to_idx.items()}
    return idx_to_class[pred]


print(classify_image(datadir + '/val/beermug/010_0001.jpg', model, train_dataset.class_to_idx))
"""

# --- Step 5: Classify a new image ---
def classify_image(image_path, model, class_to_idx, image_size=(512,512)):
    model.eval()
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    image = transform(Image.open(image_path).convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        pred = torch.argmax(output, dim=1).item()
    idx_to_class = {v:k for k,v in class_to_idx.items()}
    return idx_to_class[pred]




classes = sorted(os.listdir(datadir + '/val'))
for cls in classes:
    print("cls =", cls)
    print("predict in predict val/" + cls)
    predict_dir = os.path.join(datadir, 'val', cls)
    predict_files = sorted([f for f in os.listdir(predict_dir) if os.path.isfile(os.path.join(predict_dir, f))])
    for filename in predict_files:
        cls = classify_image(os.path.join(predict_dir, filename), model, train_dataset.class_to_idx)
        print(filename, cls)


#print("predict in predict dir")
#predict_dir = os.path.join(datadir, 'predict')
#predict_files = sorted([f for f in os.listdir(predict_dir) if os.path.isfile(os.path.join(predict_dir, f))])
#for filename in predict_files:
#    cls = classify_image(os.path.join(predict_dir, filename), model, train_dataset.class_to_idx)
#    print(filename, cls)



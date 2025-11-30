# QR Classification Transformer

## Project Motivation
QR codes have become widely embedded in everyday life, facilitating everything from restaurant menus to mobile payments. Unfortunately, this convenience has opened a vector for attackers to embed malicious URLs into QR codes. These codes often appear **nearly identical** to legitimate ones, and unlike traditional links, they provide no immediate visual cues regarding their destination. These combined characteristics make it difficult to assess the safety of QR codes before scanning.

Current mitigation strategies typically rely on:
1.  **Visual Inspection:** Checking for pixelation or blur (often ineffective against well-generated malicious codes).
2.  **Decoding:** Using third-party scanner apps to extract and analyze the URL (which can be risky if the scanner lacks robust sandboxing).

Our project aims to address this gap by applying a Transfer Learning technique on a **Vision Transformer (ViT)** capable of determining whether a QR code is malicious solely from the QR image itself.

Utilizing a binary classification setup (**0 = malicious/phishing**, **1 = legitimate**), we evaluate whether a computer-vision-based transformer can learn specific features (such as alignment artifacts, noise patterns, or structural anomalies) within the QR image that correlate with malicious intent. A secondary goal is to interpret the model’s learned features, providing insight into the visual cues the model associates with malicious QR patterns.

## Dataset Overview
We utilize the **PhiUSIIL Phishing URL Dataset**, a curated collection of approximately **240,000 URLs** classified as either phishing or legitimate. The original dataset contains 50+ features extracted from webpage source code and URL strings.

### Data Preprocessing & Generation
To convert this NLP-based dataset into a Computer Vision task, we introduced a custom preprocessing pipeline using the script `QR_Translator.ipynb`:
1.  **Input:** URL strings from the PhiUSIIL dataset.
2.  **Transformation:** A Python `qrcode` translator converts each URL into a QR code.
3.  **Output:** A **256x256 RGB image** for every data point to ensure consistent input shape.
4.  **Filtering:** A small fraction of URLs (<1%) were too large to be encoded into standard QR versions and were omitted.
 
#
This resulted in a parallel dataset of QR images aligned with the original ground-truth labels. These images provide the structured visual representation required for our Vision Transformer to analyze potential correlations between visual patterns and malicious intent.

## Model Architecture
We selected the **Vision Transformer (ViT)** architecture because QR codes are highly structured, geometric, and binary in nature. Unlike Convolutional Neural Networks (CNNs), which process images locally, Transformers utilize **Self-Attention mechanisms** to consider global context immediately. This is crucial for detecting subtle structural discrepancies (e.g., alignment issues, tampering artifacts) that might indicate a malicious code.

### Pre-Trained Backbone
* **Model:** `google/vit-base-patch16-224`
* **Pre-training:** ImageNet-21k (approx. 86M parameters).
* **Input Handling:** Partitions images into 16x16 patches.
* **Transfer Learning:** We leverage the pre-trained feature extractor and fine-tune it for our binary classification task.

## Training Setup
Our training pipeline is implemented in `ViT_Training.ipynb` (and optimized for Colab in `Colab_Training.ipynb`):

### 1. Preprocessing
* **Encoding:** URL dataset converted to QR codes.
* **Formatting:** QR codes converted to 3-channel RGB images and tensors.
* **Labeling:** `0` (Malicious), `1` (Legitimate).

### 2. Dataset Split
* **Ratio:** 80/20 split.
* **Training Set:** ~189,000 samples.
* **Testing Set:** ~47,000 samples.

### 3. Model Fine-Tuning
To preserve learned representations and minimize overfitting given the dataset size and computational constraints, we employed a **feature extraction** strategy:
* **Frozen Layers:** All 12 encoding layers of the ViT backbone.
* **Trainable Layers:** Only the final classification head.

**Hyperparameters:**
* **Optimizer:** AdamW
* **Learning Rate:** 0.0001
* **Batch Size:** 16
* **Epochs:** 40
* **Activation:** GELU (Gaussian Error Linear Unit) for hidden layers.
* **Loss Function:** Cross-Entropy Loss (applied to raw logits; probabilities derived internally).

## Evaluation Metrics
We evaluate the fine-tuned Vision Transformer using standard binary classification metrics:
* **Accuracy**
* **Precision & Recall**
* **F1-Score**
* **Confusion Matrix**
* **Classification Report**

## Repository Structure 
* `QR_Translator.ipynb`: Generates QR code images from the raw URL dataset.
* `ViT_Training.ipynb`: Main notebook for loading data, preprocessing, fine-tuning the ViT model, and evaluating performance.
* `Colab_Training.ipynb`: Adapted training notebook optimized for Google Colab environments.
* `training_logs`: A directory containing training
* `colab_setup.png`: Image illustrating Colab directory setup
* `ViT_Explainability`:

## Results and Visualizations


## Limitations and Future Work


## References
* **Dataset:** PhiUSIIL Phishing URL Dataset.
* **Transformer Architecture:** Vaswani et al. (2017). *"Attention Is All You Need"*. Google Brain.
* **Vision Transformer:** Dosovitskiy et al. (2020). *"An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"*.
# LEAFFLICTION

## Part 4: Classification

### Data Loading and Preprocessing:
- Use a program to load the images from the directory you specified.
- Use the augmented and transformed images from Parts 2 and 3 to create a more balanced and diverse dataset. This balanced dataset will help improve model accuracy and prevent overfitting on any specific plant type or disease.
- Preprocess the images by resizing them to a uniform size (e.g., 128x128 or 224x224 pixels) for consistency, as many deep learning models require fixed input dimensions.
- Normalize pixel values to a range that deep learning models expect (often between 0 and 1).

### Training the Model:

- Split your dataset into training, validation, and test sets (e.g., 70% training, 15% validation, 15% testing).
- Fine-tune the model using the training set and validate on the validation set to monitor performance and avoid overfitting.
- Use metrics like accuracy and loss to evaluate model performance. If your dataset is imbalanced, consider using other metrics like F1-score or recall to get a more accurate picture of the model's effectiveness across classes.

### Saving the Model and Augmented Images:

- Once the model is trained, save it along with the augmented and transformed images into a .zip file for easy sharing or deployment.
- You can save your trained model using libraries like TensorFlow's tf.saved_model format, or PyTorch's torch.save function.

### Prediction Program:

- Write a separate program that loads the trained model and takes a path to an image as input.
- Display both the original and transformed images, if possible, to visualize what the model "sees."
- Run the image through the model to predict the type of disease. Display the predicted disease type as output.
- If you want to visualize which areas of the image the model is focusing on, you could use Grad-CAM (Gradient-weighted Class Activation Mapping), a technique available in many libraries, to highlight areas in the image that influence the model's prediction.

### Recommended Libraries

- [PyTorch](https://pytorch.org/docs/stable/index.html): PyTorch is a flexible deep learning library that makes it straightforward to define and train neural networks from scratch. It provides complete control over model architecture, optimization, and training loops, which is especially useful when building a custom model without pre-trained weights.
Use torchvision.transforms for data augmentation and transformation, torch.utils.data for data loading and batching, and torch.nn to create your CNN model.

- [fastai](https://fastai1.fast.ai/vision.html#Images): Fastai is a high-level library built on top of PyTorch, designed to simplify training neural networks. It’s especially well-suited for computer vision and can be used to create and train models without relying on pre-trained weights.
Fastai’s vision module offers tools for building custom CNNs, managing image datasets, and data augmentation through DataBlock and DataLoader.
Fastai’s high-level API is user-friendly, offering functions like Learner to simplify model training, metrics calculation, and evaluation.

- [TensorFlow/Keras](https://fastai1.fast.ai/vision.html#Images): TensorFlow/Keras still offers a flexible way to define CNNs and train them from scratch. The Sequential API or functional API in Keras is straightforward and allows you to build and train custom models.
Use Keras’s ImageDataGenerator for image data augmentation, but without loading weights from pre-trained models.

- scikit-learn: For data splitting, calculating metrics, and managing basic utilities in your workflow.
train_test_split for splitting data, classification_report and confusion_matrix for evaluation.

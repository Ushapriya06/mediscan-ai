import numpy as np
import os
import pickle
from PIL import Image

def preprocess_image(image_file):
    img = Image.open(image_file).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def train_xray_model():
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
    from tensorflow.keras.models import Model
    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    train_dir = "data/chest_xray/train"
    if not os.path.exists(train_dir):
        return None, 0.0

    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=10,
        zoom_range=0.1,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_gen = datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode="binary",
        subset="training"
    )

    val_gen = datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode="binary",
        subset="validation"
    )

    base_model = MobileNetV2(
        weights="imagenet",
        include_top=False,
        input_shape=(224, 224, 3)
    )
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    predictions = Dense(1, activation="sigmoid")(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        train_gen,
        epochs=5,
        validation_data=val_gen,
        verbose=1
    )

    os.makedirs("saved_models", exist_ok=True)
    model.save("saved_models/xray_model.h5")

    _, accuracy = model.evaluate(val_gen, verbose=0)
    return model, round(accuracy * 100, 2)

def predict_xray(image_file):
    import tensorflow as tf
    model_path = "saved_models/xray_model.h5"
    if not os.path.exists(model_path):
        return None, None
    model = tf.keras.models.load_model(model_path)
    img_array = preprocess_image(image_file)
    prediction = model.predict(img_array)[0][0]
    confidence = round(float(prediction) * 100, 2) if prediction > 0.5 else round((1 - float(prediction)) * 100, 2)
    result = "Pneumonia Detected" if prediction > 0.5 else "Normal"
    return result, confidence
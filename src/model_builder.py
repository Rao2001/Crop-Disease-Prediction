import tensorflow as tf
from tensorflow.keras import layers, models

def build_transfer_model(num_classes, image_size=224, learning_rate=0.0001):
    """
    Builds a Transfer Learning model using MobileNetV2.
    
    Args:
        num_classes: Number of output classes (dynamic).
        image_size: Input image size (square).
        learning_rate: Optimizer learning rate.
        
    Returns:
        Compiled Keras model.
    """
    # 1. Load the pre-trained MobileNetV2 model
    # include_top=False means we drop the final 1000-class layer used for ImageNet
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(image_size, image_size, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # 2. Freeze the base model
    # We don't want to destroy the pre-learned patterns during the first phase of training
    base_model.trainable = False
    
    # 3. Add custom Classification Head
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x) # Better than Flatten() for CNNs
    x = layers.Dropout(0.2)(x) # Prevent overfitting
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.1)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = models.Model(inputs=base_model.input, outputs=outputs, name="MobileNetV2_Transfer")
    
    # 4. Compile
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

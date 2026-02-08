import tensorflow as tf
import os

def load_data(data_dir, image_size=224, batch_size=32, val_split=0.2):
    """
    Loads dataset from a directory, infers class names, and splits into Train/Val.
    
    Args:
        data_dir: Path to the dataset (containing subfolders of classes).
        
    Returns:
        train_ds, val_ds, class_names (list)
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory '{data_dir}' not found.")
        
    # Count classes efficiently
    subdirs = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    if not subdirs:
        raise ValueError(f"No class folders found in '{data_dir}'. Please add subfolders for each crop/disease.")
        
    print(f"Found {len(subdirs)} classes: {subdirs}")
    
    # Load Training Data
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="training",
        seed=123,
        image_size=(image_size, image_size),
        batch_size=batch_size
    )
    
    # Load Validation Data
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=val_split,
        subset="validation",
        seed=123,
        image_size=(image_size, image_size),
        batch_size=batch_size
    )
    
    class_names = train_ds.class_names
    
    # Optimize dataset performance (prefetching)
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
    
    return train_ds, val_ds, class_names

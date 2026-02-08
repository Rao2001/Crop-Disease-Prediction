import tensorflow as tf
import os

def train_job(model, train_ds, val_ds, epochs=10, model_save_path='./models/best_model.h5'):
    """
    Runs the training loop with callbacks.
    """
    # Define Callbacks
    
    # 1. EarlyStopping: Stop if validation accuracy doesn't improve for 3 epochs
    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    )
    
    # 2. ModelCheckpoint: Save the best model automatically
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        model_save_path,
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    # 3. ReduceLROnPlateau: Slow down learning rate if stuck
    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=2,
        min_lr=0.00001,
        verbose=1
    )
    
    print(f"Starting training for {epochs} epochs...")
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[early_stop, checkpoint, reduce_lr]
    )
    
    return history

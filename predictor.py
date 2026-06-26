"""
Plant Disease Predictor
========================
Loads the trained model (Keras .h5 or TFLite) and runs inference.

Two modes:
  - Keras mode  : uses full .h5 model (server with enough RAM/GPU)
  - TFLite mode : uses quantized .tflite model (low-resource servers)
"""

import json
import os
import numpy as np
from pathlib import Path

from treatments import get_treatment

# Lazy imports — only loaded when needed
_keras_model  = None
_tflite_interp = None
_class_labels  = None

# ── Paths ───────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent
MODEL_DIR   = BASE_DIR / "model"

KERAS_PATH  = MODEL_DIR / "best.keras"
TFLITE_PATH = MODEL_DIR / "plant_disease_model_quantized.tflite"
LABELS_PATH = MODEL_DIR / "class_labels.json"

# Confidence threshold — predictions below this are marked as "uncertain"
CONFIDENCE_THRESHOLD = 0.15


# ── Label Loading ────────────────────────────────────────────────────────────

def load_labels() -> dict:
    """Load integer → class_name mapping."""
    global _class_labels
    if _class_labels is None:
        with open(LABELS_PATH) as f:
            raw = json.load(f)
        # Keys from JSON are strings; convert to int
        _class_labels = {int(k): v for k, v in raw.items()}
    return _class_labels


# ── Keras Model ──────────────────────────────────────────────────────────────

def load_keras_model():
    """Load Keras .h5 model (once, then cached)."""
    global _keras_model
    if _keras_model is None:
        import tensorflow as tf
        print(f"[Predictor] Loading Keras model from {KERAS_PATH} …")
        _keras_model = tf.keras.models.load_model(str(KERAS_PATH))
        print("[Predictor] Keras model loaded ✓")
    return _keras_model


def predict_keras(img_array: np.ndarray) -> np.ndarray:
    """
    Run Keras inference.
    img_array: shape (1, 224, 224, 3), float32 normalised [0,1]
    Returns: probability array shape (1, num_classes)
    """
    model = load_keras_model()
    return model.predict(img_array, verbose=0)


# ── TFLite Model ─────────────────────────────────────────────────────────────

def load_tflite_interpreter():
    """Load TFLite interpreter (once, then cached)."""
    global _tflite_interp
    if _tflite_interp is None:
        import tensorflow as tf
        print(f"[Predictor] Loading TFLite model from {TFLITE_PATH} …")
        _tflite_interp = tf.lite.Interpreter(model_path=str(TFLITE_PATH))
        _tflite_interp.allocate_tensors()
        print("[Predictor] TFLite interpreter loaded ✓")
    return _tflite_interp


def predict_tflite(img_array: np.ndarray) -> np.ndarray:
    """
    Run TFLite inference.
    img_array: shape (1, 224, 224, 3), float32 normalised [0,1]
    Returns: probability array shape (1, num_classes)
    """
    interp = load_tflite_interpreter()
    input_details  = interp.get_input_details()
    output_details = interp.get_output_details()

    interp.set_tensor(input_details[0]["index"], img_array)
    interp.invoke()
    output = interp.get_tensor(output_details[0]["index"])
    return output


# ── Main Predict Function ────────────────────────────────────────────────────

def predict(img_array: np.ndarray, use_tflite: bool = False) -> dict:
    """
    Run prediction and return structured result.

    Parameters:
        img_array  : preprocessed image, shape (1, 224, 224, 3)
        use_tflite : True = use TFLite model (faster, lower RAM)

    Returns dict:
        {
          "class_name"    : "Tomato___Late_blight",
          "disease"       : "Tomato Late Blight",
          "crop"          : "Tomato",
          "confidence"    : 0.943,          # 0.0 – 1.0
          "confident"     : True,
          "top3"          : [...],           # top 3 predictions
          "treatment"     : { ... },         # from treatments.py
        }
    """
    labels = load_labels()

    # Run inference
    if use_tflite:
        probs = predict_tflite(img_array)[0]
    else:
        probs = predict_keras(img_array)[0]

    # Top prediction
    top_idx    = int(np.argmax(probs))
    confidence = float(probs[top_idx])
    class_name = labels[top_idx]

    # Top-3 for UI display
    top3_idx = np.argsort(probs)[::-1][:3]
    top3     = [
        {
            "class_name" : labels[i],
            "disease"    : get_treatment(labels[i])["disease"],
            "confidence" : round(float(probs[i]) * 100, 1),
        }
        for i in top3_idx
    ]

    # Treatment info
    treatment_info = get_treatment(class_name)

    return {
        "class_name" : class_name,
        "disease"    : treatment_info["disease"],
        "crop"       : treatment_info["crop"],
        "confidence" : round(confidence, 4),
        "confident"  : confidence >= CONFIDENCE_THRESHOLD,
        "top3"       : top3,
        "treatment"  : treatment_info,
    }

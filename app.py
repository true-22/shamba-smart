"""
Plant Disease Detection — Flask Backend API
============================================
Endpoints:
  POST /api/predict     → upload image, get prediction
  GET  /api/health      → server health check
  GET  /api/diseases    → list all known disease classes
  GET  /                → serve frontend (if static/ folder exists)

Usage:
    pip install -r requirements.txt
    python app.py

Environment variables:
    PORT        : server port (default 5000)
    USE_TFLITE  : set to "1" to use TFLite model instead of Keras
    DEBUG       : set to "1" for Flask debug mode (dev only)
"""

import os
import io
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Local modules
from validator  import validate_image, preprocess_for_model, ValidationError
from predictor  import predict, load_labels
from treatments import list_all_diseases


# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)   # Allow cross-origin requests (needed when frontend is separate)

# Logging
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s [%(levelname)s] %(message)s",
    handlers= [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("api.log"),
    ]
)
logger = logging.getLogger(__name__)

# Config
USE_TFLITE        = os.environ.get("USE_TFLITE", "0") == "1"
MAX_CONTENT_LENGTH = 20 * 1024 * 1024   # 20 MB hard limit for Flask itself
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp"}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def allowed_extension(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def error_response(message: str, code: str, status: int = 400, retake: bool = False) -> tuple:
    """Standardised JSON error response."""
    logger.warning(f"[{code}] {message}")
    return jsonify({
        "success"  : False,
        "error"    : {"message": message, "code": code, "retake": retake},
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }), status


# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def serve_index():
    """Serve the frontend index.html if running as a single server."""
    static_dir = Path(app.static_folder)
    if (static_dir / "index.html").exists():
        return send_from_directory(app.static_folder, "index.html")
    return jsonify({"message": "Plant Disease Detection API is running. POST /api/predict"}), 200


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint — useful for uptime monitoring."""
    return jsonify({
        "status"    : "healthy",
        "model_mode": "tflite" if USE_TFLITE else "keras",
        "timestamp" : datetime.utcnow().isoformat() + "Z",
        "version"   : "1.0.0",
    }), 200


@app.route("/api/diseases", methods=["GET"])
def list_diseases():
    """Return a list of all disease classes the model can detect."""
    diseases = list_all_diseases()
    return jsonify({
        "success"      : True,
        "total_classes": len(diseases),
        "diseases"     : diseases,
    }), 200


@app.route("/api/predict", methods=["POST"])
def predict_disease():
    """
    Main prediction endpoint.

    Accepts:
        multipart/form-data with 'image' file field
        OR application/json with 'image_base64' field (base64-encoded)

    Returns:
        JSON prediction result with disease name, confidence, and treatment.
    """
    t_start = time.perf_counter()

    # ── 1. Extract image bytes ───────────────────────────────────
    file_bytes = None

    if "image" in request.files:
        file = request.files["image"]
        if file.filename == "":
            return error_response("No file selected.", "NO_FILE_SELECTED")
        if not allowed_extension(file.filename):
            return error_response(
                "Unsupported file format. Please upload a JPG or PNG image.",
                "UNSUPPORTED_FORMAT"
            )
        file_bytes = file.read()

    elif request.is_json and "image_base64" in request.json:
        import base64
        try:
            b64_str    = request.json["image_base64"]
            # Strip data URI prefix if present: "data:image/jpeg;base64,..."
            if "," in b64_str:
                b64_str = b64_str.split(",", 1)[1]
            file_bytes = base64.b64decode(b64_str)
        except Exception:
            return error_response("Invalid base64 image data.", "INVALID_BASE64")

    else:
        return error_response(
            "No image provided. Send a multipart file under 'image' key, "
            "or JSON with 'image_base64' key.",
            "NO_IMAGE_IN_REQUEST"
        )

    # ── 2. Validate image ────────────────────────────────────────
    try:
        cv_img, img_meta = validate_image(file_bytes)
    except ValidationError as e:
        return error_response(e.message, e.code, status=422, retake=e.retake)

    # ── 3. Preprocess ────────────────────────────────────────────
    img_array = preprocess_for_model(cv_img, target_size=(160, 160))

    # ── 4. Inference ─────────────────────────────────────────────
    try:
        result = predict(img_array, use_tflite=USE_TFLITE)
    except Exception as e:
        logger.error(f"Model inference failed: {e}", exc_info=True)
        return error_response(
            "Prediction failed due to a server error. Please try again.",
            "INFERENCE_ERROR",
            status=500
        )

    elapsed_ms = round((time.perf_counter() - t_start) * 1000, 1)

    # ── 5. Handle low-confidence predictions ────────────────────
    if not result["confident"]:
        # Still return the result but flag low confidence
        logger.info(
            f"Low confidence prediction: {result['class_name']} "
            f"({result['confidence']*100:.1f}%)"
        )

    # ── 6. Log prediction ────────────────────────────────────────
    logger.info(
        f"Prediction: {result['disease']} | "
        f"Confidence: {result['confidence']*100:.1f}% | "
        f"Latency: {elapsed_ms}ms | "
        f"Image: {img_meta['width']}x{img_meta['height']}px"
    )

    # ── 7. Build response ────────────────────────────────────────
    treatment = result["treatment"]

    response_data = {
        "success"    : True,
        "prediction" : {
            "class_name"  : result["class_name"],
            "disease"     : result["disease"],
            "crop"        : result["crop"],
            "confidence"  : result["confidence"],
            "confidence_pct": round(result["confidence"] * 100, 1),
            "confident"   : result["confident"],
            "top3"        : result["top3"],
        },
        "treatment"  : {
            "severity"    : treatment["severity"],
            "symptoms"    : treatment["symptoms"],
            "organic"     : treatment["organic"],
            "chemical"    : treatment["chemical"],
            "prevention"  : treatment["prevention"],
            "urgency"     : treatment["urgency"],
            "local_tip"   : treatment["local_tip"],
        },
        "image_quality": img_meta,
        "meta": {
            "model_mode"  : "tflite" if USE_TFLITE else "keras",
            "latency_ms"  : elapsed_ms,
            "timestamp"   : datetime.utcnow().isoformat() + "Z",
        }
    }

    return jsonify(response_data), 200


# ─────────────────────────────────────────────
# ERROR HANDLERS
# ─────────────────────────────────────────────

@app.errorhandler(413)
def request_entity_too_large(e):
    return error_response("File too large. Maximum size is 20 MB.", "FILE_TOO_LARGE", 413)


@app.errorhandler(404)
def not_found(e):
    return error_response("Endpoint not found.", "NOT_FOUND", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return error_response("Method not allowed.", "METHOD_NOT_ALLOWED", 405)


@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Unhandled server error: {e}", exc_info=True)
    return error_response("Internal server error.", "SERVER_ERROR", 500)


# ─────────────────────────────────────────────
# STARTUP
# ─────────────────────────────────────────────

if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "0") == "1"

    logger.info("=" * 55)
    logger.info("  🌱  Plant Disease Detection API")
    logger.info(f"  Model mode : {'TFLite' if USE_TFLITE else 'Keras (.h5)'}")
    logger.info(f"  Port       : {port}")
    logger.info(f"  Debug      : {debug}")
    logger.info("=" * 55)

    # Pre-warm model to avoid cold-start on first request
    try:
        load_labels()
        import numpy as np
        dummy = np.zeros((1, 160, 160, 3), dtype=np.float32)
        predict(dummy, use_tflite=USE_TFLITE)
        logger.info("Model pre-warmed successfully ✓")
    except Exception as e:
        logger.warning(f"Model pre-warm failed (model files missing?): {e}")

    app.run(host="0.0.0.0", port=port, debug=debug)

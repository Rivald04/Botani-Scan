import logging
from flask import jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import io
import numpy as np

# Load corn model
model = load_model('modelAI/corn_model_2.h5')

logging.basicConfig(level=logging.DEBUG)

def predict_corn(request):
    # Periksa apakah ada file gambar yang dikirimkan dalam permintaan
    if 'file' not in request.files:
        logging.error('No file found')
        return jsonify({'error': 'No file found'})
    file = request.files['file']
    # Periksa apakah file memiliki nama
    if file.filename == '':
        logging.error('No filename provided')
        return jsonify({'error': 'No filename provided'})
    try:
        file = request.files['file']
        img = image.load_img(io.BytesIO(file.read()), target_size=(256, 256))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
  
        images = np.vstack([x])
        images /= 255

        classes = model.predict(images, batch_size=32)
        predicted_class_indices = np.argmax(classes)

        # label
        class_labels = ['Corn Cercospora Leaf Spot Gray', 'Corn Common Rust', 'Corn Healthy', 'Corn Northern Leaf Blight', 'Not Corn Clean']
        predicted_label = class_labels[predicted_class_indices]

        # Format hasil prediksi sebagai JSON
        response = {
            'prediction': predicted_label,
            'confidence': round(np.max(classes) * 100, 2)
        }

        # Mengembalikan respons JSON
        return jsonify(response)
    except Exception as e:
        logging.error(str(e))
        return jsonify({'error': 'Invalid image file'})
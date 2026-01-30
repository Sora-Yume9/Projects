from pynput import keyboard
import socketio
import base64
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image
import numpy as np
import eventlet
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
from io import BytesIO
model = tf.keras.models.load_model('my_model.keras')
cli = socketio.Client()
cli.connect('http://localhost:5000')

@sio.event
def Got_image(sid, data):
    test_images = []
    base64_data = data.get("image").split(',')[1]
    image_data = base64.b64decode(base64_data + '==')
    image = Image.open(BytesIO(image_data))
    image = image.resize((28, 28))
    image = image.convert('L')
    img_array = np.array(image)
    img_array = img_array / 255.0
    test_images.append(img_array.reshape((28, 28, 1))) 
    test_array = np.array(test_images)
    pre = model.predict(test_array)
    print(pre)
    predicted_classes = np.argmax(pre, axis=1) + 1
    print("Predicted classes:", predicted_classes)    
    cli.emit('Prediction', {'message': predicted_classes.tolist()})

eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)

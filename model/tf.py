import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from PIL import Image
import numpy as np

a = 1
imges = []

while a < 28:
    path = f"./X_train/{a}.png"
    img = Image.open(path)
    img_resized = img.resize((28, 28))
    img_resized_gray = img_resized.convert('L')
    img_array = np.array(img_resized_gray)
    img_array = img_array / 255.0
    imges.append(img_array.reshape((28, 28, 1)))  
    a += 1

imges = np.array(imges)

test_images = []
b = 1

while b < 6:
    if b == 2:
        b+=1
    path = f"./X_train/x{b}.png"
    img = Image.open(path)
    img_resized = img.resize((28, 28))
    img_resized_gray = img_resized.convert('L')
    img_array = np.array(img_resized_gray)
    img_array = img_array / 255.0
    test_images.append(img_array.reshape((28, 28, 1))) 
    b += 1

test_array = np.array(test_images)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(5, activation='sigmoid'))

model.compile(optimizer='adam', loss='CategoricalCrossentropy', metrics=['accuracy'])

Y_train = np.array([[1, 0, 0, 0, 0], 
[0, 1, 0, 0, 0], 
[0, 0, 1, 0, 0], 
[0, 0, 0, 1, 0], 
[0, 0, 0, 0, 1],
[1, 0, 0, 0, 0], 
[0, 1, 0, 0, 0], 
[0, 1, 0, 0, 0],
[0, 0, 1, 0, 0],
[0, 1, 0, 0, 0],
[0, 0, 0, 1, 0], 
[0, 0, 0, 1, 0], 
[0, 0, 0, 0, 1],
[0, 0, 1, 0, 0], 
[0, 0, 1, 0, 0], 
[0, 0, 1, 0, 0],
[0, 0, 1, 0, 0], 
[0, 0, 1, 0, 0], 
[0, 0, 1, 0, 0],
[0, 0, 1, 0, 0], 
[0, 0, 1, 0, 0],
[0, 0, 1, 0, 0],
[0, 1, 0, 0, 0], 
[0, 1, 0, 0, 0],
[0, 1, 0, 0, 0],
[0, 1, 0, 0, 0],
[1, 0, 0, 0, 0]      
])
model.fit(imges, Y_train, epochs=110)

pre = model.predict(test_array)
print(pre)
predicted_classes = np.argmax(pre, axis=1) + 1
print("Predicted classes:", predicted_classes)
model.save('my_model.keras')

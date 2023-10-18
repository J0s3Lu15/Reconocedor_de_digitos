# Importar las bibliotecas necesarias
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical

# Cargar el conjunto de datos MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Preprocesar los datos
x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Crear el modelo
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

# Compilar el modelo
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Entrenar el modelo
print("Comenzando el entrenamiento...")
model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=15, batch_size=200)
print("Entrenamiento completado.")

# Evaluar el modelo
score = model.evaluate(x_test, y_test, verbose=0)

try:
    print("Guardando el modelo...")
    model.save('modelo/modelo_digitos.keras')
    print("Modelo guardado con éxito.")
except Exception as e:
    print(f"Error al guardar el modelo: {e}")

print('Pérdida en el conjunto de prueba:', score[0])
print('Precisión en el conjunto de prueba:', score[1])

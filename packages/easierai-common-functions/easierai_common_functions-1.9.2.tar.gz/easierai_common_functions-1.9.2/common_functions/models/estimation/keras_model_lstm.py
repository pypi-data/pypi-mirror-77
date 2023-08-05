#   Copyright  2020 Atos Spain SA. All rights reserved.
 
#   This file is part of EASIER AI.
 
#   EASIER AI is free software: you can redistribute it and/or modify it under the terms of Apache License, either version 2 of the License, or
#   (at your option) any later version.
 
#   THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT ANY WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT,
#   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#   WHETHER IN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
#   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#   See  LICENSE file for full license information  in the project root.
from tensorflow.keras import Sequential, optimizers
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.models import Model
import tensorflow.keras.models

class Predictor:
    learning_rate = 0.001

    decay_lr = 0

    loss_fn = 'mean_squared_error'

    def __init__(self, output_activation, ft_range, lr=0.001):
        self.model = None
        self.output_activation = output_activation
        self.ft_range = ft_range
        self.learning_rate = lr

    def predict(self, input):
        return self.model.predict(input)

    def classify(self, input):
        return self.model.predict_proba(input), self.model.predict_classes(input)

    def load_model(self, path):
        self.model = tensorflow.keras.models.load_model(path)
        self.model._make_predict_function()

    def get_model(self, shape, num_forecasts, inner_activation='tanh'):
        model = Sequential()
        # Shape = (Samples, Timesteps, Features)
        model.add(LSTM(units=128, input_shape=shape,
                       return_sequences=False, activation=inner_activation))
        model.add(Dropout(0.2))

        model.add(Dense(units=num_forecasts, activation=self.output_activation))

        opt = optimizers.Adagrad(lr=self.learning_rate, decay=self.decay_lr)
        # opt = optimizers.rmsprop(lr=0.01)
        model.compile(optimizer=opt, loss=self.loss_fn, metrics=['mae'])
        model.summary()
        return model

    def get_model_configurable(self, shape, num_forecasts, inner_activation='tanh', num_dense_layers=1, num_units_per_layer=[64], loss='mae', metrics=['mse']):
        model = Sequential()
        # Input arrays of shape (*, layers[1])
        # Output = arrays of shape (*, layers[1] * 16)
        model.add(LSTM(units=int(num_units_per_layer[0]), input_shape=shape,
                       return_sequences=True, activation=inner_activation))
        for i in range(1,num_dense_layers-1):
            model.add(LSTM(units=int(num_units_per_layer[i]),
                       return_sequences=True, activation=inner_activation))
        model.add(LSTM(units=int(num_units_per_layer[num_dense_layers-1]), input_shape=shape,
                       return_sequences=False, activation=inner_activation))
        model.add(Dropout(0.2))
        model.add(Dense(units=num_forecasts, activation=self.output_activation))

        # opt = optimizers.Adagrad(lr=self.learning_rate, epsilon=None, decay=self.decay_lr)
        opt = optimizers.RMSprop(lr=self.learning_rate)
        model.compile(optimizer=opt, loss=loss, metrics=metrics)
        model.summary()
        self.model = model
        return model
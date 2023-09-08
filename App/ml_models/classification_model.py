import torch
import torch.nn as nn
import torchvision
import numpy as np
import tensorflow as tf

class ClassificationModel():
    def __init__(self, model_path='App/ml_models/classmodelv5.1.tflite'):
        # Load the TFLite model and allocate tensors
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']

    def forward(self, x):
        input_data = x
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)

        self.interpreter.invoke()

        # get_tensor() returns a copy of the tensor data
        # use tensor() in order to get a pointer to the tensor
        outputs = self.interpreter.get_tensor(self.output_details[0]['index'])

        return outputs

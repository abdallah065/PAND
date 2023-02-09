import onnx
from onnx_tf.backend import prepare
import tensorflow as tf
import tensorflow.lite as tflite
import numpy as np

onnx_model = onnx.load('model.onnx')
tf_rep = prepare(onnx_model)

tf_rep.export_graph('plant_tf_mode.pb')
#pip install update tensorflow==1.15.0
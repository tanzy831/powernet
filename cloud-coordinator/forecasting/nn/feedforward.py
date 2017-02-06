from matplotlib.pyplot import figure, show

import math
import numpy as np
import os
import random
import time
import tensorflow as tf

FLAGS = None

def generate_batch(data, batch_size = 100):
  x, y = data
  indices = np.random.choice(len(x), batch_size, replace=False)
  return x[indices], y[indices]

class FeedForward:
  def __init__(self, num_layer = 1, num_neuron = 100):
    self.num_layer = num_layer
    self.num_neuron = num_neuron
    self.sess = tf.InteractiveSession()
    self.input_size = 7 * 24 #represents a week's worth of datas
    self.output_size = 24

    self.construct_graph()

  def layer(self, x, num_neuron):
    input_shape = x.get_shape()
    #layer takes input x, with num_neuron many neurons. Relu is used for activation.
    W = tf.get_variable("W", shape=[input_shape[1], num_neuron], initializer=tf.contrib.layers.xavier_initializer())
    b = tf.get_variable("b", shape=[num_neuron], initializer=tf.constant_initializer(0))
    y = tf.matmul(x, W) + b
    return tf.nn.relu(y)

  def construct_graph(self):
    self.x = tf.placeholder(tf.float32, [None, self.input_size])
    h = self.x
    for layer_idx in range(self.num_layer):
      #add intermediate layers
      with tf.variable_scope("layer{}".format(layer_idx)):
        h = self.layer(h, self.num_neuron)

    #add projection layer
    with tf.variable_scope("proj_layer"):
      hidden_shape = h.get_shape()
      W = tf.get_variable("W", shape=[hidden_shape[1], self.output_size],
        initializer=tf.contrib.layers.xavier_initializer())

      b = tf.get_variable("b", shape=[self.output_size], initializer=tf.constant_initializer(0))
      y = tf.matmul(h, W) + b

    self.prediction = y
    self.y_ = tf.placeholder(tf.float32, [None, self.output_size])

    loss = tf.reduce_mean(tf.divide(tf.abs(y - self.y_), y))
    tf.summary.scalar('mean_squared_error_%d' % time.time(), tf.reduce_mean(tf.square(y - self.y_)))
    self.loss = loss

    self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.loss)
    self.saver = tf.train.Saver()

  def train(self, data):
    merged = tf.summary.merge_all()
    train_writer = tf.summary.FileWriter('./train')
    validation_writer = tf.summary.FileWriter('./validation')

    tf.global_variables_initializer().run()
    batch_size = 100
    for i in range(4000):
      batch_xs_train, batch_ys_train = generate_batch(data, batch_size)
      batch_ys_train.reshape(batch_size, 24)

      train_summary, train = self.sess.run([merged, self.train_step],
        feed_dict={
        self.x: batch_xs_train,
        self.y_: batch_ys_train
        })
      train_writer.add_summary(train_summary, i)

      # pick another random set for validation
      batch_xs_validation, batch_ys_validation = generate_batch(data, batch_size)

      validation_summary, validation = self.sess.run([merged, self.loss],
        feed_dict={
        self.x: batch_xs_validation,
        self.y_: batch_ys_validation
        })

      validation_writer.add_summary(validation_summary, i)

    save_path = self.saver.save(self.sess, "./model.ckpt")

  def test(self, data):
    x, y = data
    self.saver.restore(self.sess, "./model.ckpt")
    return self.sess.run(self.loss, feed_dict = {self.x: x, self.y_: y})
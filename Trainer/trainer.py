from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dropout, LSTM, Dense, Bidirectional, Activation, Embedding
from keras.callbacks import ModelCheckpoint, EarlyStopping

import numpy as np


class Trainer:
    def __init__(self, textfile, seq_length=50, batch_size=32):
        self.textfile = textfile
        self.seq_length = seq_length
        self.BATCH_SIZE = batch_size

        self._process_content()
        self._build_model()
        self._setup_checkpoints()

    def _setup_checkpoints(self):
        model_checkpoint = ModelCheckpoint(
            'model.hdf5', monitor='acc', save_best_only=True)
        earlystopping_checkpoint = EarlyStopping(
            monitor='acc', patience=20)
        self._checkpoints = [model_checkpoint, earlystopping_checkpoint]

    def _build_model(self):
        model = Sequential()
        model.add(Embedding(input_dim=len(self._words), output_dim=1024))

        model.add(Bidirectional(
            LSTM(128), input_shape=(self.seq_length, len(self._words))))

        model.add(Dropout(0.5))
        model.add(Dense(len(self._words)))
        model.add(Activation('softmax'))
        model.compile(loss='sparse_categorical_crossentropy',
                      optimizer="adam", metrics=['accuracy'])

        self._model = model

    def _process_content(self):
        file = open(self.textfile, 'r')
        filecontents = file.read()
        file.close()
        filecontents = filecontents.replace('\n', ' \n ')

        text_in_words = [w for w in filecontents.split(
            ' ') if w.strip() != '' or w == '\n']
        self._words = set(text_in_words)

        self._word_indices = dict((c, i) for i, c in enumerate(self._words))
        self._indices_word = dict((i, c) for i, c in enumerate(self._words))

        STEP = 1
        self._codelines = []
        self._next_words = []
        for i in range(0, len(text_in_words) - self.seq_length, STEP):
            # print(text_in_words[i: i + self.seq_length])
            self._codelines.append(text_in_words[i: i + self.seq_length])
            self._next_words.append(text_in_words[i + self.seq_length])

    def _generator(self, sentence_list, next_word_list, batch_size):
        index = 0
        while True:
            x = np.zeros((batch_size, self.seq_length), dtype=np.int32)
            y = np.zeros((batch_size), dtype=np.int32)
            for i in range(batch_size):
                for t, w in enumerate(sentence_list[index % len(sentence_list)]):
                    x[i, t] = self._word_indices[w]
                y[i] = self._word_indices[next_word_list[index %
                                                         len(sentence_list)]]
                index = index + 1
            yield x, y

    def train(self):
        self._model.fit_generator(self._generator(self._codelines, self._next_words, self.BATCH_SIZE),
                                  steps_per_epoch=int(
                                      len(self._codelines)/self.BATCH_SIZE) + 1,
                                  epochs=100,
                                  callbacks=self._checkpoints)

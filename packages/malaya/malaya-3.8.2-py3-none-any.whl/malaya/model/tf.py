import tensorflow as tf
import numpy as np
import re
from unidecode import unidecode
from malaya.text.function import (
    language_detection_textcleaning,
    split_into_sentences,
    transformer_textcleaning,
    translation_textcleaning,
    pad_sentence_batch,
)
from malaya.text.bpe import (
    constituency_bert,
    constituency_xlnet,
    PTB_TOKEN_ESCAPE,
)
from malaya.text import chart_decoder
from malaya.text.trees import tree_from_str
from herpetologist import check_type
from typing import List


def _convert_sparse_matrix_to_sparse_tensor(X, got_limit = False, limit = 5):
    coo = X.tocoo()
    indices = np.mat([coo.row, coo.col]).transpose()
    if got_limit:
        coo.data[coo.data > limit] = limit
    return (
        tf.SparseTensorValue(indices, coo.col, coo.shape),
        tf.SparseTensorValue(indices, coo.data, coo.shape),
    )


class _LANG_MODEL:
    def __init__(self, dimension = 32, output = 6):
        self.X = tf.sparse_placeholder(tf.int32)
        self.W = tf.sparse_placeholder(tf.int32)
        self.Y = tf.placeholder(tf.int32, [None])
        embeddings = tf.Variable(tf.truncated_normal([400000, dimension]))
        embed = tf.nn.embedding_lookup_sparse(
            embeddings, self.X, self.W, combiner = 'mean'
        )
        self.logits = tf.layers.dense(embed, output)


class DEEP_LANG:
    def __init__(self, path, vectorizer, label, bpe, type):
        self._graph = tf.Graph()
        with self._graph.as_default():
            self._model = _LANG_MODEL()
            self._sess = tf.InteractiveSession()
            self._sess.run(tf.global_variables_initializer())
            saver = tf.train.Saver(tf.trainable_variables())
            saver.restore(self._sess, path + '/model.ckpt')
        self._vectorizer = vectorizer
        self._label = label
        self._softmax = tf.nn.softmax(self._model.logits)
        self._bpe = bpe
        self._type = type

    def _classify(self, strings):
        strings = [language_detection_textcleaning(i) for i in strings]
        subs = [
            ' '.join(s)
            for s in self._bpe.encode(strings, output_type = self._type)
        ]
        transformed = self._vectorizer.transform(subs)
        batch_x = _convert_sparse_matrix_to_sparse_tensor(transformed)
        probs = self._sess.run(
            self._softmax,
            feed_dict = {self._model.X: batch_x[0], self._model.W: batch_x[1]},
        )
        return probs

    @check_type
    def predict(self, strings: List[str]):
        """
        classify list of strings.

        Parameters
        ----------
        strings: List[str]

        Returns
        -------
        result: List[str]
        """

        probs = self._classify(strings)
        dicts = []
        probs = np.argmax(probs, 1)
        for prob in probs:
            dicts.append(self._label[prob])
        return dicts

    @check_type
    def predict_proba(self, strings: List[str]):
        """
        classify list of strings and return probability.

        Parameters
        ----------
        strings : List[str]


        Returns
        -------
        result: List[dict[str, float]]
        """

        probs = self._classify(strings)
        dicts = []
        for i in range(probs.shape[0]):
            dicts.append({self._label[no]: k for no, k in enumerate(probs[i])})
        return dicts


class PARAPHRASE:
    def __init__(self, X, greedy, beam, sess, tokenizer):

        self._X = X
        self._greedy = greedy
        self._beam = beam
        self._sess = sess
        self._tokenizer = tokenizer

    def _paraphrase(self, strings, beam_search = True):
        encoded = [
            self._tokenizer.encode(translation_textcleaning(string)) + [1]
            for string in strings
        ]
        if beam_search:
            output = self._beam
        else:
            output = self._greedy
        batch_x = pad_sentence_batch(encoded, 0)[0]
        p = self._sess.run(output, feed_dict = {self._X: batch_x}).tolist()
        result = []
        for row in p:
            result.append(
                self._tokenizer.decode([i for i in row if i not in [0, 1]])
            )
        return result

    @check_type
    def paraphrase(
        self, string: str, beam_search: bool = True, split_fullstop: bool = True
    ):
        """
        Paraphrase a string.

        Parameters
        ----------
        string : str
        beam_search : bool, (optional=True)
            If True, use beam search decoder, else use greedy decoder.
        split_fullstop: bool, (default=True)
            if True, will generate paraphrase for each strings splitted by fullstop.

        Returns
        -------
        result: str
        """

        if split_fullstop:

            splitted_fullstop = split_into_sentences(
                transformer_textcleaning(string)
            )

            results, batch, mapping = [], [], {}
            for no, splitted in enumerate(splitted_fullstop):
                if len(splitted.split()) < 4:
                    results.append(splitted)
                else:
                    mapping[len(batch)] = no
                    results.append('REPLACE-ME')
                    batch.append(splitted)

            if len(batch):
                output = self._paraphrase(batch, beam_search = beam_search)
                for no in range(len(output)):
                    results[mapping[no]] = output[no]

            return ' '.join(results)

        else:
            return self._paraphrase([string], beam_search = beam_search)[0]


class TRANSLATION:
    def __init__(self, X, greedy, beam, sess, tokenizer):

        self._X = X
        self._greedy = greedy
        self._beam = beam
        self._sess = sess
        self._tokenizer = tokenizer

    def _translate(self, strings, beam_search = True):
        encoded = [
            self._tokenizer.encode(translation_textcleaning(string)) + [1]
            for string in strings
        ]
        if beam_search:
            output = self._beam
        else:
            output = self._greedy
        batch_x = pad_sentence_batch(encoded, 0)[0]
        p = self._sess.run(output, feed_dict = {self._X: batch_x}).tolist()
        result = []
        for row in p:
            result.append(
                self._tokenizer.decode([i for i in row if i not in [0, 1]])
            )
        return result

    @check_type
    def translate(self, strings: List[str], beam_search: bool = True):
        """
        translate list of strings.

        Parameters
        ----------
        strings : List[str]
        beam_search : bool, (optional=True)
            If True, use beam search decoder, else use greedy decoder.

        Returns
        -------
        result: List[str]
        """
        return self._translate(strings, beam_search = beam_search)


class CONSTITUENCY:
    def __init__(
        self,
        input_ids,
        word_end_mask,
        charts,
        tags,
        sess,
        tokenizer,
        dictionary,
        mode,
    ):

        self._input_ids = input_ids
        self._word_end_mask = word_end_mask
        self._charts = charts
        self._tags = tags
        self._sess = sess
        self._tokenizer = tokenizer
        self._LABEL_VOCAB = dictionary['label']
        self._TAG_VOCAB = dictionary['tag']
        self._mode = mode

    def _parse(self, string):
        s = string.split()
        sentences = [s]
        if self._mode == 'bert':
            i, m = constituency_bert(self._tokenizer, sentences)
        elif self._mode == 'xlnet':
            i, m = constituency_xlnet(self._tokenizer, sentences)
        else:
            raise Exception(
                'mode not supported, only supported `bert` or `xlnet`'
            )
        charts_val, tags_val = self._sess.run(
            (self._charts, self._tags),
            {self._input_ids: i, self._word_end_mask: m},
        )
        for snum, sentence in enumerate(sentences):
            chart_size = len(sentence) + 1
            chart = charts_val[snum, :chart_size, :chart_size, :]
        return s, tags_val[0], chart_decoder.decode(chart)

    @check_type
    def parse_nltk_tree(self, string: str):

        """
        Parse a string into NLTK Tree, to make it useful, make sure you already installed tktinker.

        Parameters
        ----------
        string : str

        Returns
        -------
        result: nltk.Tree object
        """

        try:
            import nltk
            from nltk import Tree
        except:
            raise Exception(
                'nltk not installed. Please install it and try again.'
            )

        sentence, tags, (score, p_i, p_j, p_label) = self._parse(string)

        idx_cell = [-1]

        def make_tree():
            idx_cell[0] += 1
            idx = idx_cell[0]
            i, j, label_idx = p_i[idx], p_j[idx], p_label[idx]
            label = self._LABEL_VOCAB[label_idx]
            if (i + 1) >= j:
                word = sentence[i]
                tag = self._TAG_VOCAB[tags[i]]
                tag = PTB_TOKEN_ESCAPE.get(tag, tag)
                word = PTB_TOKEN_ESCAPE.get(word, word)
                tree = Tree(tag, [word])
                for sublabel in label[::-1]:
                    tree = Tree(sublabel, [tree])
                return [tree]
            else:
                left_trees = make_tree()
                right_trees = make_tree()
                children = left_trees + right_trees
                if label:
                    tree = Tree(label[-1], children)
                    for sublabel in reversed(label[:-1]):
                        tree = Tree(sublabel, [tree])
                    return [tree]
                else:
                    return children

        tree = make_tree()[0]
        tree.score = score
        return tree

    @check_type
    def parse_tree(self, string):

        """
        Parse a string into string treebank format.

        Parameters
        ----------
        string : str

        Returns
        -------
        result: malaya.text.trees.InternalTreebankNode class
        """

        sentence, tags, (score, p_i, p_j, p_label) = self._parse(string)

        idx_cell = [-1]

        def make_str():
            idx_cell[0] += 1
            idx = idx_cell[0]
            i, j, label_idx = p_i[idx], p_j[idx], p_label[idx]
            label = self._LABEL_VOCAB[label_idx]
            if (i + 1) >= j:
                word = sentence[i]
                tag = self._TAG_VOCAB[tags[i]]
                tag = PTB_TOKEN_ESCAPE.get(tag, tag)
                word = PTB_TOKEN_ESCAPE.get(word, word)
                s = '({} {})'.format(tag, word)
            else:
                children = []
                while (
                    (idx_cell[0] + 1) < len(p_i)
                    and i <= p_i[idx_cell[0] + 1]
                    and p_j[idx_cell[0] + 1] <= j
                ):
                    children.append(make_str())

                s = ' '.join(children)

            for sublabel in reversed(label):
                s = '({} {})'.format(sublabel, s)
            return s

        return tree_from_str(make_str())

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers

from graphgallery.nn.layers import GraphConvolution
from graphgallery.nn.models import SemiSupervisedModel
from graphgallery.sequence import FullBatchNodeSequence
from graphgallery.utils.shape import set_equal_in_length
from graphgallery import astensors, asintarr, normalize_x, normalize_adj, Bunch


class GCN_MIX(SemiSupervisedModel):
    """
        Implementation of Mixed Graph Convolutional Networks (GCN_MIX) occured in FastGCN. 
        Tensorflow 1.x implementation: <https://github.com/matenure/FastGCN>

    """

    def __init__(self, adj, x, labels, norm_adj=-0.5, norm_x=None,
                 device='CPU:0', seed=None, name=None, **kwargs):
        """Creat Mixed Graph Convolutional Networks (GCN_MIX) occured in FastGCN.

        Calculating `A @ X` in advance to save time.

        Parameters:
        ----------
            adj: Scipy.sparse.csr_matrix, shape [n_nodes, n_nodes]
                The input `symmetric` adjacency matrix in CSR format.
            x: Numpy.ndarray, shape [n_nodes, n_attrs]. 
                Node attribute matrix in Numpy format.
            labels: Numpy.ndarray, shape [n_nodes]
                Array, where each entry represents respective node's label(s).
            norm_adj: float scalar. optional 
                The normalize rate for adjacency matrix `adj`. (default: :obj:`-0.5`, 
                i.e., math:: \hat{A} = D^{-\frac{1}{2}} A D^{-\frac{1}{2}}) 
            norm_x: string. optional 
                How to normalize the node attribute matrix. See `graphgallery.normalize_x`
                (default :obj: `None`)
            device: string. optional 
                The device where the model is running on. You can specified `CPU` or `GPU` 
                for the model. (default: :str: `CPU:0`, i.e., running on the 0-th `CPU`)
            seed: interger scalar. optional 
                Used in combination with `tf.random.set_seed` & `np.random.seed` 
                & `random.seed` to create a reproducible sequence of tensors across 
                multiple calls. (default :obj: `None`, i.e., using random seed)
            name: string. optional
                Specified name for the model. (default: :str: `class.__name__`)
            kwargs: other customed keyword Parameters.

        """
        super().__init__(adj, x, labels, device=device, seed=seed, name=name, **kwargs)

        self.norm_adj = norm_adj
        self.norm_x = norm_x
        self.preprocess(adj, x)

    def preprocess(self, adj, x):
        super().preprocess(adj, x)
        adj, x = self.adj, self.x

        if self.norm_adj:
            adj = normalize_adj(adj, self.norm_adj)

        if self.norm_x:
            x = normalize_x(x, norm=self.norm_x)

        x = adj @ x

        with tf.device(self.device):
            self.x_norm, self.adj_norm = astensors(x), adj

    def build(self, hiddens=[16], activations=['relu'], dropouts=[0.5], l2_norms=[5e-4],
              lr=0.01, use_bias=False):

        ############# Record paras ###########
        local_paras = locals()
        local_paras.pop('self')
        paras = Bunch(**local_paras)
        hiddens, activations, dropouts, l2_norms = set_equal_in_length(hiddens, activations, dropouts, l2_norms)
        paras.update(Bunch(hiddens=hiddens, activations=activations, dropouts=dropouts, l2_norms=l2_norms))
        # update all parameters
        self.paras.update(paras)
        self.model_paras.update(paras)
        ######################################

        with tf.device(self.device):

            x = Input(batch_shape=[self.n_nodes, self.n_attrs], dtype=self.floatx, name='attributes')
            adj = Input(batch_shape=[None, self.n_nodes], dtype=self.floatx, sparse=True, name='adj_matrix')

            h = x
            for hid, activation, dropout, l2_norm in zip(hiddens, activations, dropouts, l2_norms):
                h = Dense(hid, use_bias=use_bias, activation=activation,
                          kernel_regularizer=regularizers.l2(l2_norm))(h)
                h = Dropout(rate=dropout)(h)

            output = GraphConvolution(self.n_classes, use_bias=use_bias, activation='softmax')([h, adj])

            model = Model(inputs=[x, adj], outputs=output)
            model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(lr=lr), metrics=['accuracy'])

            self.model = model

    def train_sequence(self, index):
        index = asintarr(index)
        labels = self.labels[index]
        adj = self.adj_norm[index]
        with tf.device(self.device):
            sequence = FullBatchNodeSequence([self.x_norm, adj], labels)
        return sequence

    def predict(self, index):
        super().predict(index)
        index = asintarr(index)
        adj = self.adj_norm[index]
        with tf.device(self.device):
            logit = self.model.predict_on_batch(astensors([self.x_norm, adj]))
        if tf.is_tensor(logit):
            logit = logit.numpy()
        return logit

import tensorflow as tf
from tensorflow.keras import Model, Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.losses import SparseCategoricalCrossentropy

from graphgallery.nn.layers import SGConvolution
from graphgallery.nn.models import SemiSupervisedModel
from graphgallery.sequence import FullBatchNodeSequence
from graphgallery.utils.shape import repeat
from graphgallery import astensors, asintarr, normalize_x, normalize_adj, Bunch


class SGC(SemiSupervisedModel):
    """
        Implementation of Simplifying Graph Convolutional Networks (SGC). 
        `Simplifying Graph Convolutional Networks <https://arxiv.org/abs/1902.07153>`
        Pytorch implementation: <https://github.com/Tiiiger/SGC>

    """

    def __init__(self, adj, x, labels, order=2,
                 norm_adj=-0.5, norm_x=None,
                 device='CPU:0', seed=None, name=None, **kwargs):
        """Creat a Simplifying Graph Convolutional Networks (SGC).
        Parameters:
        ----------
            adj: Scipy.sparse.csr_matrix, shape [n_nodes, n_nodes]
                The input `symmetric` adjacency matrix in CSR format.
            x: Numpy.ndarray, shape [n_nodes, n_attrs]. 
                Node attribute matrix in Numpy format.
            labels: Numpy.ndarray, shape [n_nodes]
                Array, where each entry represents respective node's label(s).
            order: positive integer. optional 
                The power (order) of adjacency matrix. (default :obj: `2`, i.e., math:: A^{2})
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

        self.order = order
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

        # To avoid this tensorflow error in large dataset:
        # InvalidArgumentError: Cannot use GPU when output.shape[1] * nnz(a) > 2^31 [Op:SparseTensorDenseMatMul]
        if self.n_attrs*adj.nnz > 2**31:
            device = "CPU"
        else:
            device = self.device

        with tf.device(device):
            x, adj = astensors([x, adj])
            x = SGConvolution(order=self.order)([x, adj])

        with tf.device(self.device):
            self.x_norm, self.adj_norm = x, adj

    def build(self, lr=0.2, l2_norms=[5e-5], use_bias=True):
        ############# Record paras ###########
        l2_norms = repeat(l2_norms, 1)
        local_paras = locals()
        local_paras.pop('self')
        paras = Bunch(**local_paras)
        # update all parameters
        self.paras.update(paras)
        self.model_paras.update(paras)
        ######################################

        with tf.device(self.device):

            x = Input(batch_shape=[None, self.n_attrs], dtype=self.floatx, name='attributes')

            output = Dense(self.n_classes, activation=None, use_bias=use_bias, kernel_regularizer=regularizers.l2(l2_norms[0]))(x)

            model = Model(inputs=x, outputs=output)
            model.compile(loss=SparseCategoricalCrossentropy(from_logits=True),
                          optimizer=Adam(lr=lr), metrics=['accuracy'])

            self.model = model

    def train_sequence(self, index):
        index = asintarr(index)
        labels = self.labels[index]
        with tf.device(self.device):
            x = tf.gather(self.x_norm, index)
            sequence = FullBatchNodeSequence(x, labels)
        return sequence

    def predict(self, index):
        super().predict(index)
        index = asintarr(index)
        with tf.device(self.device):
            x = tf.gather(self.x_norm, index)
            logit = self.model.predict_on_batch(x)

        if tf.is_tensor(logit):
            logit = logit.numpy()
        return logit

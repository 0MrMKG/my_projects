import numpy as np

def correct_dimensions(s, targetlength):
    """checks the dimensionality of some numeric argument s, broadcasts it
       to the specified length if possible.

    Args:
        s: None, scalar or 1D array
        targetlength: expected length of s

    Returns:
        None if s is None, else numpy vector of length targetlength
    """
    if s is not None:
        s = np.array(s)
        if s.ndim == 0:
            s = np.array([s] * targetlength)
        elif s.ndim == 1:
            if not len(s) == targetlength:
                raise ValueError("arg must have length " + str(targetlength))
        else:
            raise ValueError("Invalid argument")
    return s


def identity(x):
    return x


class ESN():

    def __init__(self, n_inputs, n_outputs, n_reservoir=200,
                 spectral_radius=0.95, sparsity=0, noise=0.001, input_shift=None,
                 input_scaling=None, teacher_forcing=True, feedback_scaling=None,
                 teacher_scaling=None, teacher_shift=None,
                 out_activation=identity, inverse_out_activation=identity,
                 random_state=None, silent=True):
        """
        Args:
            n_inputs: 输入向量维度
            n_outputs: 输出向量维度
            n_reservoir: 储备池维度
            spectral_radius:  recurrent weight matrix的谱半径
            sparsity: 稀疏性，用来初始化各个矩阵（除了Wout）
            noise: 加入网络的噪声
            input_shift: scalar or vector of length n_inputs to add to each
                        input dimension before feeding it to the network.
            input_scaling: scalar or vector of length n_inputs to multiply
                        with each input dimension before feeding it to the netw.
            teacher_forcing: if True, feed the target back into output units
            teacher_scaling: factor applied to the target signal
            teacher_shift: additive term applied to the target signal
            out_activation: 输出时候的激活函数 (applied to the readout)
            inverse_out_activation: inverse of the output activation function
            random_state: 是np.rand.RandomState的对象，表示随机种子数值

            silent: supress messages
        """
        # check for proper dimensionality of all arguments and write them down.
        self.n_inputs = n_inputs
        self.n_reservoir = n_reservoir
        self.n_outputs = n_outputs
        self.spectral_radius = spectral_radius
        self.sparsity = sparsity
        self.noise = noise
        self.input_shift = correct_dimensions(input_shift, n_inputs)
        self.input_scaling = correct_dimensions(input_scaling, n_inputs)

        self.teacher_scaling = teacher_scaling
        self.teacher_shift = teacher_shift

        self.out_activation = out_activation
        self.inverse_out_activation = inverse_out_activation
        self.random_state = random_state

        # the given random_state might be either an actual RandomState object,
        # a seed or None (in which case we use numpy's builtin RandomState)
        #类里面的random_state_参数指的是随机种子，是np.random.RandomState类型的变量
        #下列函数是判断是否是np.random.RandomState类型的变量
        if isinstance(random_state, np.random.RandomState):
            self.random_state_ = random_state
        elif random_state:
            try:
                self.random_state_ = np.random.RandomState(random_state)
            except TypeError as e:
                raise Exception("Invalid seed: " + str(e))
        else:
            self.random_state_ = np.random.mtrand._rand

        self.teacher_forcing = teacher_forcing
        self.silent = silent
        self.initweights()

    def initweights(self):
        #【初始化W矩阵】
        #取-0.5到0.5的随机数值
        W = self.random_state_.rand(self.n_reservoir, self.n_reservoir) - 0.5
        #dropout操作
        W[self.random_state_.rand(*W.shape) < self.sparsity] = 0
        #Wx以False形式保存要删除的神经元
        # Wx = self.random_state_.rand(*W.shape) >= self.sparsity
        # W *= Wx
        #计算radius
        radius = np.max(np.abs(np.linalg.eigvals(W)))
        #使原矩阵除以radius
        self.W = W * (self.spectral_radius / radius)

        #【初始化W_in矩阵】
        # random input weights:
        self.W_in = self.random_state_.rand(
            self.n_reservoir, self.n_inputs) * 2 - 1
        # 【初始化W_feedback矩阵】
        # random feedback (teacher forcing) weights:
        self.W_feedb = self.random_state_.rand(
            self.n_reservoir, self.n_outputs) * 2 - 1

    def _update(self, state, input_pattern, output_pattern):
        """performs one update step.

        i.e., computes the next network state by applying the recurrent weights
        to the last state & and feeding in the current input and output patterns
        """
        #分为两种训练模式
        #teacher_forcing 使用来自先验时间步长的输出作为输入
        #在训练网络过程中，每次不使用上一个state的输出作为下一个state的输入，
        #而是直接使用训练数据的标准答案(ground truth)的对应上一项作为下一个state的输入。
        if self.teacher_forcing:
            preactivation = (np.dot(self.W, state)
                             + np.dot(self.W_in, input_pattern)
                             + np.dot(self.W_feedb, output_pattern))
        #free-running mode 上一个state的输出作为下一个state的输入。
        else:
            preactivation = (np.dot(self.W, state)
                             + np.dot(self.W_in, input_pattern))
        return (np.tanh(preactivation)
                + self.noise * (self.random_state_.rand(self.n_reservoir) - 0.5))

    def _scale_inputs(self, inputs):
        """for each input dimension j: multiplies by the j'th entry in the
        input_scaling argument, then adds the j'th entry of the input_shift
        argument."""
        #点乘以input_scaling构建的对角矩阵
        if self.input_scaling is not None:
            inputs = np.dot(inputs, np.diag(self.input_scaling))
        # 加上偏移值
        if self.input_shift is not None:
            inputs = inputs + self.input_shift
        return inputs

    def _scale_teacher(self, teacher):
        """multiplies the teacher/target signal by the teacher_scaling argument,
        then adds the teacher_shift argument to it."""
        #没有必要这么处理,teacher_scaling teacher_shift 都是None,所以以下两个代码在ESN调用的时候不执行
        #乘相关参数
        if self.teacher_scaling is not None:
            teacher = teacher * self.teacher_scaling
        #加偏移值
        if self.teacher_shift is not None:
            teacher = teacher + self.teacher_shift
        return teacher

    def _unscale_teacher(self, teacher_scaled):
        """inverse operation of the _scale_teacher method."""
        #self.out_activation(np.dot(extended_states, self.W_out.T))
        if self.teacher_shift is not None:
            teacher_scaled = teacher_scaled - self.teacher_shift
        if self.teacher_scaling is not None:
            teacher_scaled = teacher_scaled / self.teacher_scaling
        return teacher_scaled

    def fit(self, inputs, outputs, inspect=False):
        """
        Collect the network's reaction to training data, train readout weights.

        Args:
            inputs: array of dimensions (N_training_samples x n_inputs)
            outputs: array of dimension (N_training_samples x n_outputs)
            inspect: show a visualisation of the collected reservoir states

        Returns:
            the network's output on the training data, using the trained weights
        """

        # 将传入的数据标准化
        # 比如，把一维向量(11,)更正为 (11, 1):
        if inputs.ndim < 2:
            inputs = np.reshape(inputs, (len(inputs), -1))
        if outputs.ndim < 2:
            outputs = np.reshape(outputs, (len(outputs), -1))

        #增加偏移值或乘以参数（_scale_inputs，_scale_teacher）
        # transform input and teacher signal:
        inputs_scaled = self._scale_inputs(inputs)
        teachers_scaled = self._scale_teacher(outputs)

        #注释神经网络运行状态(获取储备池状态)
        if not self.silent:
            print("harvesting states...")

        #更新state数组
        # step the reservoir through the given input,output pairs:
        states = np.zeros((inputs.shape[0], self.n_reservoir))
        for n in range(1, inputs.shape[0]):
            states[n, :] = self._update(states[n - 1], inputs_scaled[n, :],
                                        teachers_scaled[n - 1, :])
        # learn the weights, i.e. find the linear combination of collected
        # network states that is closest to the target output
        # 注释神经网络运行状态(获取储备池状态)
        if not self.silent:
            print("fitting...")

        # we'll disregard the first few states:
        # 不考虑前几个状态（阈值）
        transient = min(int(inputs.shape[1] / 10), 100)
        #扩展state，加入原始数据（state之前是在初始化的赋值）
        # include the raw inputs:
        extended_states = np.hstack((states, inputs_scaled))
        #求解Wout
        # Solve for W_out:
        self.W_out = np.dot(np.linalg.pinv(extended_states[transient:, :]),
                            self.inverse_out_activation(teachers_scaled[transient:, :])).T

        #记录最后训练的数据state , input 和 output
        # remember the last state for later:
        self.laststate = states[-1, :]
        self.lastinput = inputs[-1, :]
        self.lastoutput = teachers_scaled[-1, :]

        # optionally visualize the collected states
        if inspect:
            from matplotlib import pyplot as plt
            # (^-- we depend on matplotlib only if this option is used)
            plt.figure(
                figsize=(states.shape[0] * 0.0025, states.shape[1] * 0.01))
            plt.imshow(extended_states.T, aspect='auto',
                       interpolation='nearest')
            plt.colorbar()

        # 注释神经网络运行状态(打印训练误差)
        if not self.silent:
            print("training error:")

        #将求解得到的数组返回到state里面，训练完成更新
        #这里没有采用激活函数，激活函数可以通过 out_activation 来设置
        # apply learned weights to the collected states:
        pred_train = self._unscale_teacher(self.out_activation(
            np.dot(extended_states, self.W_out.T)))

        # 注释神经网络运行状态(打印MSE结果)
        if not self.silent:
            print(np.sqrt(np.mean((pred_train - outputs)**2)))

        return pred_train

    def predict(self, inputs, continuation=True):
        """
        Apply the learned weights to the network's reactions to new input.

        Args:
            inputs: array of dimensions (N_test_samples x n_inputs)
            continuation: if True, start the network from the last training state

        Returns:
            Array of output activations
        """
        #更改数组维度
        if inputs.ndim < 2:
            inputs = np.reshape(inputs, (len(inputs), -1))
        #取得预测样本的数量
        n_samples = inputs.shape[0]

        #两种方法实现，参数选择末尾的数据还是新数据
        if continuation:
            laststate = self.laststate
            lastinput = self.lastinput
            lastoutput = self.lastoutput
        else:
            laststate = np.zeros(self.n_reservoir)
            lastinput = np.zeros(self.n_inputs)
            lastoutput = np.zeros(self.n_outputs)

        #将input，state，output扩展
        inputs = np.vstack([lastinput, self._scale_inputs(inputs)])
        states = np.vstack(
            [laststate, np.zeros((n_samples, self.n_reservoir))])
        outputs = np.vstack(
            [lastoutput, np.zeros((n_samples, self.n_outputs))])

        for n in range(n_samples):
            states[
                n + 1, :] = self._update(states[n, :], inputs[n + 1, :], outputs[n, :])
            outputs[n + 1, :] = self.out_activation(np.dot(self.W_out,
                                                           np.concatenate([states[n + 1, :], inputs[n + 1, :]])))

        return self._unscale_teacher(self.out_activation(outputs[1:]))

    def print_sth(self):
        laststate = self.laststate
        lastinput = self.lastinput
        lastoutput = self.lastoutput
        print("laststate:",laststate.shape)
        print("lastinput:",lastinput.shape)
        print("lastoutput:",lastoutput.shape)
        return 0
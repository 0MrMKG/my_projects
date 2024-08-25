



------

ESN调用框架

------



+ numpy读取csv文件部分

  delimiter是划分两个列之间的区分符号

  skiprows是指跳过前面x行读取数据

  data = data[:,1]是一种切片，逗号1表示取整个表第二列有效的数据

  ```python
  data_path = "datasets//daily-min-temperatures.csv"
  with open(data_path,encoding='utf-8') as f:
      data = np.loadtxt(data_path,dtype = "str" ,delimiter=",",skiprows=1)
      data = data[:,1]
      data = np.array(data[:]).astype('float64')
  ```

+ plt展示所有数据集部分

  + 基本流程：

  ```python
  a = data
  plt.title(data_name)
  plt.xlabel('时间',fontproperties='SimHei',fontsize=20)
  plt.ylabel('温度',fontproperties='SimHei',fontsize=20)
  plt.plot(a)
  plt.show()
  ```

  + 图表设置方法：

    + plt.figure(figsize = (x,y))可以调整图表的xy轴的显示大小（1个单位等于100像素点）

    + plt.xlabel plt.ylabel plt.title

      基本没有参数，fontproperties='SimHei',fontsize=20是为了显示中文字与中文字大小

    + plt.plot参数

      ls：折线图的线条风格

      lw：折线图的线条宽度

      label：标记图内容的标签文本

+ MSE损失函数

  ```python
  def MSE(yhat, y):
      return np.sqrt(np.mean((yhat.flatten() - y)**2))
  ```

+ 训练神经网络部分

  + 主要参数解释：

    + n_reservoir：网络中储备池神经元数量
    + sparsity：稀疏性
    + radius_set： 设置的训练谱半径
    + noise_set:  设置的训练噪声
    + trainlen: 训练读取的数据集大小
    + future：步长
    + futureToTal：总量

  + 训练过程：

    + 初始化loss数组，大小为谱半径数量*噪声数量（展示不同谱半径与噪声情况下的结果）

    + 进入循环，外层为谱半径，内层为不同的噪声，以下论述在双循环内部的操作

      + 创建pred_tot，存储futureTotal个数据（预测数据）

      + 导入ESN类，设置参数

        + 对futureTotal循环，步长为future

        + 开始训练

          类似滑窗法，窗口大小为trainlen，步长为future，总的移动步数为100

          也就是说0到trainlen, future到trainlen+future,...,futureTotal到trainlen+futureTotal

        + 预测数据

          参数传入一个大小为future的全1数组，并且预测

          再把预测结果传入之前定义的future_tot里面

      + 用MSE计算预测值与真实值的大小，输出结果

  

  ```python
  n_reservoir= 500
  sparsity   = 0.2
  rand_seed  = 23
  radius_set = [0.9,  1,  1.1]
  noise_set = [ 0.001, 0.004, 0.006]
  
  radius_set = [0.5, 0.7, 0.9,  1,  1.1,1.3,1.5]
  noise_set = [ 0.0001, 0.0003,0.0007, 0.001, 0.003, 0.005, 0.007,0.01]
  
  radius_set_size  = len(radius_set)
  noise_set_size = len(noise_set)
  
  trainlen = 1500
  future = 2
  futureTotal= 100
  
  loss = np.zeros([radius_set_size, noise_set_size])
  
  for l in range(radius_set_size):
      rho = radius_set[l]
      for j in range(noise_set_size):
          noise = noise_set[j]
  
          pred_tot=np.zeros(futureTotal)
  
          esn = ESN(n_inputs = 1,
            n_outputs = 1,
            n_reservoir = n_reservoir,
            sparsity=sparsity,
            random_state=rand_seed,
            spectral_radius = rho,
            noise=noise)
  
          for i in range(0,futureTotal,future):
              pred_training = esn.fit(np.ones(trainlen),data[i:trainlen+i])
              prediction = esn.predict(np.ones(future))
              pred_tot[i:i+future] = prediction[:,0]
  
          loss[l, j] = MSE(pred_tot, data[trainlen:trainlen+futureTotal])
          print('rho = ', radius_set[l], ', noise = ', noise_set[j], ', MSE = ', loss[l][j] )
  ```

+ 预测数据部分

  + 参数和训练时基本一致，但是谱半径和误差已经被确定了（选一个MSE最小的）

  + 这里只需要一次循环预测数据，以下是内部逻辑:

    【1】预测数据部分：

    使用esn类中的fit参数训练，然后进行predict参数。
    
    再把预测的东西导入到pred_tot里面进行绘制（prediction[:,0]表示第1列数据）
    
    ```python
    for i in range(0,futureTotal,future):
        pred_training = esn.fit(np.ones(trainlen),data[i:trainlen+i])
        prediction = esn.predict(np.ones(future))
        pred_tot[i:i+future] = prediction[:,0]
    ```
    
    【2】绘图部分：
    
    
    
    【X】python知识：
    
    ![image-20230402155323434](https://blogphoto1.oss-cn-shanghai.aliyuncs.com/imgimage-20230402155323434.png)
    
    
    
    ```python
    import seaborn as sns
    from matplotlib import rc
    #rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
    rc('text', usetex=False)
    
    n_reservoir= 500
    sparsity=0.2
    rand_seed=23
    spectral_radius = 1.2
    noise = .0005
    
    
    esn = ESN(n_inputs = 1,
          n_outputs = 1,
          n_reservoir = n_reservoir,
          sparsity=sparsity,
          random_state=rand_seed,
          spectral_radius = spectral_radius,
          noise=noise)
    
    trainlen = 2000
    future = 2
    futureTotal = 200
    pred_tot=np.zeros(futureTotal)
    
    for i in range(0,futureTotal,future):
        pred_training = esn.fit(np.ones(trainlen),data[i:trainlen+i])
        prediction = esn.predict(np.ones(future))
        pred_tot[i:i+future] = prediction[:,0]
    
    plt.figure(figsize=(30,8))
    plt.plot(range(1000,trainlen+futureTotal),data[1000:trainlen+futureTotal],'b',label="Data", alpha=0.3)
    #plt.plot(range(0,trainlen),pred_training,'.g',  alpha=0.3)
    plt.plot(range(trainlen,trainlen+futureTotal),pred_tot,'k',  alpha=0.8, label='Free Running ESN')
    
    lo,hi = plt.ylim()
    plt.plot([trainlen,trainlen],[lo+np.spacing(1),hi-np.spacing(1)],'k:', linewidth=4)
    
    plt.title(r'气温变化预测图', fontsize=25)
    plt.xlabel(r'时间(天)', fontsize=20,labelpad=10)
    plt.ylabel(r'温度', fontsize=20,labelpad=10)
    plt.legend(fontsize='xx-large', loc='best')
    sns.despine()
    ```
    
    

------

pyESN中的ESN类

------

+ 前置的处理函数;

  + 处理变量维度函数

+ ESN类的静态属性：

  ```python
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
  ```

  + 实际传参：

    ​	输入向量维度 n_inputs = 1,
    ​    输出向量维度 n_outputs = 1, 
    ​    储备池参数数量 n_reservoir = n_reservoir,
    ​    稀疏性  sparsity=sparsity,
    ​    随机种子 random_state=rand_seed,

    以下两个作为变量负责每一部分的训练结果，训练结果取最优的MSE：

    ​    谱半径 spectral_radius = spectral_radius,
    ​    训练噪声 noise=noise

    ```python
    n_reservoir= 500
    sparsity=0.2
    rand_seed=23
    spectral_radius = 1.2
    noise = .0005
    
    
    esn = ESN(n_inputs = 1,
          n_outputs = 1, 
          n_reservoir = n_reservoir,
          sparsity=sparsity,
          random_state=rand_seed,
          spectral_radius = spectral_radius,
          noise=noise)
    ```

+ 初始化权重

  

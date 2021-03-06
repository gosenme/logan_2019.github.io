---
title: Deeplearning4j 快速入门-19
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>在之前的课程中，我们为大家介绍的机器学习实例大部分都属于监督学习或者无监督学习。例如图像的分类和目标检测属于监督学习，而词嵌入课程中的 word2vec 和 GloVe 都属于无监督学习。在本次课程中，我们将为大家介绍另一种机器学习的方式——强化学习（Reinforcement Learning）。本节课核心内容包括：</p>
<ul>
<li>强化学习简介</li>
<li>强化学习的实现方式与基本原理</li>
<li>基于 RL4J 的 CartPole 问题建模</li>
</ul>
<p>强化学习也可以称为反馈激励学习或者评价学习，是相对于监督学习和非监督学习更契合人类行为的一种训练学习方式，下面我们将从强化学习的基本原理、实现方式及结合 RL4J 框架给出 CartPole 问题解决方案，从三个方面介绍强化学习的相关知识，并以此作为入门强化学习的案例供大家参考。其中 RL4J 是在 ND4J 基础上构建的深度强化学习开源框架，并隶属于 Deeplearning4j 生态圈，支持 Deep Q-Learning 等多种深度强化学习的方式。下面我们首先介绍强化学习的相关内容。</p>
<h3 id="171">17.1 强化学习简介</h3>
<p>强化学习是区别于监督和非监督学习的另一种机器学习方式。强化学习的主要特点在于其具备根据环境的变化而做出连续决策的能力。从这个意义上讲，强化学习是更加符合人类等智能体学习规律的一种方式，原因在于，智能体的学习方式大多需要经过多次的逻辑推演和决策才能够达到某一具体目标，典型的例子有智能自动控制系统、博弈游戏等。无人车的自动控制系统会根据道路环境的实际状态来做出加速、制动等动作，围棋游戏则需要根据双方的棋局态势做出有利于我方的落子方案。虽然从宏观上讲，强化学习和监督学习一样是要完成对某一目标的学习，但强化学习需要智能体在完成阶段性目标的基础上不断累积才能达成最终目标，就像下棋的每一步都有着暂时的目的及长远的布局两个目标，而不可能仅仅凭借一两步棋来赢得正常比赛。</p>
<p>当然，强化学习的应用场景并不仅仅只有上述几种，在更多的领域如机器翻译、人机多轮交互系统、个性化推荐等问题上，强化学习都有着广泛的应用。另外，随着深度神经网络技术的不断成熟，深度学习与强化学习相结合的解决方案逐渐成为主流的强化学习方案，其中以 DeepMind 的 Deep Q-Learning（DQN）为代表的技术逐渐成为学术界和工业界应用的热点。</p>
<p>下面我们就强化学习的经典理论以及深度强化学习的相关内容为大家做些介绍。</p>
<h3 id="172">17.2 强化学习的实现方式与基本原理</h3>
<p>在介绍具体的算法之前，我们先给出强化学习领域的几个概念。</p>
<ul>
<li>environment：强化学习问题中的外部环境，在具体问题中可以抽象成环境特征向量进行表征。</li>
<li>action：在不同外部环境条件下采取的动作，action 集合可以是连续的也可以是离散集合。</li>
<li>reward：对于 agent 作出的 action 后获取的回报/评价。</li>
<li>agent：智能体的抽象描述，也是做出决策的主体。</li>
</ul>
<p>随着 environment 不断变化，agent 根据当前的 environment 来决定采取的 action，environment 则会根据 action 给到 agent 一定的 reward，这个 reward 可以是一定的正激励，也可以是一定的惩罚，同时因为 agent 采取了一定的 action，因此对 environment 也产生了一定的影响，使得 environment 发生了变化。到此为止，agent 会结合当前的 environment 以及 reward 来决定下一步的 action 是什么，并周而复始，争取将 reward 最大化。这就是强化学习的基本学习过程。</p>
<p>强化学习的学习策略大致可以分为 Value-Based、Policy-Based，以及结合了前两者的 Actor-Critic。</p>
<ul>
<li>Value-Based：最优化 action 所带来的 reward（action-value function，Q-function）来选取 action。</li>
<li>Policy-Based：直接学习 action，通过 Policy Gradient 来更新模型参数。</li>
<li>Actor-Critic：顾名思义可以分为 actor 和 critic 两个部分。actor 直接通过优化 policy 来提升模型表现，critic 则通过估计 value-based function 来达到优化的目的，因此是前两种学习策略的结合。</li>
</ul>
<p>在 Value-Based 学习方法中，Q-Learning 和 Sarsa 是常见的两种算法，这里我们主要讨论 Q-Learning 和深度学习相结合的 Deep Q-Learning。</p>
<p>在强化学习早期，Q-Learning 的核心模块可以表示成一张表——Q-Table。例如下面这张表就是一张典型的 Q-Table：</p>
<p><img src="https://images.gitbook.cn/c70bc050-3f15-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>Q-Table 的含义是，在某一种环境状态 state 下采取某种 action 所带来的潜在奖励 reward。既然强化学习的目标是将 reward 最大化，那么 agent 就需要在不同的 state 状态下选择最有利的 action。以上面这张 Q-Table 为例，我们将这张 Q-Table 作为一个简单的篮球游戏中运动员的比赛价值评估表，假设其中存在两个动作——投篮和过人，存在两种状态——有人防守和无人防守。表中的分值表示在当前的环境状态下选取某个动作的得分。这个得分存在正分和负分。如果你操控的运动员想得到较高的评价分数，那么很明显你需要在不同的环境下选择合理的动作，并通过不断学习你的选择来优化你的 reward。这就是一个比较典型的 Q-Learning 过程，Q 值的更新公式如下：</p>
<pre><code>Q(st,at)←Q(st,at)+α[rt+1+λmaxaQ(st+1,a)−Q(st,at)]
</code></pre>
<p>基于 Q-Table 的传统 Q-Learning 算法是比较直观的，action、state 以及即时的 reward 或者说 Q 值都来自于表格。但我们可以想象，当 action 和 state 的维度不断增加的过程中，整个表格就会急剧膨胀，这对于计算机的存储和计算都将是很大的负担。</p>
<p>因此我们考虑一种方式来自动学习 Q-Table，或者说代替 Q-Table，而深度神经网络是一种很好的选择。Q-Table 从本质上讲是一种离散的函数分布，而我们知道，经过多层非线性变换后的神经网络在理论上有拟合任意函数的能力，因此从理论上神经网络完全可以代替 Q-Table。与深度神经网络结合的强化学习，就是我们通常所说的 DRL（Deep Reinforcement Learning），典型的算法就是 Deep Q-Network/Deep Q-Learning。</p>
<p>Deep Q-Network（DQN）比较具有代表性的论文是 2015 年 DeepMind 发表在 Nature 上的这篇：<a href="https://www.nature.com/articles/nature14236"><em>Human-level control through deep reinforcement learning</em></a>。在 DQN 中有两个重要的策略影响着 DQN 的最终学习效果——Experience replay 和 Fixed Q-targets。Experience replay 主要用于打乱并抽取记忆中的 state，使得训练样本之间避免有着过强的连续性，加快 mini-batch SGD 的收敛速度。Fixed Q-targets 通常在 Double DQN 中使用。使用 Fixed Q-targets 我们同样可以达到打乱连续性的效果，另外我们需要引入两个结构相同的神经网络：eval-net 和 target-net 来分别作为 action 的评估和选择的标准。</p>
<p>上面介绍的 Q-Learning 或者结合神经网络的 DQN/Doule DQN 都是 Value-Based 的策略。Q-Learning 在处理 action 是离散值得问题已经可以有比较好的表现，但是当 action 是连续值或者服从某一分布时则显得力不从心，这种情况下直接预测 action 概率的 Policy-Based 方法更为合适。预测 action 的方式我们可以选择神经网络。</p>
<p>在 Deeplearning4j 的开源深度强化学习项目 RL4J 中，目前主要支持的是 Q-Learning 系列中的 DQN、Double DQN、A3C 和 Async NStepQlearning 算法。在下面第三部分中，我们将基于 RL4J 的框架尝试解决强化学习中的一个经典问题——CartPole 问题。</p>
<h3 id="173rl4jcartpole">17.3 基于 RL4J 的 CartPole 问题建模</h3>
<p>CartPole 问题是强化学习中的一个经典入门问题。它可以被描述为：</p>
<blockquote>
  <p>在一辆小车上竖立一根杆子，然后给小车一个推或者拉的力，使得杆子尽量保持平衡不滑倒。更详细的描述可参见 OpenAI 官网上关于 CartPole 问题的解释：<a href="https://gym.openai.com/envs/CartPole-v0">CartPole V0</a>。</p>
</blockquote>
<p>由于强化学习和以往介绍的监督或者非监督学习不同，需要构建 environment 等参数，所以编写环境非常重要。我们在这里讨论的 CartPole 问题的环境参数可以用 OpenAI 提供的 Gym 来获取。在这里，我们简单介绍下 OpenAI 以及 Gym 的相关信息。</p>
<p><img src="https://images.gitbook.cn/4e1b5060-3f2a-11e9-acbf-6f04514d907d" alt="enter image description here" /></p>
<p>强化学习算法中涉及的环境是非常重要的一类参数，在不同的 environment 条件下训练出来的模型在不同测试环境中的表现肯定会不同，因此作为算法工程师，不仅在一些具体的问题需要环境参数作为训练模型的一个环节，在建模结束后也需要有一个对比模型好坏的标准环境参数。OpenAI 的 Gym 则针对以上问题提供了一个统一的开发环境，包括环境参数和评估模型的环境。目前 Gym 提供 CartPole、MountainCar 等多个经典强化学习问题的标准环境。开发人员可以通过 gym-http-api（<a href="https://github.com/openai/gym-http-api">https://github.com/openai/gym-http-api</a>）提供的 REST 接口获取诸如 CartPole 问题的环境参数。对于 Python 以外的语言调用 Gym 本来并不是十分方便，但 gym-http-api 提供的接口可以方便更多的编程语言获取环境参数。</p>
<p>RL4J 提供了对 gym-http-api 的 Java 语言封装（GitHub 地址：<a href="https://github.com/deeplearning4j/gym-java-client">https://github.com/deeplearning4j/gym-java-client</a>）。对于基于 RL4J 的开发者来说，可以直接调用 Java 接口获取 CartPole 问题的参数。</p>
<pre><code>final String name = "CartPole-v0";
GymEnv&lt;Box, Integer, DiscreteSpace&gt; mdp = new GymEnv&lt;Box, Integer, DiscreteSpace&gt;(name, false, false);
</code></pre>
<p>通过类似以上逻辑声明我们可以获取 Gym 的客户端。需要引入的 Maven 依赖如下：</p>
<pre><code>&lt;properties&gt;
      &lt;project.build.sourceEncoding&gt;UTF-8&lt;/project.build.sourceEncoding&gt; 
      &lt;nd4j.version&gt;0.8.0&lt;/nd4j.version&gt;  
      &lt;dl4j.version&gt;0.8.0&lt;/dl4j.version&gt;   
      &lt;rl4j.version&gt;0.8.0&lt;/rl4j.version&gt;
&lt;/properties&gt;
&lt;dependencies&gt;
    &lt;dependency&gt;  
        &lt;groupId&gt;org.nd4j&lt;/groupId&gt;  
        &lt;artifactId&gt;nd4j-native&lt;/artifactId&gt;   
        &lt;version&gt;${nd4j.version}&lt;/version&gt;  
    &lt;/dependency&gt;  
        &lt;dependency&gt;  
        &lt;groupId&gt;org.deeplearning4j&lt;/groupId&gt;  
        &lt;artifactId&gt;deeplearning4j-core&lt;/artifactId&gt;  
        &lt;version&gt;${dl4j.version}&lt;/version&gt;  
    &lt;/dependency&gt;  
        &lt;dependency&gt;
            &lt;groupId&gt;org.deeplearning4j&lt;/groupId&gt;
            &lt;artifactId&gt;rl4j-core&lt;/artifactId&gt;
            &lt;version&gt;${rl4j.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.deeplearning4j&lt;/groupId&gt;
            &lt;artifactId&gt;rl4j-gym&lt;/artifactId&gt;
            &lt;version&gt;${rl4j.version}&lt;/version&gt;
        &lt;/dependency&gt;
&lt;/dependencies&gt;
</code></pre>
<p>rl4j-gym 和 rl4j-core 是 RL4J 的两个核心依赖，前者用于通过封装好的 Java 客户端获取相应强化学习问题的环境参数，后者是 DQN 等核心算法的实现。需要注意的是，在编写上述 Java 逻辑之前，我们必须首先在本地安装 gym-http-api。安装过程可以参考该项目的 GitHub 首页。下面给出 gym-http-api 安装过程的截图：</p>
<p><img src="https://images.gitbook.cn/55944ea0-408d-11e9-9708-f529efc309cf" alt="enter image description here" /></p>
<p>在 gym-http-api 安装结束后，我们可以开始开发 CartPole 问题的主干逻辑，主要分为以下三个步骤：</p>
<ul>
<li>定义 DQN 网络超参数以及网络结构</li>
<li>声明 Gym 客户端对象并读取环境数据</li>
<li>训练 DQN 并保存模型</li>
</ul>
<p>我们看下以下逻辑：</p>
<pre><code>private static QLearning.QLConfiguration CARTPOLE_QL =
            new QLearning.QLConfiguration(
                    123,    //随机数
                    200,    //单轮最大步长
                    150000, //最大步长
                    150000, //experience replay 的最大步长
                    32,     //batch size
                    500,    //目标更新步长限制
                    10,     //noop warmup 的步长
                    0.01,   //reward 剪裁比例
                    0.99,   //参数 gamma
                    1.0,    //td-error 剪裁
                    0.1f,   //对应 Q-Learning 公式中的参数 epsilon
                    1000,   //epsilon 贪心策略回退的步长限制
                    true    //是否是 Double-DQN
            );

    private static DQNFactoryStdDense.Configuration CARTPOLE_NET = DQNFactoryStdDense.Configuration.builder()                                                            .l2(0.001)                                                          .learningRate(0.0005)
                                       .numHiddenNodes(16)
                                       .numLayer(3)
                                    .build();
    //此处略去部分逻辑
    public static void cartPole() {

        //数据存储器，将训练数据保存在临时目录中
        DataManager manager = new DataManager(true);

        //定义 Gym 对象
        GymEnv&lt;Box, Integer, DiscreteSpace&gt; mdp = null;
        try {
            mdp = new GymEnv&lt;Box, Integer, DiscreteSpace&gt;("CartPole-v0", false, false);
        } catch (RuntimeException e){
            System.out.print("To run this example, download and start the gym-http-api repo found at https://github.com/openai/gym-http-api.");
        }
        //定义训练过程
        QLearningDiscreteDense&lt;Box&gt; dql = new QLearningDiscreteDense&lt;Box&gt;(mdp, CARTPOLE_NET, CARTPOLE_QL, manager);

        //训练 DQN
        dql.train();

        //获取策略
        DQNPolicy&lt;Box&gt; pol = dql.getPolicy();

        //保存模型（以序列化形式）
        pol.save("/tmp/pol1");

        //关闭客户端
        mdp.close();

}
</code></pre>
<p>QLConfiguration 用于定义用于 Q-Learning 相关的配置信息，DQNFactoryStdDense.Configuration 则用于声明神经网络的超参数配置信息。这里的代码定义的是一个三层（只有一层隐藏层）的全连接神经网络。CartPole 方法中我们给出了完整的建模逻辑，在定义 Gym 客户端的基础上，我们根据已经声明好的 Q-Learning 参数以及 DQN 网络结构构建训练场景对象并通过客户端读取 Gym 服务端的 CartPole 环境参数的同时，训练我们定义的三层全连接神经网络。随后我们保存训练结果并关闭客户端。</p>
<p>在训练完模型后，我们自然需要验证或者测试模型，我们可以通过以下逻辑来测试训练效果：</p>
<pre><code>public static void loadCartpole(){

        //重新定义 Gym 环境对象，区别于训练时的 Gym 对象
        GymEnv&lt;Box, Integer, DiscreteSpace&gt; mdp2 = new GymEnv&lt;Box, Integer, DiscreteSpace&gt;("CartPole-v0", true, false);

        //加载训练好的模型（agent）
        DQNPolicy&lt;Box&gt; pol2 = DQNPolicy.load("/tmp/pol1");

        //评估模型
        double rewards = 0;
        for (int i = 0; i &lt; 1000; i++) {
            mdp2.reset();
            double reward = pol2.play(mdp2);
            rewards += reward;
            Logger.getAnonymousLogger().info("Reward: " + reward);
        }

        Logger.getAnonymousLogger().info("average: " + rewards/1000);

        mdp2.close();

}
</code></pre>
<p>我们可以通过 <code>xvfb</code> 命令截取虚拟 monitor 的在每个 action 后的效果拼接起来获得如下的 GIF 动态图：</p>
<p><img src="https://images.gitbook.cn/48490780-3f2b-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<h3 id="174">17.4 小结</h3>
<p>本次课程我们为大家介绍了另一种目前非常流行的人工智能技术——强化学习的相关知识，以及如何结合 Deeplearning4j 生态圈中的强化学习框架 RL4J，来完成一个深度强化学习应用问题的开发。</p>
<p>强化学习相对于之前介绍的监督或者非监督学习而言主要的特点在于连续决策能力，通过当前环境状态来决定采取的动作并希望最终获得最优收益。我们在本次课程中涉及到的 Q-Learning/DQN 及 Policy Gradient 策略都属于 Off-line 学习方式，而诸如 Sarsa 或者 Sarsa（Lambda）等 On-line 算法这里我们并没有做介绍，感兴趣的同学可以查阅相关资料进行进一步的学习。</p>
<p>深度强化学习作为深度神经网络与强化学习结合的产品，目前不仅在传统的一些问题上表现良好，在之前很难解决的大规模强化学习问题上都有着出色的表现。无论是会下围棋的 AlphaGo 还是会打 DOTA2 的 OpenAI-Five，都是深度强化学习在复杂强化学习问题上的成果。</p>
<p>强化学习的学习方式作为更贴近人类决策习惯的一种方式，可能在未来的人工智能发展中起到更为关键的作用。由于我们人类的活动必须存在与周边环境（人、物、事）的不断交互，并在不断交互中做出决策，自我学习并提升，因此强化学习是更加“拟人”的学习方式。当然，AI 的落地往往不会单纯依赖一种策略或者一类学习方式就可以简单完成，因此我们有必要对强化学习这种学习方式给予更多的研究和探索。</p>
<p>相关资料：</p>
<ul>
<li><a href="https://www.nature.com/articles/nature14236"><em>Human-level control through deep reinforcement learning</em></a></li>
<li><a href="https://gym.openai.com/envs/CartPole-v0">CartPole V0</a></li>
<li><a href="https://github.com/openai/gym-http-api">gym-http-api</a></li>
<li><a href="https://github.com/deeplearning4j/gym-java-client">gym-http-api 的 Java 语言封装</a></li>
</ul>
<h3 id="">答疑与交流</h3>
<blockquote>
  <p>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Deeplearning4j 入门》读者交流群，添加<strong>小助手-伽利略</strong>微信：「GitChatty6」，回复关键字「277」给<strong>小助手-伽利略</strong>获取入群资格。</p>
</blockquote></div></article>
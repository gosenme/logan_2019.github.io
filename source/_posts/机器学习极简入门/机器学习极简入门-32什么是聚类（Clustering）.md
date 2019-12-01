---
title: 机器学习极简入门-32
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="clustering">什么是聚类（Clustering）</h3>
<p>聚类并非一种机器学习专有的模型或算法，而是一种统计分析技术，在许多领域得到广泛应用。</p>
<p>广义而言，聚类就是通过对样本静态特征的分析，把相似的对象，分成不同子集（后面我们将聚类分出的子集称为“簇”），被分到同一个子集中的样本对象都具有相似的属性。</p>
<p>在机器学习领域，聚类属于一种无监督式学习算法。</p>
<p>许多聚类算法在执行之前，需要指定从输入数据集中产生的分簇的个数。除非事先准备好一个合适的值，否则必须决定一个大概值，这是当前大多数实践的现状。我们今天要讲的 KMeans 就是如此。</p>
<h3 id="">常用的几种距离计算方法</h3>
<p>通常情况下，在聚类算法中，样本的属性主要由其在特征空间中的相对距离来表示。这就使得距离这个概念，对于聚类非常重要。</p>
<p>在正式讲解聚类算法之前，我们先来看几种最常见的距离计算方法。</p>
<h4 id="2norm">欧氏距离（又称 2-norm 距离）</h4>
<p>在欧几里德空间中，点 $x =(x_1,...,x_n)$ 和 $y =(y_1,...,y_n)$ 之间的欧氏距离为：</p>
<p>$ {d(x,y)={\sqrt {(x_{1}-y_{1})^{2}+(x_{2}-y_{2})^{2}+\cdots +(x_{n}-y_{n})^{2}}}={\sqrt {\sum _{i=1}^{n}(x_{i}-y_{i})^{2}}}} $</p>
<p>在欧几里德度量下，两点之间线段最短。</p>
<h4 id="-1">余弦距离（又称余弦相似性）</h4>
<p>两个向量间的余弦值可以通过使用欧几里德点积公式求出：</p>
<p>${{a} \cdot  {b} =\left\|{a} \right\|\left\|{b} \right\|\cos \theta }  $</p>
<p>所以：</p>
<p>$\cos(\theta)   = \frac{ {a} \cdot  {b}} {|| {a}|| \;||  {b} ||}$</p>
<p>也就是说，给定两个属性向量 $A$ 和 $B$，其余弦距离（也可以理解为两向量夹角的余弦）由点积和向量长度给出，如下所示：</p>
<p>$\cos(\theta )={A\cdot B \over \|A\|\|B\|}={\frac  {\sum \limits _{{i=1}}^{{n}}{A_{i}\times B_{i}}}{{\sqrt  {\sum \limits _{{i=1}}^{{n}}{(A_{i})^{2}}}}\times {\sqrt  {\sum \limits _{{i=1}}^{{n}}{(B_{i})^{2}}}}}}$</p>
<p>这里的 $ A_{i}$ 和 $B_{i}$ 分别代表向量 $A$ 和 $B$ 的各分量。</p>
<p>给出的余弦相似性范围从 $-1$ 到 $1$：</p>
<ul>
<li><p>$-1$ 意味着两个向量指向的方向截然相反；</p></li>
<li><p>$1$ 表示它们的指向是完全相同的；</p></li>
<li><p>$0$ 则表示它们之间是独立的；</p></li>
<li><p>$[-1, 1]$ 之间的其他值则表示中间程度的相似性或相异性。</p></li>
</ul>
<h4 id="manhattandistance1norm">曼哈顿距离（Manhattan Distance, 又称 1-norm 距离）</h4>
<p>曼哈顿距离的定义，来自于计算在规划为方型建筑区块的城市（如曼哈顿）中行车的最短路径。</p>
<p>假设一个城市是完备的块状划分，从一点到达另一点必须要沿着它们之间所隔着的区块的边缘走，没有其他捷径（如下图）：</p>
<p><img src="https://images.gitbook.cn/430f1290-8a78-11e8-974b-497483da0812" alt="enter image description here" /></p>
<p>因此，曼哈顿距离就是：在直角坐标系中，两点所形成的线段对 $x$ 和 $y$ 轴投影的长度总和。</p>
<p>从点 $(x_1, y_1)$ 到点 $(x_2, y_2)$，曼哈顿距离为：</p>
<p>${ \left|x_{1}-x_{2}\right|+\left|y_{1}-y_{2}\right|} $</p>
<h4 id="-2">其他距离</h4>
<p>除了上述最常用的几种距离之外，还有其他多种距离计算方法，例如：Infinity norm（又称 Uniform norm，一致范式）、马氏距离、汉明距离（Hamming Distance）等。</p>
<p>在本课的例子中，计算距离时，如无特别说明，采用的都是欧氏距离。</p>
<h3 id="kmeans">KMeans</h3>
<h4 id="kmeans-1">什么是 KMeans</h4>
<p>简单来说，KMeans 是一种聚类方法，$k$ 是一个常数值，由使用者指定，这种算法负责将特征空间中的 $n$ 个向量聚集到 $k$ 个簇中。</p>
<p>比如，下图就是一个 $k=3$ 的 KMeans 算法聚类前后的情况。</p>
<p><img src="https://images.gitbook.cn/5040e920-8a78-11e8-8838-3badd92eb83e" alt="enter image description here" /></p>
<h4 id="-3">算法步骤</h4>
<p>其算法运行过程大致如下：</p>
<p>Step 0：用户确定 $k$ 值，并将 $n$ 个样本投射为特征空间（一般为欧氏空间）中的 $n$ 个点（$k \leqslant n$）；</p>
<p>Step 1：算法在这 $n$ 个点中随机选取 $k$ 个点，作为初始的“簇核心”；</p>
<p>Step 2：分别计算每个样本点到 $k$ 个簇核心的距离（这里的距离一般取欧氏距离或余弦距离），找到离该点最近的簇核心，将它归属到对应的簇；</p>
<p>Step 3：所有点都归属到簇之后，$n$ 个点就分为了 $k$ 个簇。之后重新计算每个簇的重心（平均距离中心），将其定为新的“簇核心”；</p>
<p>Step 4：反复迭代 Step 2 - Step 3，直到簇核心不再移动为止。</p>
<p>算法的执行过程可用下图直观地表现出来：</p>
<p><img src="https://images.gitbook.cn/60534a60-8a78-11e8-974b-497483da0812" alt="enter image description here" /></p>
<h4 id="-4">计算目标和细节</h4>
<p>上面给出的 Step 3 在一次各个点归入簇中的迭代完成后，要重新计算这个簇的重心位置。</p>
<p>重心位置是根据簇中每个点的平均距离来计算的。这个平均距离如何算出？</p>
<p>要明确算法细节，首先要搞清楚 KMeans 算法的目标——在用户提供了 $k$ 值之后，以一种什么样的原则来将现有的 $n$ 个样本分成 $k$ 簇才是最理想的？</p>
<h5 id="-5"><strong>目标</strong></h5>
<p>有 $n$ 个样本 $(x_1, x_2, …, x_n)$， 每个都是 $d$ 维实向量，KMeans 聚类的目标是将它们分为 $k$ 个簇（$k \leqslant n$)，这些簇表示为 $S = (S_1, S_2, …, S_k)$。</p>
<p>KMeans 算法的目标是使得簇内平方和（Within-cluster Sum of Squares，WCSS ）最小：</p>
<p>$min \sum _{i=1}^{k}\sum _{ {x} \in S_{i}}\left\| {x} -{{\mu }}_{i}\right\|^{2}$</p>
<p>其中 $\mu_i$ 是 $S_i$ 的重心。</p>
<h5 id="-6"><strong>分配</strong></h5>
<p>Step 2 又叫做分配（Assignment）。</p>
<p>设此时为时刻 $t$，$t$ 时刻 $S_i$ 的簇核心为 $\mu_i^{(t)}$。</p>
<p>将某个样本点 $x_p$ 归入到簇 $S_i^{(t)}$ 的原则是：它归入该簇后，对该簇 WCSS 的贡献最小：</p>
<p>$S_{i}^{{(t)}}=\left\{x_{p}:\left\|x_{p}-\mu_{i}^{{(t)}}\right\|^{2}\leqslant \left\|x_{p}-\mu_{j}^{{(t)}}\right\|^{2}  \;\; \forall j,\;\;1\leqslant j\leqslant k\right\}$</p>
<p>因为 WCSS 等于簇中各点到该簇核心的欧氏距离平方和，又因为在每次进行 Step 2 之前，我们已经认定了当时所有簇的簇核心 $\mu_i^{(t)}，i=1,2, ..., k$ 已经存在。</p>
<p>因此只要把 $x_p$ 分配到离它最近的簇核心即可 。</p>
<blockquote>
  <p>注意：尽管在理论上 $ x_{p}$ 可能被分配到 $2$ 个或者更多的簇，但在实际操作中，它只被分配给一个簇。</p>
</blockquote>
<h5 id="-7"><strong>更新</strong></h5>
<p>Step 3 又叫做更新（Update）。</p>
<p>这一步要重新求簇核心，具体计算非常简单，对于该簇中的所有样本求均值就好：</p>
<p>$ \mu_{i}^{{(t+1)}}={\frac  {1}{\left|S_{i}^{{(t)}}\right|}}\sum _{{x_{j}\in S_{i}^{{(t)}}}}x_{j}$</p>
<p>其中 $|S_i|$ 表示 $S_i$ 中样本的个数。</p>
<h4 id="-8">启发式算法</h4>
<blockquote>
  <p><strong>启发式算法（Heuristic Algorithm）</strong>：是一种基于直观或经验构造的算法。</p>
  <p>相对于最优化算法要求得待解决问题的最优解，启发式算法力求在可接受的花费（消耗的时间和空间）下，给出待解决问题的一个可行解，该可行解与最优解的偏离程度一般不能被预计。</p>
  <p>启发式算法常能发现不错的解，但也没办法证明它不会得到较坏的解；它通常可在合理时间解出答案，但也没办法知道它是否每次都可以这样的速度求解。</p>
  <p>虽然有种种不确定性，且其性能无法得到严格的数学证明，但启发式算法直观、简单、易于实现。</p>
  <p>即使在某些特殊情况下，启发式算法会得到很坏的答案或效率极差，然而造成那些特殊情况的数据组合，也许永远不会在现实世界出现。</p>
  <p>因此现实世界中启发式算法常用来解决问题。</p>
</blockquote>
<p>上面我们讲的是最常见的用于实现 KMeans 的启发式算法：Lloyd's 算法。 </p>
<p>Lloyd's 算法是一种很高效的算法，通常情况，它时间复杂度是 $O(nkdi)$，其中 $n$ 为样本数，$k$ 为簇数，$d$ 为样本维度数，而 $i$ 为从开始到收敛的迭代次数。</p>
<p>如果样本数据本身就有一定的聚类结构，那么收敛所需的迭代次数通常是很少的，而且一般前几十次迭代之后，再进行迭代，每次的改进就很小了。 </p>
<p>因此，在实践中，Lloyd's 算法往往被认为是线性复杂度的算法，虽然在最糟糕的情况下时间复杂度是超多项式（Superpolynomial）的。</p>
<p>目前，Lloyd's 算法是 KMeans 聚类的标准方法。</p>
<p>当然，每一次迭代它都要计算每个簇中各个样本到簇核心的距离，这是很耗费算力的。</p>
<p>不过好在，大多数情况下，经过头几轮的迭代后，各个簇就相对稳定了，大多数样本都不会再改变簇归属，可以利用缓存和三角形公理来简化后续的计算。</p>
<h4 id="-9">局限</h4>
<p>KMeans 简单直观，有了启发式算法后，计算复杂度也可以接受，但存在以下问题。</p>
<ul>
<li><p>$k$ 值对最终结果的影响至关重要，而它却必须要预先给定。给定合适的 $k$ 值，需要先验知识，凭空估计很困难，或者可能导致效果很差。</p></li>
<li><p>初始簇核心一般是随机选定的，偏偏它们又很重要，几乎可以说是算法敏感的——一旦选择的不合适，可能只能得到局部的最优解，而无法得到全局的最优解。当然，这也是由 KMeans 算法本身的局部最优性决定的。</p></li>
</ul>
<p>这也就造成了 KMeans 的应用局限，使得它并不适合所有的数据。</p>
<p>例如，对于非球形簇，或者多个簇之间尺寸和密度相差较大的情况，KMeans 就处理不好了。</p>
<h3 id="kmeansknn">实例（对比 KMeans 和 KNN）</h3>
<h4 id="kmeans-2">KMeans 实例</h4>
<p>下面是一个简单的 KMeans 实例，其中的训练样本是10个人的身高（cm）、体重（kg）数据：</p>
<pre><code>    from sklearn.cluster import KMeans
    import numpy as np
    import matplotlib.pyplot as plt

    X = np.array([[185.4, 72.6], [155.0, 54.4], [170.2, 99.9], [172.2, 97.3], [157.5, 59.0], [190.5, 81.6], [188.0, 77.1], [167.6, 97.3], [172.7, 93.3], [154.9, 59.0]])

    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
    y_kmeans = kmeans.predict(X)
    centroids = kmeans.cluster_centers_

    plt.scatter(X[:, 0], X[:, 1], s=50);
    plt.yticks(())
    plt.show()

    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='black', s=200, alpha=0.5);
    plt.show()
</code></pre>
<p>原始训练输入如下：</p>
<p><img src="https://images.gitbook.cn/74f9a4e0-8b37-11e8-a3f8-ff18634ae51e" alt="enter image description here" /></p>
<p>KMeans 聚类后，它们被分到3个簇：</p>
<p><img src="https://images.gitbook.cn/8cd4d260-8b37-11e8-9630-81816a2dcec9" alt="enter image description here" /></p>
<p>我们可以预测一下两个新的样本：</p>
<pre><code>print(kmeans.predict([[170.0, 60], [155.0, 50]]))
</code></pre>
<p>得到输出如下：</p>
<blockquote>
  <p>[1 1]</p>
</blockquote>
<p>1 对应的是哪个簇呢？我们看看训练样本的归属：</p>
<pre><code>    print(y_kmeans)
</code></pre>
<p>输出为：</p>
<blockquote>
  <p>[0 1 2 2 1 0 0 2 2 1]</p>
</blockquote>
<p>可见，1 对应的是分簇图中左下角的那一簇。</p>
<h4 id="knn">KNN 实例</h4>
<p>同样的问题，如果我们要用 KNN 来解决，应该如何呢？我们指望只输入原始身高体重数据是不够的，还必须要给每组数据打上标签，将标签也作为训练样本的一部分。</p>
<p>如何打标签呢？我们就用上面 KMeans 的输出好了：</p>
<pre><code>    from sklearn.neighbors import KNeighborsClassifier

    X = [[185.4, 72.6],
    [155.0, 54.4],
    [170.2, 99.9],
    [172.2, 97.3],
    [157.5, 59.0],
    [190.5, 81.6],
    [188.0, 77.1],
    [167.6, 97.3],
    [172.7, 93.3],
    [154.9, 59.0]]
    y = [0, 1, 2, 2, 1, 0, 0, 2, 2, 1]

    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(X, y)
</code></pre>
<p>然后我们也来预测和 KMeans 例子中同样的新数据：</p>
<pre><code>    print(neigh.predict([[170.0, 60], [155.0, 50]]))
</code></pre>
<p>最后输出结果为：</p>
<blockquote>
  <p>[1 1]</p>
</blockquote></div></article>
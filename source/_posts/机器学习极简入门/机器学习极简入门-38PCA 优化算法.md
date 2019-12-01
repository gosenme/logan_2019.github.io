---
title: 机器学习极简入门-38
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="pca">PCA 优化算法</h3>
<p>已知 PCA 的目标函数是：</p>
<p>$\arg{\min_W  {-\mathbf {tr}(W^TXX^TW)}}$</p>
<p>$s.t. W^TW = I$</p>
<p>PCA 的优化算法要做的就是最优化上面这个函数。</p>
<h4 id="">算法一</h4>
<p>既然优化目标有等式约束条件，那么正好用我们之前学过的拉格朗日乘子法。</p>
<p>我们令：</p>
<p>$L(W) =\mathbf {tr}(W^TXX^TW)+\lambda (W^TW−I) $</p>
<p>然后对 $W$ 求导，并令导函数为$0$可得：$XX^TW = \lambda W$。</p>
<p>这是一个标准的特征方程求解问题，只需要对协方差矩阵 $XX^T$ 进行特征值分解，将求得的特征值排序：$\lambda_1 \geqslant \lambda_2 \geqslant ...  \geqslant \lambda_d$，再取前 $d'$ 个特征值对应的特征向量构成 $W=(w_1, w_2, ..., w_{d'} )$ 即可。</p>
<p>这样我们就求出了 $W$，这就是主成分分析的解！</p>
<blockquote>
  <p>注意：关于矩阵的特征值和特征向量，请参见 《<a href="https://gitbook.cn/books/59ed598e991df70ecd5a0049/index.html">机器学习常用「线性代数」知识速查手册</a>》第4部分。</p>
</blockquote>
<p><strong>算法描述</strong>如下。</p>
<p>【输入】：</p>
<ul>
<li><p>$d$ 维空间中 $n$ 个样本数据的集合 $D = \{x^{(1)}, x^{(2)}, ..., x^{(n)} \}$；</p></li>
<li><p>低维空间的维数 $d'$ ，这个数值<strong>通常由用户指定</strong>。</p></li>
</ul>
<p>【过程】：</p>
<ol>
<li><p>对所有原始样本做中心化：$x^{(i)} :=  x^{(i)}  - \frac{1}{n}\sum_{i=1}^{n} x^{(i)}  $；</p></li>
<li><p>计算样本的协方差矩阵：$XX^T$；</p></li>
<li><p>协方差矩阵 $XX^T$ 进行特征值分解；</p></li>
<li><p>取最大的 $d'$ 个特征值对应的特征向量 $w^{(1)}, w^{(2)}, ..., w^{(d')}$。</p></li>
</ol>
<p>【输出】：</p>
<p>$W=(w^{(1)}, w^{(2)}, ..., w^{(d')} )$</p>
<h4 id="-1">算法二</h4>
<p>上述求解过程可以换一个角度来看。</p>
<p>先对协方差矩阵 $\sum_{i=1}^{n}x^{(i)}{x^{(i)}}^T$ 做特征值分解，取最大特征值对应的特征向量 $w_1$；再对 $\sum_{i=1}^{n}x^{(i)}{x^{(i)}}^T - \lambda_1 w_1w_1^T$ 做特征值分解，取其最大特征值对应的特征向量 $w_2$；以此类推。</p>
<p>因为 $W$ 的各个分量正交，因此 $\sum_{i=1}^{n}x^{(i)}{x^{(i)}}^T = \sum_{j=1}^{d} \lambda_j w_jw_j^T$。</p>
<p>故而解法二和解法一等价。</p>
<h3 id="pca-1">PCA 的作用</h3>
<p>PCA 将 $d$ 维的原始空间数据转换成了$d'$ 维的新空间数据，无疑丧失了部分数据。</p>
<p>根据上面讲的算法我们知道，经过 PCA 后，原样本集协方差矩阵进行特征值分解后，倒数 $(d - d')$ 个特征值对应的特征向量被舍弃了。</p>
<p>因为舍弃了这部分信息，导致的结果是：</p>
<ul>
<li><p>样本的采样密度增大——这是降维的首要动机；</p></li>
<li><p>最小的那部分特征值所对应的特征向量往往与噪声有关，舍弃它们有降噪的效果。 </p></li>
</ul>
<h3 id="singularvaluedecompositionsvd">奇异值分解（Singular Value Decomposition, SVD）</h3>
<p>SVD 是线性代数中一种重要的<strong>矩阵分解方法</strong>，在信号处理、统计学等领域有重要应用。</p>
<h4 id="svd">SVD 的三个矩阵</h4>
<p>我们先来看看 SVD 方法本身。</p>
<p>假设 $M$ 是一个 $m\times n$ 阶实矩阵，则存在一个分解使得：</p>
<p>$M_{m \times n} = U_{m \times m}  \Sigma_{m \times n} {V^T_{n \times n}}$</p>
<p><img src="https://images.gitbook.cn/5ed5df10-af4c-11e8-a51c-93c39f2785b1" alt="enter image description here" /></p>
<p>其中，$\Sigma$ 是一个 $m \times n$ 的非负实数对角矩阵，$\Sigma$ 对角线上的元素是矩阵 $M$ 的奇异值：</p>
<p>$\Sigma = diag{( \sigma_i)}, \;\;i=1, 2, ..., \min{(m,n)} $</p>
<blockquote>
  <p>注意：对于一个非负实数 $\sigma$ 而言，仅当存在 $m$ 维的单位向量 $u$ 和 $n$ 维的单位向量 $v$，它们和 $M$ 及 $\sigma$ 有如下关系时：</p>
  <p>$Mv = \sigma u \,\text{ 且 } M^{T}u= \sigma v$</p>
  <p>我们说 $\sigma$ 是 $M$ 矩阵的奇异值，向量 $u$ 和 $v$ 分别称为 $\sigma$ 的<strong>左奇异向量</strong>和<strong>右奇异向量</strong>。</p>
  <p>一个 $m\times n$ 的矩阵至多有 $\min{(m,n)}$ 个不同的奇异值。</p>
</blockquote>
<p>$U$ 是一个 $m \times m$ 的酉矩阵，它是一组由 $M$ 的左奇异向量组成的正交基：$U = (u_1, u_2, ..., u_m)$。</p>
<p>它的每一列 $u_i$ 都是 $\Sigma$ 中对应序号的对角值 $\sigma_i$ 关于 $M$ 的左奇异向量。</p>
<p>$V$ 是一个 $n \times n$ 的酉矩阵，它是一组由 $M$ 的右奇异向量组成的正交基：$V = (v_1, v_2, ... v_n)$。</p>
<p>它的每一列 $v_i$ 都是 $\Sigma$ 中对应序号的对角值 $\sigma_i$ 关于$M$的右奇异向量。</p>
<blockquote>
  <p><strong>何为酉矩阵？</strong></p>
  <p>若一个 $n \times n$ 的实数方阵 $U$ 满足 $U^TU= UU^T = I_n$，则 $U$ 称为酉矩阵。</p>
</blockquote>
<h4 id="-2">三个矩阵间的关系</h4>
<p>我们这样来看：</p>
<p>$M = U\Sigma V^T$</p>
<p>$M^T = {(U\Sigma V^T)}^T = V{\Sigma}^TU^T$</p>
<p>$MM^T = U\Sigma V^TV{\Sigma}^TU^T $</p>
<p>又因为 $U$ 和 $V$ 都是酉矩阵，所以：</p>
<p>$MM^T = U(\Sigma \Sigma^T)U^T$</p>
<p>同理：$M^TM = V(\Sigma^T \Sigma)V^T$。</p>
<p>也就是说 $U$ 的列向量是 $MM^T$ 的特征向量；$V$ 的列向量是 $M^TM$ 的特征向量；而 $\Sigma$ 的对角元素，是 $M$ 的奇异值，也是 $MM^T$ 或者 $M^TM$ 的非零特征值的平方根。</p>
<h4 id="svd-1">SVD 的计算</h4>
<p>SVD 的手动计算过程大致如下：</p>
<ol>
<li>计算 $MM^T$ 和 $M^TM$；</li>
<li>分别计算 $MM^T$ 和 $M^TM$ 的特征向量及其特征值；</li>
<li>用 $MM^T$ 的特征向量组成 $U$，$M^TM$ 的特征向量组成 $V$；</li>
<li>对 $MM^T$ 和 $M^TM$ 的非零特征值求平方根，对应上述特征向量的位置，填入 $\Sigma$ 的对角元。</li>
</ol>
<p>更详细的过程和计算实例还可以参照<a href="http://web.mit.edu/be.400/www/SVD/Singular_Value_Decomposition.htm">这里</a>。 </p>
<h3 id="svdpca">用 SVD 实现 PCA</h3>
<p>所谓降维度，就是按照重要性排列现有特征，舍弃不重要的，保留重要的。</p>
<p>上面讲了 PCA 的算法，很关键的一步就是对协方差矩阵进行特征值分解，不过其实在实践当中，我们通常用对样本矩阵 $X$ 进行奇异值分解来代替这一步。</p>
<p>$X$ 是原空间的样本矩阵，$W$ 是投影矩阵，而 $T$ 是降维后的新样本矩阵，有 $ T= XW$。</p>
<p>我们直接对 $X$ 做 SVD，得到：</p>
<p>$T = XW = U\Sigma W^TW$</p>
<p>因为 $W$ 是标准正交基组成的矩阵，因此：$T =U\Sigma W^TW = U\Sigma$。</p>
<p>我们选矩阵 $U$ 前 $d'$ 列，和 $\Sigma$ 左上角前 $d' \times d'$ 区域内的对角值，也就是前 $d'$ 大的奇异值，然后直接降维：</p>
<p>$T_{d'}=U_{d'}\Sigma_{d'}$</p>
<p>这样做很容易解释其<strong>物理意义</strong>：样本数据的特征重要性程度既可以用特征值来表征，也可以用奇异值来表征。</p>
<p>动机也很清楚，当然是成本。直接做特征值分解需要先求出协方差矩阵，当样本或特征量大的时候，计算量很大。更遑论对这样复杂的矩阵做特征值分解的难度了。</p>
<p>而对矩阵 $M$ 进行 SVD 时，直接对 $MM^T$ 做特征值分解，要简单得多。</p>
<p>当然 SVD 算法本身也是一个接近 $O(m^3)$（假设 $m&gt;n$）时间复杂度的运算，不过现在 SVD 的并行运算已经被实现，效率也因此提高了不少。</p>
<h3 id="svd-2">直接用 SVD 降维</h3>
<p>除了可以用于 PCA 的实现，SVD 还可以直接用来降维。</p>
<p>在现实应用中，SVD 也确实被作为降维算法大量使用。</p>
<p>有一些应用，直接用眼睛就能看得见。比如：用 SVD 处理图像，减少图片信息量，而又尽量不损失关键信息。</p>
<p>图片是由像素（Pixels）构成的，一般彩色图片的单个像素用三种颜色（Red、Green、Blue）描述，每一个像素点对应一个 RGB 三元值。一张图片可以看作是像素的二维点阵，正好可以对应一个矩阵。那么我们用分别对应 RGB 三种颜色的三个实数矩阵，就可以定义一张图片。</p>
<p>设 $X_R、X_G、X_B$ 是用来表示一张图片的 RGB 数值矩阵，我们对其做 SVD：</p>
<p>$X_R = U_R \Sigma_R V_R^T$</p>
<p>然后我们指定一个参数：$k$，$U_R$ 和 $V_R$ 取前 $k$ 列，形成新的矩阵 $U^k_R$ 和 $V^k_R$，$\Sigma_R$ 取左上 $k \times k$ 的区域，形成新矩阵 $\Sigma^k_R$，然后用它们生成新的矩阵：</p>
<p>$X'_R = U^k_R \Sigma^k_R ({V^k_R})^T $</p>
<p>对 $X_G$ 和 $X_B$ 做同样的事情，最后形成的 $X'_R、X'_G 和 X'_B$ 定义的图片，就是压缩了信息量后的图片。</p>
<blockquote>
  <p>注意：如此处理后的图片尺寸未变，也就是说 $X'_R、X'_G、 X'_B$ 与原本的 $X_R、X_G、X_B$ 行列数一致，只不过矩阵承载的信息量变小了。</p>
  <p>比如，$X_R$ 是一个 $m \times n$ 矩阵，那么 $U_R$ 是 $m \times m$ 矩阵， $\Sigma_R$ 是 $m \times n$ 矩阵， 而 $ V_R^T $ 是 $n \times n$ 矩阵，$U^k_R$ 是 $m \times k$ 矩阵， $\Sigma^k_R$ 是 $k \times k$ 矩阵， 而 $ ({V^k_R})^T $ 是 $k \times n$ 矩阵，它们相乘形成的矩阵仍然是 $m \times n$ 矩阵。</p>
  <p>从数学上讲，经过 SVD 重构后的新矩阵，相对于原矩阵秩（Rank）下降了。</p>
</blockquote>
<h3 id="svdpca-1">SVD &amp; PCA 实例</h3>
<p>下面我们来看一个压缩图片信息的例子，比如压缩下面这张图片：</p>
<p><img src="https://images.gitbook.cn/1e8e2090-a6c1-11e8-a6df-e5b5930cc16b" alt="enter image description here" /></p>
<p>我们将分别尝试 SVD 和 PCA 两种方法。</p>
<h4 id="svd-3">SVD 压缩图片</h4>
<p>我们用 SVD 分解上面这张图片，设不同的 $k$ 值，来看分解后的结果。</p>
<p>下面几个结果的 $k$ 值分别是：$100、50、20 和 5$。</p>
<p>很明显，$k$ 取 $100$ 的时候，损失很小，取 $50$ 的时候还能看清大致内容，到了 $20$ 就模糊得只能看轮廓了，到了 $5$ 则是一片条纹。</p>
<p><img src="https://images.gitbook.cn/54ab46d0-a6c1-11e8-9a57-fbf83638d2ea" alt="enter image description here" /></p>
<p>代码如下：</p>
<pre><code>    import os
    import threading

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import sys

    def svdImageMatrix(om, k):
        U, S, Vt = np.linalg.svd(om)
        cmping = np.matrix(U[:, :k]) * np.diag(S[:k]) * np.matrix(Vt[:k,:])    
        return cmping

    def compressImage(image, k):
        redChannel = image[..., 0]
        greenChannel = image[..., 1]
        blueChannel = image[..., 2]

        cmpRed = svdImageMatrix(redChannel, k)
        cmpGreen = svdImageMatrix(greenChannel, k)
        cmpBlue = svdImageMatrix(blueChannel, k)

        newImage = np.zeros((image.shape[0], image.shape[1], 3), 'uint8')

        newImage[..., 0] = cmpRed
        newImage[..., 1] = cmpGreen
        newImage[..., 2] = cmpBlue

        return newImage

    path = 'liye.jpg'
    img = mpimg.imread(path)

    title = "Original Image"
    plt.title(title)
    plt.imshow(img)
    plt.show()

    weights = [100, 50, 20, 5]

    for k in weights:
        newImg = compressImage(img, k)

        title = " Image after =  %s" %k
        plt.title(title)
        plt.imshow(newImg)
        plt.show()    

        newname = os.path.splitext(path)[0] + '_comp_' + str(k) + '.jpg'
        mpimg.imsave(newname, newImg)
</code></pre>
<h4 id="pca-2">PCA 压缩图片</h4>
<p>用 PCA 压缩同一张图片。</p>
<p>我们使用：</p>
<pre><code>from sklearn.decomposition import PCA
</code></pre>
<p>过程部分，只要将上面代码中的 <code>svdImageMatrix()</code> 替换为如下 <code>pca()</code> 即可：</p>
<pre><code>    def pca(om, cn):

        ipca = PCA(cn).fit(om)
        img_c = ipca.transform(om)

        print img_c.shape
        print np.sum(ipca.explained_variance_ratio_)

        temp = ipca.inverse_transform(img_c)
        print temp.shape

        return temp
</code></pre>
<p>cn 对应 <code>sklearn.decomposition.PCA</code> 的 <code>n_components</code> 参数，指的是 PCA 算法中所要保留的主成分个数 n，也就是保留下来的特征个数 n。</p>
<p>我们仍然压缩四次，具体的 cn 值还是 <code>[100, 50, 20, 5]</code>。</p>
<p>从运行的结果来看，和 SVD 差不多。</p>
<p><img src="https://images.gitbook.cn/af0a2320-a6c7-11e8-9a57-fbf83638d2ea" alt="enter image description here" /></p>
<p>其实好好看看 sklearn.decomposition.PCA 的代码，不难发现，它其实就是用 SVD 实现的。</p></div></article>
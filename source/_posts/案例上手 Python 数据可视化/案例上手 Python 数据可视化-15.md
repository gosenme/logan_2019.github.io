---
title: 案例上手 Python 数据可视化-15
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>第一部分和第二部分所学的 Matplotlib 和 Seaborn 工具，是具有师承关系的两个数据可视化库，在实际项目中，可根据自己的喜好选择使用。本课将用它来展示两个实际的案例，从中窥见数据可视化在数据分析方面的威力。</p>
<h3 id="251">2.5.1 分析马拉松跑步数据</h3>
<p>在本课程的 github.com 数据仓库中，有此处所使用的数据集，<a href="https://github.com/qiwsir/DataSet/tree/master/marathon">请单击这里自行下载</a>。</p>
<pre><code class="python language-python">import pandas as pd
marathon = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/marathon/marathon.csv")
marathon.head()
</code></pre>
<p><img src="https://images.gitbook.cn/FuWF4kxZ5PYbNAxtiYoBtSK4wwTx" alt="avatar" /></p>
<p>这个数据集有以下几个特征：</p>
<ul>
<li>age，运动员的年龄</li>
<li>gender，运动员的性别</li>
<li>split，半程所用时间</li>
<li>final，全程所用时间，即最终成绩</li>
</ul>
<p>在对这些数据进行分析之前，要先了解数据集的基本情况，即数据清洗——这是数据科学的重要环节。</p>
<pre><code class="python language-python">marathon.info()

# out
&lt;class 'pandas.core.frame.DataFrame'&gt;
RangeIndex: 37250 entries, 0 to 37249
Data columns (total 4 columns):
age       37250 non-null int64
gender    37250 non-null object
split     37250 non-null object
final     37250 non-null object
dtypes: int64(1), object(3)
memory usage: 1.1+ MB
</code></pre>
<p>从返回信息可知，在 marathon 数据集中，没有缺失数据。但是，split 和 final 两个特征中的数据，不是数字类型。“01:05:38” 这是用字符串的形式表示了所用时间长度（一小时五分钟三十八秒），对于这种数据类型的特征，需要进行转化，首先转换为时间类型：</p>
<pre><code class="python language-python">import datetime
def convert_time(s):
    h,m,s = map(int, s.split(":"))
    return datetime.timedelta(hours=h, minutes=m, seconds=s)
</code></pre>
<p>然后重新读入数据集，并使用 pd.read_csv 函数中的参数 converters，实现对 split 和 final 两个特征数据类型的转化。</p>
<pre><code class="python language-python">marathon = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/marathon/marathon.csv", 
                       converters={"split":convert_time, "final":convert_time})

marathon.dtypes

#out
age                 int64
gender             object
split     timedelta64[ns]
final     timedelta64[ns]
dtype: object
</code></pre>
<p>从数据结果中可知，此时再次得到的 marathon 数据集的 split 和 final 特征已经是 timedelta64 类型的数据了。</p>
<p>但是，这种时间类型的数据，仍然不是最终的，还要继续转化，将时间间隔的表述转化为整数，比如以秒为单位的整数。时间间隔转化为整数，通常用这样的方式进行：</p>
<pre><code class="python language-python">d = datetime.timedelta(hours=1,minutes=0,seconds=0)
df = pd.DataFrame({'time':[d]})
df.astype(int)

# out
             time
0    3600000000000
</code></pre>
<p>其实这个结果不是以秒为单位的，而是以“纳秒”（ns）为单位：</p>
<p>$$
1s = 10^9 ns
$$</p>
<p>因此，要得到以秒为单位的整数，需要如此操作：</p>
<pre><code class="python language-python">d = datetime.timedelta(hours=1,minutes=0,seconds=0)
df = pd.DataFrame({'time':[d]})
df.astype(int) * 1e-9

# out
       time
0    3600.0
</code></pre>
<p>于是，对于 marathon 数据集，依据上述方式，将 split 和 final 两个特征的数据进行转化。</p>
<pre><code class="python language-python"># 将 split 和 final 的特征值转化为秒为单位的整数
marathon['split_sec'] = marathon['split'].astype(int) * 1e-9
marathon['final_sec'] = marathon['final'].astype(int) * 1e-9
marathon.head()
</code></pre>
<p><img src="https://images.gitbook.cn/FlX9zzFPAEHgAVkG866P7b68JWKG" alt="avatar" /></p>
<p>在 marathon 中增加了两个特征，它们的数据就是以秒为单位的浮点数，在后续的分析中，分别使用这些数据。</p>
<p><strong>1. 描述统计</strong></p>
<p>这是了解这个数据集的第一步。</p>
<pre><code class="python language-python">marathon.describe()
</code></pre>
<p><img src="https://images.gitbook.cn/FpX45oWyG7-hMIuBVqj5FsgjeeuM" alt="avatar" /></p>
<p>或许会眼前一亮，age 中的最大值居然是 86，看来有必要看一看此特征的数据分布。</p>
<pre><code class="python language-python">%matplotlib inline
import seaborn as sns
ax = sns.boxplot(x=marathon['age'])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9950a4b0-3e47-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>从 age 列的数据箱线图中可以看出，的确有一些“离群值”——高龄运动员，向他们致敬。</p>
<p><strong>2. 数据分布</strong></p>
<p>然后通过直方图，研究数据分布，比如 split_sec 和 final_sec。</p>
<pre><code class="python language-python">sns.distplot(marathon['split_sec'])
</code></pre>
<p><img src="https://images.gitbook.cn/ab4de600-3e47-11e9-a98d-5dc2d0f56a42" alt="enter image description here" /></p>
<pre><code class="python language-python">sns.distplot(marathon['final_sec'])
</code></pre>
<p><img src="https://images.gitbook.cn/bd10b660-3e47-11e9-a98d-5dc2d0f56a42" alt="enter image description here" /></p>
<p>总体上看，两个特征下的数据都符合正态分布，但是 final_sec 的分布图比较“胖”——说明什么？请参考有关统计学知识。</p>
<p>根据已学知识，我们还可以把 gender 这个分类特征添加进来，于是就看到了这样的分布图：</p>
<pre><code class="python language-python">sns.violinplot(x='gender', y='final_sec', data=marathon)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/cb5e3620-3e47-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>从结果中可以看出来，从总体上讲，男性运动员比女性运动员跑的还是快一点。</p>
<p><strong>3. 寻找优秀的原因</strong></p>
<p>根据一个同事介绍——他是一名每年都要跑一两个马拉松的，在我看来已经是大神了。马拉松运动员很关注整个赛程中前后半程的时间比较，好的选手是后半程用时和前半程应该近似。因此，我们也来研究一下，在 marathon 数据集中，这些运动员的前后半程用时情况。</p>
<pre><code class="python language-python">g = sns.jointplot("split_sec", "final_sec", data=marathon, kind='hex')   #or: kind='scatter'

#绘制一条直线，作为参考
import numpy as np
g.ax_joint.plot(np.linspace(4000, 16000), np.linspace(8000, 32000), ":k")   
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/dce9f0f0-3e47-11e9-a7c2-ef0a2addb332" width = "60%" /></p>
<p>图中横坐标表示 split_sec 特征，即半程用时；纵轴表示 final_sec 特征，即全程用时。从图中可以看出，的确是越优秀的运动员，前半程用时越接近全程用时的一半——还有少数后半程跑得更快的。</p>
<p>为了更深入研究，再做一个计算：</p>
<pre><code class="python language-python">marathon['split_frac'] = 1 - 2 * marathon['split_sec'] / marathon["final_sec"]
marathon.head()
</code></pre>
<p><img src="https://images.gitbook.cn/Fvw2TSRPxR40fKF6VcrQEh56-jKN" alt="avatar" /></p>
<p>下面就用直方图看一看 split_frac 特征中的数据分布，并且增加一个参考线。</p>
<pre><code class="python language-python">import matplotlib.pyplot as plt
sns.distplot(marathon['split_frac'], kde=False)
plt.axvline(0, color='k', linestyle="--")   # 垂直于 x 轴的直线，0 表示 x 轴位置
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/f33b9840-3e47-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>这张图更清晰地显示了全体参赛者的运动时间安排——这是优秀运动必须知道的。</p>
<p>探究规律，就少不了研究不同特征之间的关系。</p>
<pre><code class="python language-python">sns.pairplot(data=marathon, 
             vars=['age', 'split_sec', 'final_sec', 'split_frac'], 
             hue='gender')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/0c29bc60-3e48-11e9-a98d-5dc2d0f56a42" width = "80%" /></p>
<p>前面提到过，在这个数据集中，有 80 多岁的选手。</p>
<pre><code class="python language-python">(marathon.age &gt;= 80).sum()

#out
15
</code></pre>
<blockquote>
  <p>老当益壮！</p>
</blockquote>
<p>下面就划分一下年龄段，看看各年龄段的成绩分布。</p>
<pre><code class="python language-python">marathon['age_dec'] = marathon['age'].map(lambda age: 10 * (age // 10))
sns.violinplot(x="age_dec", y="split_frac", hue="gender", data=marathon, 
               split=True, inner='quartile', palette=['lightblue', 'lightpink'])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/1b7ff990-3e48-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>观察这个图中各个年龄段不同性别的运动员的 split_frac 特征数据分布，会发现一个有趣的现象，年龄越大，前后段的时间分布比相对集中。</p>
<p>下面是全程用时分布比较：</p>
<pre><code class="python language-python">sns.violinplot(x="age_dec", y="final_sec", hue="gender", data=marathon, 
               split=True, inner='quartile', palette=['lightblue', 'lightpink'])
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/2b4db0b0-3e48-11e9-a7c2-ef0a2addb332" alt="enter image description here" /></p>
<blockquote>
  <p>“廉颇老矣，尚能饭否”。</p>
</blockquote>
<p>以上仅是对 marathon 数据进行研究的举例，还可以从更多的角度去研究，或许会有更有意思的结论。</p>
<h3 id="252pokeman">2.5.2 可视化 Pokeman 数据</h3>
<p><a href="https://github.com/qiwsir/DataSet/tree/master/pokemon">本案例的数据集下载地址，请单击这里</a>。</p>
<p>读入数据：</p>
<pre><code class="python language-python">pokemon = pd.read_csv("/Users/qiwsir/Documents/Codes/DataSet/pokemon/pokemon.csv", 
                      index_col=0, encoding='cp1252')
pokemon.head()
</code></pre>
<p><img src="https://images.gitbook.cn/FpQxMWPG_ucuTQgvpX9EfYA8up1N" alt="avatar" /></p>
<p>然后对此数据集的各个特征类型了解一下：</p>
<pre><code class="python language-python">pokemon.info()

#out
&lt;class 'pandas.core.frame.DataFrame'&gt;
Int64Index: 151 entries, 1 to 151
Data columns (total 12 columns):
Name         151 non-null object
Type 1       151 non-null object
Type 2       67 non-null object
Total        151 non-null int64
HP           151 non-null int64
Attack       151 non-null int64
Defense      151 non-null int64
Sp. Atk      151 non-null int64
Sp. Def      151 non-null int64
Speed        151 non-null int64
Stage        151 non-null int64
Legendary    151 non-null bool
dtypes: bool(1), int64(8), object(3)
memory usage: 19.3+ KB
</code></pre>
<p>Type 2 这个特征有缺失值，其他的没有，而且显示为整数型，这就很符合数据分析的要求了。</p>
<p>尝试做一个散点图，主要是研究特征 Attack 和 Defense 的关系。</p>
<pre><code class="python language-python">sns.lmplot(x='Attack', y='Defense', data=pokemon, fit_reg=False, hue='Stage')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/3ef0b2c0-3e48-11e9-9475-090a8c8aed3a" width = "75%" /></p>
<p>需要提醒的是，本来 sns.lmplot 是绘制“散点图 + 回归曲线”的，但是，参数中使用了 fit_reg=False，就不再包含回归线了——虽然在 Seaborn 中没有单独绘制散点图的专门方法，但是通过这里的参数设置，就实现了散点图的绘制。</p>
<p>如果要用箱线图看看各个特征数据分布，可以这样做：</p>
<pre><code class="python language-python">sns.boxplot(data=pokemon)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/503eef60-3e48-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>从结果中可以看出，特征 Total、Stage 和 Legendary 的数据不适合在这里绘制散点图，因此需要对特征进行适当选择。</p>
<pre><code class="python language-python">stats_pokemon = pokemon.drop(['Total', 'Stage', 'Legendary'], axis=1)
sns.boxplot(data=stats_pokemon)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/5fdd3210-3e48-11e9-9475-090a8c8aed3a" alt="enter image description here" /></p>
<p>现在，就能比较清晰地看出几个特征的数据分布情况了——对于非数字的特征，自动摒弃。</p>
<p>在 Seaborn 中，还有一种研究数据分布的函数 sns.violinplot，下面用它绘制特征“Attack”相对于特征“Type 1”中的数据（这是一个分类型特征）的分布。</p>
<pre><code class="python language-python">pokemon['Type 1'].unique()

#out
array(['Grass', 'Fire', 'Water', 'Bug', 'Normal', 'Poison', 'Electric',
       'Ground', 'Fairy', 'Fighting', 'Psychic', 'Rock', 'Ghost', 'Ice',
       'Dragon'], dtype=object)
</code></pre>
<p>以上显示了特征“Type 1”中唯一数据，即数据的值。</p>
<pre><code class="python language-python">sns.set(style='whitegrid', rc={'figure.figsize':(11.7,8.27)}) 
pkmn_type_colors = ['#78C850',  # Grass
                    '#F08030',  # Fire
                    '#6890F0',  # Water
                    '#A8B820',  # Bug
                    '#A8A878',  # Normal
                    '#A040A0',  # Poison
                    '#F8D030',  # Electric
                    '#E0C068',  # Ground
                    '#EE99AC',  # Fairy
                    '#C03028',  # Fighting
                    '#F85888',  # Psychic
                    '#B8A038',  # Rock
                    '#705898',  # Ghost
                    '#98D8D8',  # Ice
                    '#7038F8',  # Dragon
                   ]
sns.violinplot(x="Type 1", y='Attack', 
               data=pokemon, 
               inner = None, # 移除提琴图中的竖棒
               palette=pkmn_type_colors)
sns.swarmplot(x="Type 1", y='Attack', 
              data=pokemon, 
              color = 'k', # 表示数据的点的颜色
              alpha =.7   # 透明度
              )

plt.title('Attack by Type')
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/6f7189b0-3e48-11e9-a98d-5dc2d0f56a42" width = "80%" /></p>
<p>有没有注意到，这次的图比前面的大了一些？控制图变大的就是 sns.set 函数中的参数 rc={'figure.figsize':(11.7,8.27)}。</p>
<p>变量 pkmn_type_colors 是一个列表，其中列出了一些颜色，每一个颜色值对应着特征“Type 1”中的唯一值——见 pokemon['Type 1'].unique() 的结果。</p>
<p>为了让最终所绘制的图不至于太乱，设置函数 sns.violinplot 的参数 inner = None，移除提琴图内部的竖线（棒），并且以参数 palette=pkmn_type_colors 设置每个提琴图的颜色。</p>
<p>在前面，已经得到了变量 stats_pokemon 引用的一个数据集，相对于原来的 pokemon，删除了三个特征。</p>
<pre><code class="python language-python">stats_pokemon.head()
</code></pre>
<p><img src="https://images.gitbook.cn/FuBLfGEdFGoE8Rmzo4zv6TdyyIST" alt="avatar" /></p>
<p>输出结果表明，特征“HP  Attack  Defense  Sp. Atk  Sp. Def  Speed”都是整数（在 pokemon.info() 已经显示出）。现在有这样一种需求，如何将这些特征的数据分布进行可视化，并放到一个坐标系中比较？请思考。</p>
<p>或许你有了一种方案，下面的演示仅供参考。</p>
<p>先用 pd.melt 函数，将所指定的特征进行归并。</p>
<pre><code class="python language-python">melted_pokemon = pd.melt(stats_pokemon, 
                    id_vars=["Name", "Type 1", "Type 2"], # 保留的特征
                    var_name="Stat") # 其余特征规定到此列
melted_pokemon.sample(10)
</code></pre>
<p><img src="https://images.gitbook.cn/FgcmOPy4ki01Q-Ssc-ZqvoKL8d_C" alt="avatar" /></p>
<p>这样，在 melted_pokemon 数据集中的 “Stat” 特征中的数据，就是分类数据，它们的值是 stats_pokemon 中被归并的特征名称。</p>
<pre><code class="python language-python">melted_pokemon['Stat'].unique()

#out
array(['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
      dtype=object)
</code></pre>
<p>在这个基础上，用 sns.swarmplot 函数绘制反映分类特征数据分布的图示。</p>
<pre><code class="python language-python">sns.swarmplot(x='Stat', y='value', data=melted_pokemon)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/80f5f180-3e48-11e9-a98d-5dc2d0f56a42" width = "80%" /></p>
<p>如果使用 hue 参数，可以在上图基础上，再叠加一层分类。</p>
<pre><code class="python language-python">sns.swarmplot(x='Stat', y='value', data=melted_pokemon, hue='Type 1')
plt.legend(bbox_to_anchor=(1, 1), loc=2)
</code></pre>
<p>输出结果：</p>
<p><img src="https://images.gitbook.cn/9055a490-3e48-11e9-a7c2-ef0a2addb332" width = "80%" /></p>
<p>除了上述几项分析之外，还可以有很多分析维度，不妨根据自己的理解，在本示例基础上继续深入。</p>
<h3 id="">总结</h3>
<p>本课演示了两个案例，旨在引导读者综合运用已经学习过的知识。如果已经阅读到这里，为了强化所学，下面的建议希望能够被采纳：</p>
<ul>
<li>任选本课中的一个数据集，依据自己的设想——通过观察数据的特征，找自己的想法，运用各种知识，以可视化方式分析数据；</li>
<li>到本课的在线数据集中下载某个其他数据，对其进行分析，并可视化。</li>
</ul>
<h3 id="-1">答疑与交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《Python数据可视化》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「288」给小助手伽利略获取入群资格。</strong></p>
</blockquote></div></article>
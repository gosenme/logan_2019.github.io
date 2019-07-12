---
title: nlp之 stanfordnlp和CoreNLP
---

### 下载CoreNLP
- [下载地址](https://stanfordnlp.github.io/CoreNLP/index.html#download)
- 使用`unzip`解压

### 安装Java(java 8或以上)
- Mac安装
    ```text
    brew update
    brew install jenv
    brew cask install java
    ```

### 打开CoreNLP服务
- 命令
    
        java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,pos,lemma,parse,sentiment" -port 9000 -timeout 30000


### stanfordnlp
- [README](https://github.com/stanfordnlp/stanfordnlp)

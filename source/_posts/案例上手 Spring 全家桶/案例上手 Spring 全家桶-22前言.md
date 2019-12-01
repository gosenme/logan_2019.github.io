---
title: 案例上手 Spring 全家桶-22
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><h3 id="">前言</h3>
<p>上一讲我们学习了如何使用 MyBatis 框架，这一讲一起来探究 MyBatis 框架的底层原理，仿照 MyBatis，自己写一个操作数据库的小工具，自己写框架的主要目的在于学习 MyBatis 底层源码的设计思想，提高自己对框架的认知，进一步理解框架，进而更好地应用框架进行实际开发。</p>
<p>由于篇幅有限，本讲我带领大家来完成一个 Demo 实现 MyBatis 的主要功能，MyBatis 作为一个“半自动化”的 ORM 框架，其特点是开发者手动在 Mapper.xml 中定义 SQL 语句，再结合 Mapper.xml，通过 Mapper 动态代理来实现自定义接口的功能。</p>
<p>所以我们自己写的框架具备如下功能：</p>
<ul>
<li>自定义接口</li>
<li>在 XML 文件中定义接口方法对应的 SQL 语句</li>
<li>根据 XML，通过 JDK 动态代理完成自定义接口的具体实现</li>
<li>自动解析结果集，映射成 XML 中配置的 POJO</li>
</ul>
<p>主要功能搞清楚之后，我们来分析需要用到哪些技术。</p>
<ul>
<li>XML 解析是一定需要的，这也是企业级框架中几乎都会用到的技术</li>
<li>Mapper 代理机制我们通过 JDK 动态代理来实现</li>
<li>结果集解析为 POJO，那必然需要用到反射机制</li>
</ul>
<p>在实际开发中，使用 MyBatis 和传统 JDBC 的方式最大区别在于接口不需要开发者自己实现了，由 MyBatis 自动实现，这就极大地简化了开发步骤，我们通过下面这个例子对比一下。</p>
<p><strong>传统 JDBC 开发方式</strong>。</p>
<p>（1）自定义接口</p>
<pre><code class="java language-java">public interface UserDAO {
    public User get(int id);
}
</code></pre>
<p>（2）根据接口自定义实现类</p>
<pre><code class="java language-java">public class UserDAOImpl implements UserDAO{

    @Override
    public User get(int id) {
        Connection conn = JDBCTools.getConnection();
        String sql = "select * from user where id = ?";
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            pstmt = conn.prepareStatement(sql);
            pstmt.setInt(1, id);
            rs = pstmt.executeQuery();
            if(rs.next()){
                int sid = rs.getInt(1);
                String name = rs.getString(2);
                User user = new User(sid,name);
                return user;
            }
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }finally{
            JDBCTools.release(conn, pstmt, rs);
        }
        return null;
    }

}
</code></pre>
<p>（3）实例化接口对象，完成相关操作</p>
<pre><code class="java language-java">public static void main(String[] args) {
        UserDAO userDAO = new UserDAOImpl();
        User user = userDAO.get(1);
        System.out.println(user);
}
</code></pre>
<p><strong>接下来我们看看 MyBatis 的开发方式</strong>。</p>
<p>（1）自定义接口</p>
<pre><code class="java language-java">public interface StudentDAO {
    public Student getById(int id);
    public Student getByStudent(Student student);
    public Student getByName(String name);
    public Student getByStudent2(Student student);
}
</code></pre>
<p>（2）不需要定义实现类，将实现类需要执行的 SQL 语句定义在 XML 文件中</p>
<pre><code class="xml language-xml">&lt;?xml version="1.0" encoding="UTF-8" ?&gt;
&lt;!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd"&gt; 
&lt;mapper namespace="com.southwind.dao.StudentDAO"&gt; 

    &lt;select id="getById" parameterType="int" 
        resultType="com.southwind.entity.Student"&gt;
        select * from student where id=#{id}
    &lt;/select&gt;

    &lt;select id="getByStudent" parameterType="com.southwind.entity.Student" 
        resultType="com.southwind.entity.Student"&gt;
        select * from student where id=#{id} and name=#{name}
    &lt;/select&gt;

    &lt;select id="getByStudent2" parameterType="com.southwind.entity.Student" 
        resultType="com.southwind.entity.Student"&gt;
        select * from student where name=#{name} and tel=#{tel} 
    &lt;/select&gt;

    &lt;select id="getByName" parameterType="java.lang.String" 
        resultType="com.southwind.entity.Student"&gt;
        select * from student where name=#{name}
    &lt;/select&gt;

&lt;/mapper&gt;
</code></pre>
<p>（3）通过 JDK 动态代理获取接口的实例化对象，完成相关操作</p>
<pre><code class="java language-java">public static void main(String[] args) {
    StudentDAO studentDAO = (StudentDAO) new MyInvocationHandler().getInstance(StudentDAO.class);
    Student stu = studentDAO.getById(1);
    System.out.println(stu);
}
</code></pre>
<p>通过上述对比我们可以直观地感受到两种开发方式的区别，要实现上述 MyBatis 的核心功能，动态创建代理对象是关键所在。这就需要用到 JDK 动态代理，运行时结合接口和 Mapper.xml 来动态创建一个代理对象，程序调用该代理对象的方法来完成业务。</p>
<h4 id="-1">具体实现步骤</h4>
<p>创建一个类，实现 InvocationHandler 接口，该类就具备了创建动态代理对象的功能，定义两个核心方法。</p>
<p>（1）自定义 getInstance 方法：入参为目标对象，通过 Proxy.newProxyInstance 方法创建代理对象，并返回。</p>
<pre><code class="java language-java">public Object getInstance(Class cls){
  Object newProxyInstance = Proxy.newProxyInstance(  
    cls.getClassLoader(),  
    new Class[] { cls }, 
    this); 
  return (Object)newProxyInstance;
}
</code></pre>
<p>（2）实现接口的 invoke 方法，通过反射机制完成业务逻辑代码。</p>
<pre><code class="java language-java">@Override
public Object invoke(Object proxy, Method method, Object[] args)
  throws Throwable {
  // TODO Auto-generated method stub
  return null;
}
</code></pre>
<p>invoke 方法是核心代码，在该方法中实现具体的业务需求，接下来我们来看如何实现。</p>
<p>既然是对数据库进行操作，则一定需要数据库连接对象，数据库相关信息配置在 config.xml 中。因此 invoke 方法第一步，就是要解析 config.xml，创建数据库连接对象，使用 C3P0 数据库连接池。</p>
<pre><code class="java language-java">//读取 C3P0 数据源配置信息
public static Map&lt;String,String&gt; getC3P0Properties(){
  Map&lt;String,String&gt; map = new HashMap&lt;String,String&gt;();
  SAXReader reader = new SAXReader();
  try {
    Document document = reader.read("src/config.xml");
    //获取根节点
    Element root = document.getRootElement();
    Iterator iter = root.elementIterator();
    while(iter.hasNext()){
      Element e = (Element) iter.next();
      //解析 environments 节点
      if("environments".equals(e.getName())){
        Iterator iter2 = e.elementIterator();
        while(iter2.hasNext()){
          //解析 environment 节点
          Element e2 = (Element) iter2.next();
          Iterator iter3 = e2.elementIterator();
          while(iter3.hasNext()){
            Element e3 = (Element) iter3.next();
            //解析 dataSource 节点
            if("dataSource".equals(e3.getName())){
              if("POOLED".equals(e3.attributeValue("type"))){
                Iterator iter4 = e3.elementIterator();
                //获取数据库连接信息
                while(iter4.hasNext()){
                  Element e4 = (Element) iter4.next();
                  map.put(e4.attributeValue("name"),e4.attributeValue("value"));
                }
              }
            }
          }
        }
      }
    }
  } catch (Exception e) {
    // TODO Auto-generated catch block
    e.printStackTrace();
  }
  return map; 
}
</code></pre>
<pre><code class="java language-java">//获取 C3P0 信息，创建数据源对象
Map&lt;String,String&gt; map = ParseXML.getC3P0Properties();
ComboPooledDataSource datasource = new ComboPooledDataSource();
datasource.setDriverClass(map.get("driver"));
datasource.setJdbcUrl(map.get("url"));
datasource.setUser(map.get("username"));
datasource.setPassword(map.get("password"));
datasource.setInitialPoolSize(20);
datasource.setMaxPoolSize(40);
datasource.setMinPoolSize(2);
datasource.setAcquireIncrement(5);
Connection conn = datasource.getConnection();
</code></pre>
<p>有了数据库连接，接下来就需要获取待执行的 SQL 语句，SQL 的定义全部写在 StudentDAO.xml 中。</p>
<p>第二步，继续解析 XML，执行 SQL 语句，SQL 执行完毕，查询结果会保存在 ResultSet 中，还需要将 ResultSet 对象中的数据进行解析，封装到 POJO 中返回，这一功能同样需要两步操作。</p>
<p>（1）反射机制创建 Student 对象。</p>
<p>（2）通过反射动态执行类中所有属性的 setter 方法，完成赋值。</p>
<p>这样就将 ResultSet 中的数据封装到 POJO 中了。</p>
<pre><code class="java language-java">//获取 sql 语句
String sql = element.getText();
//获取参数类型
String parameterType = element.attributeValue("parameterType");
//创建 pstmt
PreparedStatement pstmt = createPstmt(sql,parameterType,conn,args);
ResultSet rs = pstmt.executeQuery();
if(rs.next()){
    //读取返回数据类型
    String resultType = element.attributeValue("resultType");   
    //反射创建对象
    Class clazz = Class.forName(resultType);
    obj = clazz.newInstance();
    //获取 ResultSet 数据
    ResultSetMetaData rsmd = rs.getMetaData();
    //遍历实体类属性集合，依次将结果集中的值赋给属性
    Field[] fields = clazz.getDeclaredFields();
    for(int i = 0; i &lt; fields.length; i++){
        Object value = setFieldValueByResultSet(fields[i],rsmd,rs);
        //通过属性名找到对应的 setter 方法
        String name = fields[i].getName();
        name = name.substring(0, 1).toUpperCase() + name.substring(1);
        String MethodName = "set"+name;
        Method methodObj = clazz.getMethod(MethodName,fields[i].getType());
        //调用 setter 方法完成赋值
        methodObj.invoke(obj, value);
        }
}
</code></pre>
<p>代码的实现大致思路如上所述，具体实现起来有很多细节需要处理。使用到两个自定义工具类：ParseXML、MyInvocationHandler，完整代码请直接下载源码查看。</p>
<p><strong>创建数据表</strong></p>
<pre><code class="sql language-sql">CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `tel` varchar(20) DEFAULT NULL,
  `address` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) 

INSERT INTO `student` VALUES 
(1,'张三',2,90,'13512345678','科技路'),
(2,'李四',9,96,'18300001234','高新路'),
(3,'王五',2,98,'13612345671','科技路');
</code></pre>
<p><strong>现在进行测试</strong></p>
<p>（1）StudnetDAO.getById 方法</p>
<pre><code class="java language-java">public static void main(String[] args) {
    StudentDAO studentDAO = (StudentDAO) new MyInvocationHandler().getInstance(StudentDAO.class);
    Student stu = studentDAO.getById(1);
    System.out.println(stu);
}
</code></pre>
<p>代码中的 studentDAO 为动态代理对象，此对象通过 MyInvocationHandler().getInstance(StudentDAO.class) 方法动态创建，并且结合 StudentDAO.xml 实现了 StudentDAO 接口的全部方法，直接调用 studentDAO 对象的方法即可完成业务需求，结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/ee463640-acf3-11e9-b015-0198f673a736" width = "70%" /></p>
<p>（2）StudnetDAO.getByName 方法</p>
<pre><code class="java language-java">public static void main(String[] args) {
    StudentDAO studentDAO = (StudentDAO) new MyInvocationHandler().getInstance(StudentDAO.class);
    Student stu = studentDAO.getByName("李四");
    System.out.println(stu);
}
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/4e141f10-acf4-11e9-a760-01c165706a91" width = "70%" /></p>
<p>（3）StudnetDAO.getByStudent 方法（根据 id 和 name 查询）</p>
<pre><code class="java language-java">public static void main(String[] args) {
    StudentDAO studentDAO = (StudentDAO) new MyInvocationHandler().getInstance(StudentDAO.class);
    Student student = new Student();
    student.setId(1);
    student.setName("张三");
    Student stu = studentDAO.getByStudent(student);
    System.out.println(stu);
}
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/6fb177d0-acf4-11e9-8f3f-792c82c0addc" width = "70%" /></p>
<p>（4）StudnetDAO.getByStudent2 方法（根据 name 和 tel 查询）</p>
<pre><code class="java language-java">public static void main(String[] args) {
    StudentDAO studentDAO = (StudentDAO) new MyInvocationHandler().getInstance(StudentDAO.class);
    Student student = new Student();
    student.setName("李四");
    student.setTel("18367895678");
    Student stu = studentDAO.getByStudent2(student);
    System.out.println(stu);
}
</code></pre>
<p>结果如下图所示。</p>
<p><img src="https://images.gitbook.cn/92adeb60-acf4-11e9-a760-01c165706a91" width = "70%" /></p>
<p>以上就是仿 MyBatis 实现自定义小工具的大致思路，细节之处还需具体查看源码。</p>
<h3 id="-2">总结</h3>
<p>本讲我们自己手写了一个 MyBatis 框架，虽然功能并不完整，但是 MyBatis 的核心机制是有的，通过自己写 MyBatis 框架，我们可以更加深刻地理解框架的底层原理，进而可以更好地使用 MyBatis 框架进行实际开发，同时框架底层代码优秀的编程思想也是非常值得我们学习和借鉴的。</p>
<p><a href="https://github.com/southwind9801/MyBatisImitate.git">请单击这里下载源码</a></p>
<h3 id="-3">分享交流</h3>
<blockquote>
  <p><strong>为了方便与作者交流与学习，GitChat 编辑团队组织了一个《快速上手 Spring 全家桶》读者交流群，添加小助手-伽利略微信：「GitChatty6」，回复关键字「200」给小助手-伽利略获取入群资格。</strong></p>
  <p>阅读文章过程中有任何疑问随时可以跟其他小伙伴讨论，或者直接向作者提问（作者看到后抽空回复）。你的分享不仅帮助他人，更会提升自己。</p>
</blockquote></div></article>
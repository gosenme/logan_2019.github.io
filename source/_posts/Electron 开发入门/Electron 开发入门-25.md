---
title: Electron 开发入门-25
---
<article id="topicContainer" class="column_content"><h2 class="topic_title"></h2><div><p>本节课将利用全局快捷键实现一款贪吃蛇的游戏，下面先看下游戏主界面的截图。</p>
<p>Mac OS X 的效果如图所示。</p>
<p><img src="https://images.gitbook.cn/Fo7ee2_CS-e1LjdWD3rhHngzi35N"  width = "50%" /></p>
<p>Windows 的效果如图所示。</p>
<p><img src="https://images.gitbook.cn/FhHGAmvrLDXU3drOeeDzlMKKsASY"  width = "50%" /></p>
<p>全局快捷键需要通过 globalShortcut 对象注册，使用下面的代码可以得到 globalShortcut 对象。</p>
<pre><code>const {globalShortcut} = require('electron');
</code></pre>
<p>接下来使用 globalShortcut.register 方法注册全局快捷键，代码如下。</p>
<pre><code>globalShortcut.register('CommandOrControl+P', () =&gt; {
    ... ...
  });
</code></pre>
<p>本例的游戏是在 Renderer 进程中实现的，而注册全局快捷键是在主进程中完成的，因此主进程要想与 Renderer 进程进行通信，就需要 send 方法向 Renderer 进程发送消息，然后 Renderer 进程再拦截这个消息，并做进一步处理。</p>
<p>下面看一下本例的完整实现代码。</p>
<ul>
<li>入口脚本文件（index.js）</li>
</ul>
<p>在 index.js 文件中除了创建窗口对象（BrowserWindow 对象），装载主页面外，还注册了全局快捷键。</p>
<pre><code>const {app, globalShortcut, BrowserWindow} = require('electron');

let mainWindow = null;

app.on('window-all-closed', () =&gt; {
  if (process.platform !== 'darwin') app.quit();
});

app.on('ready', () =&gt; {
  mainWindow = new BrowserWindow({
    width: 840,
    height: 470,
    useContentSize: true
  });
  mainWindow.loadURL(`file://${__dirname}/index.html`);
  mainWindow.on('closed', () =&gt; { mainWindow = null; });
 //注册全局快捷键，在 Mac OS X 下是 &lt;Comand+P&gt;，在 Windows 和 Linux 下是 &lt;Control+P&gt;
  const pauseKey = 
globalShortcut.register('CommandOrControl+P', () =&gt; {
    //向Renderer进程发送消息，要求暂停或开始游戏
    mainWindow.webContents.send('togglePauseState');
  });
  //判断注册全局快捷键是否失败
  if (!pauseKey) alert('不同通过键盘暂停游戏');
});

app.on('will-quit', () =&gt; {
  globalShortcut.unregister('CommandOrControl+P');
});
</code></pre>
<ul>
<li>主页面（index.html）</li>
</ul>
<pre><code>&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;贪吃蛇&lt;/title&gt;
    &lt;link href="index.css" rel="stylesheet" /&gt;
    &lt;script src="event.js"&gt;&lt;/script&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;div id="scoreboard"&gt;
      &lt;span id="label"&gt;分数:&lt;/span&gt;
      &lt;span id="score"&gt;&lt;/span&gt;
            &lt;div id="bar"&gt;
                  &lt;div id="play_menu"&gt;
                      &lt;button onclick="pause();"&gt;暂停&lt;/button&gt;
                  &lt;/div&gt;
                  &lt;div id="pause_menu"&gt;
                    &lt;button onclick="play();"&gt;恢复&lt;/button&gt;
                    &lt;button onclick="restart();"&gt;重新开始&lt;/button&gt;
                  &lt;/div&gt;
                  &lt;div id="restart_menu"&gt;
                    &lt;button onclick="restart();"&gt;重新开始&lt;/button&gt;
                  &lt;/div&gt;
                &lt;/div&gt;
            &lt;/div&gt;
    &lt;/div&gt;
    &lt;canvas &gt;&lt;/canvas&gt;
  &lt;/body&gt;
&lt;/html&gt;
</code></pre>
<p>在 index.html 页面中放置了一些按钮，用来控制游戏的暂停、播放和重新开始。</p>
<ul>
<li>event.js 脚本文件</li>
</ul>
<pre><code>let currentState;   //当前的状态（暂停还是正在运行中）
let canvas, ctx, gridSize, currentPosition, snakeBody, snakeLength, direction, score, suggestedPoint, allowPressKeys, interval, choice;
//更新分数，规则是吃掉一次食物，就加 10 分
function updateScore () {
  //贪吃蛇初始长度为 3，snakeLength 是当前的长度，每吃掉一次食物，长度加 1，因此计算分数可以用贪吃蛇长度的增量计算  
  score = (snakeLength - 3) * 10;
  document.getElementById('score').innerText = score;
}
//判断贪吃蛇是否碰到了食物，suggestedPoint 表示当前事物的位置
function hasPoint (element) {
  return (element[0] === suggestedPoint[0] &amp;&amp; element[1] === suggestedPoint[1]);
}
//随机放置食物
function makeFoodItem () {
  suggestedPoint = [Math.floor(Math.random()*(canvas.width/gridSize))*gridSize, Math.floor(Math.random()*(canvas.height/gridSize))*gridSize];
  if (snakeBody.some(hasPoint)) {
    makeFoodItem();
  } else {
    ctx.fillStyle = 'rgb(10,100,0)';
    ctx.fillRect(suggestedPoint[0], suggestedPoint[1], gridSize, gridSize);
  }
}
//判断贪吃蛇是否吃了自己，如果是，则 gameover  
function hasEatenItself (element) {
  return (element[0] === currentPosition.x &amp;&amp; element[1] === currentPosition.y);
}
//算出左移的坐标
function leftPosition(){
 return currentPosition.x - gridSize;
}
//算出右移的坐标
function rightPosition(){
  return currentPosition.x + gridSize;
}
//算出上移的坐标
function upPosition(){
  return currentPosition.y - gridSize;
}
//算出下移的坐标
function downPosition(){
  return currentPosition.y + gridSize;
}

function whichWayToGo (axisType) {
  if (axisType === 'x') {
    choice = (currentPosition.x &gt; canvas.width / 2) ? moveLeft() : moveRight();
  } else {
    choice = (currentPosition.y &gt; canvas.height / 2) ? moveUp() : moveDown();
  }
}
//向上移动贪吃蛇
function moveUp(){
  if (upPosition() &gt;= 0) {
    executeMove('up', 'y', upPosition());
  } else {
    whichWayToGo('x');
  }
}
//向下移动贪吃蛇
function moveDown(){
  if (downPosition() &lt; canvas.height) {
    executeMove('down', 'y', downPosition());
  } else {
    whichWayToGo('x');
  }
}
//向左移动贪吃蛇
function moveLeft(){
  if (leftPosition() &gt;= 0) {
    executeMove('left', 'x', leftPosition());
    } else {
    whichWayToGo('y');
  }
}
//向右移动贪吃蛇
function moveRight(){
  if (rightPosition() &lt; canvas.width) {
    executeMove('right', 'x', rightPosition());
  } else {
    whichWayToGo('y');
  }
}
//开始移动贪吃蛇，dirValue 是移动的方向，axisType 表示坐标轴类型，'x' 或 'y'，axisValue 表示移动的值
function executeMove(dirValue, axisType, axisValue) {
  direction = dirValue;
  currentPosition[axisType] = axisValue;
  //绘制贪吃蛇
  drawSnake();
}
//定时器的回调函数，每 100 毫秒会调用一次
function moveSnake(){
  switch (direction) {
    case 'up':    //向上移动
      moveUp();
      break;
    case 'down':  //向下移动
      moveDown();
      break;
    case 'left':    //向左移动
      moveLeft();
      break;
    case 'right':  //向右移动
      moveRight();
      break;
  }
}
//重新开始游戏
function restart () {
    document.getElementById('play_menu').style.display='block';
    document.getElementById('pause_menu').style.display='none';
    document.getElementById('restart_menu').style.display='none';
    pause();
    start();
}
//暂停游戏
function pause(){
    document.getElementById('play_menu').style.display='none';
    document.getElementById('pause_menu').style.display='block';
  clearInterval(interval);
  allowPressKeys = false;
}
//开始游戏
function play(){
    document.getElementById('play_menu').style.display='block';
    document.getElementById('pause_menu').style.display='none';
    interval = setInterval(moveSnake,100);
    allowPressKeys = true;
}
//游戏结束
function gameOver(){
  pause();
  window.alert('游戏结束，您的分数： ' + score);
  ctx.clearRect(0,0, canvas.width, canvas.height);
    document.getElementById('play_menu').style.display='none';
  document.getElementById('restart_menu').style.display='block';
}
//绘制贪吃蛇的一个小块，贪吃蛇不是一次绘制成的，每次只绘制一个小块，每 100 毫秒绘制一次
function drawSnake() {
  if (snakeBody.some(hasEatenItself)) {
    gameOver();
    return false;
  }
  snakeBody.push([currentPosition.x, currentPosition.y]);
  ctx.fillStyle = 'rgb(200,0,0)';

  ctx.fillRect(currentPosition.x, currentPosition.y, gridSize, gridSize);
  if (snakeBody.length &gt; snakeLength) {
    let itemToRemove = snakeBody.shift();
    //当蛇移动后，将蛇的最后一个块清除
    ctx.clearRect(itemToRemove[0], itemToRemove[1], gridSize, gridSize);
  }
  if (currentPosition.x === suggestedPoint[0] &amp;&amp; currentPosition.y === suggestedPoint[1]) {
    makeFoodItem();
    snakeLength += 1;
    updateScore();
  }
}
//设置页面的键盘事件
window.document.onkeydown = function(event) {
  if (!allowPressKeys){
    return null;
  }
  let keyCode;
  if(!event)
  {
    keyCode = window.event.keyCode;
  }
  else
  {
    keyCode = event.keyCode;
  }

  switch(keyCode)
  {
    case 37:  //按左箭头键

      //不能倒退
      if (direction !== 'right') {
        moveLeft();
      }
      break;

    case 38:  //按上箭头键
      if (direction !== 'down'){
        moveUp();
      }
      break;

    case 39:   //按右箭头键
      if (direction !== 'left'){
        moveRight();
      }
      break;

    case 40:   //按上箭头键
      if (direction !== 'up'){
        moveDown();
      }
      break;
    default:
      break;
  }
};
//开始游戏
function start () {
  ctx.clearRect(0,0, canvas.width, canvas.height);
  currentPosition = {'x':50, 'y':50};
  snakeBody = [];
  snakeLength = 3;
  updateScore();
  makeFoodItem();
  drawSnake();
  direction = 'right';
  play();
}
//页面初始化函数
function initialize () {
  canvas = document.querySelector('canvas');
  ctx = canvas.getContext('2d');
  gridSize = 10;
  start();
}
//接收主进程发过来的消息
function togglePauseState () {
  if (currentState) {
    if (currentState === 'play') {
      pause();
           currentState = 'pause';
    } else {
      play();
           currentState = 'play';
    }
   } else {
     pause();
     currentState = 'play';
   }
}

const ipcRenderer = require('electron').ipcRenderer;
//接收主进程发过来的消息
ipcRenderer.on('togglePauseState', togglePauseState);
window.onload = initialize;
</code></pre>
<p>现在运行程序，按 <code>&lt;Command+P&gt;</code> 或 <code>&lt;Control + P&gt;</code> 以及页面左上角的按钮，可以暂停和恢复游戏。</p>
<p><a href="https://github.com/geekori/electron_gitchat_src">点击这里下载源代码</a></p></div></article>
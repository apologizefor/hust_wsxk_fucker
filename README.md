# 华科公选自动选课

我是在补选阶段使用的这个工具。它包含一个简陋的python脚本用来自动监视-自动抢课，和一个fish script脚本用来多线程启动python脚本(一般不必要)。和一个极其简陋的fish script用来在交易时爆破单个课程。

### 自动监视

进入选课页面，选择按课堂选课，拿下你请求`*.action`用的cookie，填进python的cookie_str。

将你不想要的类别和你不想要的课，填进python的blacklist.

直接启动python脚本，它自动监视，自动给你选上。你也可以使用go.fish。阅读go.fish来了解它做了什么和如何使用。

### 交易时对单个课程的爆破

这部分无需脚本。我只是3分钟简单写了一下。

在交易之前，chrome或chromium浏览器F12，监视network。然后点击那个课程的选课。在出现的请求里面右键那个到*.action的post请求，选copy -> copy as curl。然后替换`fuck_one_course.fish`的第7行。别忘了在后面加上 `> $log_fname`。

然后暴力开多进程。看输出log的速度稳定之后，让卖家退课。

```
for i in (seq 128)
    ./fuck_one_course.fish &
end
```

这时候脚本会瞬间爆炸。我不想修，反正你的课选上了。杀死它们，打游戏去。

### note

这个脚本只在Linux, Python 3.7.2能正常工作。在ubuntu, python 3.6.5就会爆炸，原因是unicode的处理。

但是我不想维护这个脚本。它价值不大，仅供偶尔使用。如果你愿意修了它，just open a pr.



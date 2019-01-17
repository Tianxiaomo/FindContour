## sad

tensorflow的静态图属性导致在模型中不能使用其他的代码添加到模型中，所以只能自己实现在分割图中打框的操作。本来opencv是有的，效果不错，运行效率也很高。

直接使用opencv findContours 和 minAreaRect 方法从分割结果获取box

![image](http://tuku-image-mo.oss-cn-beijing.aliyuncs.com/19-1-15/81013970.jpg)

## 造车

由于模型中间层不能使用opencv，所以自己写了个findContours，效果如下图

从分割图中分离每一个物体
![image](https://s2.ax1x.com/2019/01/15/FzoHXQ.png)

![image](http://tuku-image-mo.oss-cn-beijing.aliyuncs.com/19-1-15/1073672.jpg)

### 使用PCA求出分离出物体的主轴，然后画矩形

<figure class="fourth">
    <img src="http://tuku-image-mo.oss-cn-beijing.aliyuncs.com/19-1-15/90762611.jpg">
    <img src="http://tuku-image-mo.oss-cn-beijing.aliyuncs.com/19-1-15/66646162.jpg">
    <img src="http://tuku-image-mo.oss-cn-beijing.aliyuncs.com/19-1-16/65241962.jpg">
</figure>

## 效果

![image](http://tuku-image-mo.oss-cn-beijing.aliyuncs.com/19-1-16/33143832.jpg)

​	过滤掉太小的目标

![image](http://tuku-image-mo.oss-cn-beijing.aliyuncs.com/19-1-16/60318716.jpg)

## 运行效率，由于是python写的，自己测试测运行时间是opencv的两倍
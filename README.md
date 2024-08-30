# “Learning_logs“ 项目笔记

----------
## 1  建立项目 ##

### 1.1  制定规范 ###

在着手编写大型Web项目时,首先需要制定**规范**。我们制定的规范如下：

-   编写一个名为“学习笔记”的Web应用程序，让用户能够记录感兴趣的主题，并在学习每个主题的过程中添加日志条目。

-   “学习笔记”的主页对网站进行描述，并邀请用户注册或登录。

-   用户登录后，可以创建新主题，添加新条目以及阅读既有条目

### 1.2  虚拟环境

**建立虚拟环境**

为项目新建一个文件夹，命名为learning_logs，在终端中切换到这个目录，并执行如下代码创建一个虚拟环境：

`python -m venv ll_env`

**激活虚拟环境**

Windows系统下执行如下代码：

`ll_env\Scripts\activate`

注：若果使用的PowerShell，需要将Activate的首字母大写。

若要停止使用虚拟环境，执行如下代码：

`deactivate`

**安装Django**

执行如下命令：

`pip install --upgrade pip`

注：若因为网速下载失败，切换`python.exe pip install --upgrade pip`。pip会频繁更新，因此每次搭建好新的虚拟环境都最好更新pip。

使用阿里云镜像网站安装django：

`pip install django -i http://mirrors.aliyun.com/pypi/simple/`

### 1.3  在Django中创建项目

执行如下命令新建一个项目：

`django-admin startproject ll_project .`

注：此命令末尾的（ .）让新项目使用合适的目录结构，在开发完成后可以将应用成功部署到服务器上，千万别忘记！！！若忘记了需要删除已创建的文件和文件夹（ll_env除外），重新运行此命令。

创建完成后可以运行`dir`查看目录文件。

ll_project包含4个文件，最重要的是settings.py、urls.py和wsgi.py。

-   settings.py：指定Django如何与系统交互以及如何管理项目
-   urls.py：创建那些文件来响应浏览器请求
-   wsgi.py：web gateway interface（Web服务器网关接口）的缩写，帮助Django提供它创建的文件

### 1.4  创建数据库

Django将大部分与项目相关的信息存储在数据库中，本项目中使用的数据库为SQLite，执行如下命令给Django提供一个数据库：

`python manage.py migrate`

此命令将修改数据库为**迁移（migrate）**数据库。首次执行**migrate**命令将让Django确保数据库与项目当前状态匹配，在这里，Django指出它将准备好数据库，用于存储执行管理和身份验证任务所需的信息。

注：在活动的虚拟环境中运行manage.py时，务必使用python命令。

### 1.5  查看项目

下面来核实Django正确的创建了项目，执行如下代码：

`python manage.py runserver`

![](assets/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202024-08-22%20223347.png)

复制此URL到Web浏览器，将看到如下页面，证明成功创建项目！若要关闭连接，可切换到终端窗口按`Ctrl+C`

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-22 223706.png)

## 2  创建应用程序

在上面的终端窗口中再打开一个标签页，并切换到manage.py所在的目录，激活虚拟环境，执行如下命令：

`python manage.py startapp learning_logs`

可以看到项目目录中新增了文件夹learning_logs，执行dir查看创建了哪些文件，其中最重要的是models.py，admin.py，views.py。我们将使用models.py来定义在应用程序中管理的数据。

### 2.1  定义模型

模型告诉Django如何处理应用程序中存储的数据，模型就是一个类，打开models.py，这是一个表示用户要存储的主题的模型，将其修改为如下代码块：

```
from django.db import models

# Create your models here.
class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text
```

**注意：本次编写的项目笔记中涉及到的所有代码基础均不予解释，如有代码看不懂请自行Chatgpt**

### 2.2  激活模型

打开settings.py，找到INSTALLED_APPS片段，此片段告诉Django哪些应用程序被安装到了项目中，将此代码片段修改成如下：

```
INSTALLED_APPS = [
	#	我的应用程序
	'learning_logs',
	
	#	Django默认添加的应用程序
	--snip--
]
--snip--
```

注：务必将你自己创建的应用程序放在默认应用前，这样能覆盖默认应用程序的行为

接着让Django修改数据库使其能够存储与模型Topic相关的信息，执行如下命令：

`python manage.py makemigrations learning_logs`

makemigrations让Django确定如何修改数据库，使其能够存储与前面定义的新模型相关联的数据，输出会让Django创建一个名为“0001_initial.py”的迁移文件，在数据中为Topic模型创建一个表。

下面应用迁移，让Django修改数据库：

`python manage.py migrate`

注：每当需要修改“学习笔记”管理的数据时，都采取如下三个步骤：修改models.py，对learning_logs调用makeigrations，让Django迁移项目

### 2.3  Django管理网站

Django提供的管理网站可以轻松的处理模型，它仅供网站管理员使用。本节将建立管理网站，并通过它使用模型Topic来添加主题。

**创建超级用户**

在终端中执行如下代码：

`python manage.py createsuperuser`

输入你的用户名、邮箱、密码。

注：Django并不存储密码，而是存储从密码中派生出来的一个字符串—**哈希值**。每当你输入密码时，Django都会计算其哈希值并与存储的哈希值进行比较，这两个值相同则通过身份验证。

**向管理网站注册模型**

打开learning_ogs下的admin.py文件，输入以下代码：

```
from .models import Topic
admin.site.register(Topic)
```

注：models前的句点（.）让Django在当前文件的目录中查找models.py；admin.site.register（）让Django通过管理网站管理模型。

现在，使用超级用户访问网站：http://127.0.0.1:8000/，将看到如下页面。

<img src="C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-23 160942.png" />

**添加主题**

单击Topics进入主题，单击Add Topic，在第一个方框中输入Chess并单击Save，同样的方式在创建一个Rock Climbing，这样就保存了两个主题（国际象棋和攀岩）。

### 2.4  定义模型Entry

要记录学到的国际象棋和攀岩知识，用户必须能在学习笔记中添加条目。所以需要定义相关联的模型。每个条目都有特定的主题相关联，这种关系称为多对一关系。

在models.py文件中添加如下代码：

```
class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """若有多条条目则用entries表示"""
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回一个表示条目的字符串"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        else:
            return self.text
```

注：属性**topic**是一个ForeignKey实例。**外键（ForeignKey）**是一个数据库术语，在这里是将每个条目都与特定的主题相关联。在创建每个主题时，都会为其分配一个键（ID），当需要在两项数据之间建立联系时，Django就会使用与每项信息相关联的键。实参**on_delete=models.CASCADE**让Django删除主题的同时删除所有与之相关联的条目，这就是**级联删除（cascading dalete）**

>   [!NOTE]
>
>   **这里的时区设置是UTC时区的时间，若要显示北京时间，要将全settings.py中的USE_TZ=True改为False。**

### 2.5  迁移模型

每次添加新模型都需要再次迁移数据库，这是个固定过程：

-   修改models.py
-   执行命令`python manage.py makemigrations learning_logs`
-   执行命令`python manage.py migrate`

### 2.6  向管理网站注册Entry

打开admin.py文件，添加如下代码：

```
from .models import Topic，Entry
admin.site.register(Entry)
```

返回网站，可以看到Learning_logs下列出了Entries，单击Entries的Add按钮，在下拉列表中选择Chess，并添加一个条目，单击Save保存，同样的方法在创建一个攀岩条目。

### 2.7  Django shell

输入一些数据后，就可以用交互式终端会话以编程的方式查看数据了。这种交互式终端称为**Django shell**，是测试项目和排除故障的理想之地。下面是一个示例命令：

```
python manage.py shell
>>> from learning)logs.models import Topic
>>> Topic.objects.all()
```

第一行命令启动Python编辑器；第二行命令导入模型；第三行命令使用Topic.objects.all()方法获取模型Topic的所有实例，这将返回一个**查询集**的列表。

可以向遍历列表一样遍历查询集，下面演示了如何查看分配给每个主题对象的ID：

``` = 
>>> topics = Topic.objects.all()
>>> for topic in topics:
>>>		print(topic.id,topic)
...
1 Chess
2 Rock Climbing
```

知道了主题对象的ID就可以使用Topic.objects.get()方法获取该对象并查看其属性了：

```
>>> t = Topic.objects.get(id=1)
>>> t.text
'Chess'
>>> t,date_added
datetime,datetime(2024,8,23,19,3,36,928759,tzinfo=datetime.timezone.utc)
```

还可以查看与主题相关联的条目：

```
>>> t.entry_set.all()
```

注：要通过外键关系获取数据，可使用相关模型的小写名称、下划线和单词set。

## 3  创建网页：学习笔记主页

使用Django创建网页可分为三个阶段：定义URL，编写视图，编写模板。顺序不分先后，在本项目中按照前述顺序。

-   **URL模式**描述了URL的构成，让Django知道如何将浏览器请求与网站URL匹配，以确定返回那个网页。每个URL都被映射到特定的视图
-   **视图**函数获取并处理网页所需的数据。视图使用模板来渲染网页
-   **模板**定义网页的总体结构

### 3.1  映射URL

主页的URL最重要，它是用户用来访问项目的基础URL，当前基础URL返回默认的Django网站，下面进行修改。

打开ll_project文件夹下的urls.py文件，将代码修改成如下形式：

```
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('learning_logs.urls'))
]
```

开头两行导入admin模块和一个函数path，以便创建URL路径；变量urlpatterns包含项目中应用程序的URL；admin.site.urls定义了可在管理网站中请求的所有URL。

默认的urls.py在ll_project文件夹中，需要在learning_logs文件夹中再创建一个urls.py文件，在这个文件中输入以下代码：

```
"""定义learning_logs的url模式"""

#	需要使用path将URL映射到视图
from django.urls import path
#	句点能让Python从当前模块所在的文件下中导入views
from . import views

#	变量app_name能让Django将这个文件与项目内其他重名文件区分开来
app_name = 'learning_logs'
#	urlpatterns包含在应用程序learnig_logs中请求的网页
urlpatterns = [
    #   主页
    path('',views.index,name='index')，
]
```

注：实际的URL是对path（）函数的调用，它接受三个实参。

1.  是一个字符串，帮助Django正确路由请求，收到请求后，将请求路由给一个视图，并搜索所有URL模式，以找到与当前请求相匹配的。Django忽略项目的基础URL，因此空字符串（‘ ’）与基础URL匹配。
2.  指定了要调用view.py中的哪个函数，当请求的URL匹配时，Django调用view.py中的index（）函数（此函数将在下一节编写）。
3.  将这个URL模式名称指定为index，以此可以在其它项目文件中引用它。每当需要提供项目主页的链接时，都使用这个名称。

### 3.2  编写视图

打开learning_logs文件夹下的views.py，添加如下代码：

```
def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')
```

注：render（）函数根据视图提供的数据渲染响应。

### 3.3  编写模板

在learning_logs文件夹下新建一个templates文件夹，在templates文件夹中在新建一个learning_logs文件夹，在其中新建一个index.html*（这并不多余，这建立了Django能够明确理解的结构）*，编写如下代码：

```
<p>Learning Logs</p>
<p>Learning Logs helps you keep track of your learning,for any topic you're inte
    rested in.</p>
```

网页如图所示：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-23 193201.png)

### 3.4  创建其他网页

我们将扩充两个显示数据的网页，一个列出所有主题，一个显示特定主题的所有条目。为此，要先创建一个模板，项目中的其他模板都将继承它。

**模板继承**

**1.父模板**

在learning_logs/templates/learning_logs/base.html路径下新建一个base.html模板，当前所有页面包含的元素只有顶端的标题。所以将这个标题设置为主页的链接：

```
<p>
  <a href="{% url 'learning_logs:index' %}">Learning_Log</a> -
</p>

{% block content %}{% endblock content %}
```

第二行代码生成一个url的模板标签，该url与learning_logs/urls.py中定义的名为index的URL模式匹配，Learning_Logs命名空间来自learning_logs/urls.py赋给app_name的值。

注：python中缩进四个空格，而在模板文件中层级间一般缩进两个空格

**2.子模板**

现在要重写模板index.html，使其继承base.html：

```
{% extends 'learning_logs/base.html' %}

{% block content %}
<p>Learning Logs helps you keep track of your learning,for any topic you're inte
    rested in.</p>
{% endblock content %}
```

**显示所有主题的页面**

**1.URL模式**

首先要定义此页面的URL，我们使用http://localhost:8000/topics/返回该页面，下面修改learning_logs/urls.py：

```
"""定义learning_logs的url模式"""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    #   主页
    path('',views.index,name='index'),
    #   显示所有页面的主题
    path('topics/',views.topics,name='topics'),
]
```

新URL模式为topics/，在匹配时即可包含斜杠也可省略，但topics后不能跟东西。URL与该模式匹配的请求都交给views.py中的topics（）函数处理。

**2.视图**

在views.py中添加如下代码：

```
from .models import Topic

def topics(request):
    """显示所有主题"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics':topics}
    return render(request,'learning_logs/topics.html',context)
```

**3.模板**

在learning_logs/templates/learning_logs下新建一个topics.html文件，添加如下代码：

```
{% extends 'learning_logs/base.html' %}

{% block content %}
  <p>Topics</p>
  <ul>
    {% for topic in topics %}
    <li>
      {{topic.text}}
    </li>
    {% empty %}
      <li>No topics have been added yet.</li>  
    {% endfor%}
  </ul>
{% endblock content %}
```

在标准HTML中

-   项目列表称为无序列表，用`<ul></ul>`表示；
-   `<li></li>`为项目列表项

现在修改父模板，使其包含显示该页面的链接：

```
<p>
  <a href="{% url 'learning_logs:index' %}">Learning_Log</a> -
  <a href="{% url 'learning_logs:topics' %}">Topics</a>
</p>

{% block content %}{% endblock content %}
```

现在刷新页面，将会看到如下页面

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-26 185252.png)

**显示特定主题的页面**

**1.URL模式**

该页面使用主题的id属性来确定请求的是哪个主题，若用户要查看chess（id=1）的详细页面，URL为http://localhost:8000/topics/1/，下面在learning_logs/urls.py下添加如下代码：

```
    #   特定主题的详细页面
    path('topics/<int:topic_id>/',views.topic,name='topic'),
```

/<int:topic_id>/与在两个斜杠之间的整数匹配，并将这个整数赋给实参topic_id，模式匹配时调用视图函数topic，并将topic_id的值作为实参传递给它。

**2.视图**

在views.py下添加如下代码：

```
def topic(request,topic_id):
    """显示单个主题的所有条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {
        'topic':topic,
        'entries':entries
    }
    return render(request,'learning_logs/topic.html',context)
```

**3.模板**

在learning_logs/templates/learning_logs下新建一个topic.html文件，添加如下代码：

```
{% extends 'learning_logs/base.html' %}

{% block content %}
  <p>Topic:{{topic.text}}</p>
  <p>Entries:</p>
  <ul>
    {% for entry in entries %}
      <li> 
        <p>{{entry.date_added|date:'M d,Y H:I'}}</p>
        <p>{{entry.text|linebreaks}}</p>
      </li>
    {% empty %}
      <li>There are No entries for this topic yet.</li>  
    {% endfor%}
  </ul>
{% endblock content %}
```

注：（|）竖线表示过滤器—在渲染过程中对模板变量的值进行修改的函数，过滤器date:'M d,Y H:I'以“Auguest 26,2024 19:02”的格式显示时间。

**将显示所有主题的页面中的每个主题都设置为链接**

修改topics.html:

```
{% extends 'learning_logs/base.html' %}

{% block content %}
  <p>Topics</p>
  <ul>
    {% for topic in topics %}
    <li>
      <a href="{% url 'learning_logs:topic' topic.id %}">
      {{topic.text}}
      </a>
    </li>
    {% empty %}
      <li>No topics have been added yet.</li>  
    {% endfor%}
  </ul>
{% endblock content %}
```

现在刷新页面，显示所有主题的链接，单击其中一个主题可以看到如下页面：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-26 190517.png)

注：topic.id检查主题并获取该主题的id值；topic_id是向该id的引用

## 4  用户账户

本章将创建一些表单，让用户能够添加主题和条目，除此之外本章还将实现用户身份验证系统，供用户创建自己的账户，并让一些页面仅供已登陆的用户访问。然后修改一些视图函数，使用户只能看到自己的数据。

### 4.1  让用户能够输入数据

#### 4.1.1  添加新主题

方法与创建网页几乎一样，唯一的差别是需要导入包含表单的模块forms.py

**1.用于添加主题的表单**

在learning_logs中创建一个forms.py文件，编写第一个表单：

```
from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):
    """使用户能够添加主题的表单"""
    class Meta:
        """
        最简单的ModelForm只包含一个Meta类,告诉DJango根据那个模型创建表单
        以及在表单中包含哪些字段
        """
        model = Topic
        fields = ['text']   #只包含字段text
        labels = {'text':''}    #字典labels中的空字符串告诉DJango不为text生成标签
```

**2.URL模式**

遵循URL应尽可能简短的原则，新网页的URL设置为http://localhost:8000/new_topic/，将其添加到learning_logs/urls.py中：

```
    #   用于添加新主题的网页
    path('new_topic/',views.new_topic,name='new_topic'),
```

**3.视图函数**

new_topic()函数需要处理两种情况：

1.  刚进入new_topic网页，这种情况显示空表单
2.  对提交的表单进行处理，并重定向到网页topics

在views.py中修改成如下代码：

```
from django.shortcuts import render,redirect
from .forms import TopicForm

def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        """未提交数据；创建一个新表单"""
        form = TopicForm()
    else:
        """提交数据；对数据进行处理"""
        form = TopicForm(data=request.POST)
        if form.is_valid(): #   is_valid()核实用户填写了所有必不可少的字段，且输入的
                            #   数据与要求的字段类型一致
            form.save()
            return redirect('learning_logs:topics') #   redirect()的作用是将一个
                            #   视图作为参数，并将用户重定向到与该视图相关联的页面
    #   显示空表单或指出表单数据无效
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)
```

GET请求和POST请求：

至从服务器读取数据的页面使用GET请求；在用户需要通过表单提交数据时使用POST请求。在本项目中我们在处理所有表单时都使用POST请求

**4.模板new_topic**

新建new_topic.html，编写如下代码：

```
{% extends 'learning_logs/base.html' %}

{% block content %}
  <p>Add a new topic:</p>
  
  <form action="{% url 'learning_logs:new_topic' %}" method='post' >
    {% csrf_token %}
    {{form.as_div}}
    <button name="submit">Add topic</button>
  </form>
  
{% endblock content %}
```

实参action告诉服务器数据要发送到那里；Django使用标签{% csrf_token %}来防止攻击者利用表单对服务器进行未经授权的访问—**跨站请求伪造**。模板变量{{form.as_div}}让Django自动创建表单所需的全部字段。

**5.链接到页面new_topic**

在页面topics中添加new_topic页面的链接：

```
<a href="{% url 'learning_logs:new_topic' %}">Add a new topic</a>
```

*这个链接放在既有主题列表的后面*

刷新页面，看到如下页面：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-26 212726.png)

#### 4.1.2  添加新条目

**1.用于添加新条目的表单**

在forms.py文件中添加如下代码：

```
from .models import Topic,Entry

class EntryForm(forms.ModelForm):
    """使用户能够添加新条目的表单"""
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        """
        小部件(widgets)是一种HTML表单元素,这里让Django使用宽度
        为80列的forms.Textarea元素
        """
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
```

**2.URL模式new_entry**

在这个URL模式中，需要包含实参topic_id，因为条目必须与特定的主题相关联，在learning_logs/urls.py中添加此URL：

```
    #   用于添加新条目的网页
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
```

**3.视图函数**

在views.py中修改成如下代码：

```
from .forms import TopicForm,EntryForm

def new_entry(request,topic_id):
    """添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        """未提交数据；创建一个空表单"""
        form = EntryForm()
    else:
        """提交数据；对数据进行处理"""
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic.id)
    #   显示空表单或指出表单数据无效
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)
```

**4.模板new_entry**

新建new_entry.html，编写如下代码：

```
{% extends 'learning_logs/base.html' %}

{% block content %}
  <p><a href="{% url 'learning_logs:topic' topic.id %}">{{topic}}</a></p>
  <p>Add a new entry:</p>

  <form action="{% url 'learning_logs:new_entry' topic.id %}" method='post' >
    {% csrf_token %}
    {{form.as_div}}
    <button name="submit">Add entry</button>
  </form>
  
{% endblock content %}
```

**5.链接到页面new_entry**

在topic.html中添加如下代码：

```
  <p>
    <a href="{% url 'learning_logs:new_entry' topic.id %}">Add a new entry</a>
  </p>
```

*此行代码添加在`<p>Entries:</p>`和`<ul></ul>>`之间。*

刷新页面，看到如下页面：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-26 213737.png)

#### 4.1.3  编辑既有条目

**1.URL模式edit_entry**

该页面的URL需要传递要编辑的条目的ID，在learning_logs/urls.py中添加此URL：

```
    #   用于编辑既有条目
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),
```

**2.视图函数**

在views.py中修改成如下代码：

```
from .models import Topic,Entry

def edit_entry(request,entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        """初次请求；使用当前的条目填充表单"""
        form = EntryForm(instance=entry)
    else:
        """提交数据；对数据进行处理"""
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)

    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)
```

**3.模板edit_entry**

新建edit_entry.html，编写如下代码：

```
{% extends 'learning_logs/base.html' %}

{% block content %}
  <p><a href="{% url 'learning_logs:topic' topic.id %}">{{topic}}</a></p>
  <p>Edit entry:</p>

  <form action="{% url 'learning_logs:edit_entry' entry.id %}" method='post' >
    {% csrf_token %}
    {{form.as_div}}
    <button name="submit">Save changes</button>
  </form>
  
{% endblock content %}
```

**4.链接到页面edit_entry**

在topic.html中添加如下代码：

```
        <p>
          <a href="{% url 'learning_logs:edit_entry' entry.id %}">Edit entry</a>
        </p>
```

*此行代码插入在for循环中的`<li></li>`中间*。

刷新页面，看到如下页面：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-26 214544.png)

>   [!IMPORTANT]
>
>   **至此，“学习笔记”项目的大部分功能已开发完毕！下一步我们将实现用户注册系统以及将该项目部署到云平台。**

### 4.2  创建用户账户

本节将建立用户注册和身份验证系统，让用户能够注册账户、登录和注销。我们将新建一个应用程序，其中包含于处理用户帐户相关的所有功能，该应用程序使用Django自带的身份验证系统来完成工作。

**应用程序accounts**

新建一个accounts的应用程序：

`python manage.py startapp accounts`

**将应用程序添加到settings.py中**

```
--snip--
‘accounts’,
--snip--
```

**修改根目录的urls.py，使其包含为accounts定义的URL**

`  path('accounts/',include('accounts.urls')),`

#### 4.2.1  登录页面

使用Django提供的默认视图login实现登录页面，在learning_logs/accounts中新建一个urls/py文件，添加如下代码：

```
"""为应用程序account定义URL模式"""
from django.urls import path,include
from .import views

app_name = 'accounts'
urlpatterns=[
    #   包含默认的身份验证URL模式
    path('',include('django.contrib.auth.urls')),
]
```

**1.模板login**

虽然使用默认视图，但模板还需要我们自己创建，默认的身份验证系统在registration中查找模板，在learning_logs/accounts中新建templates文件夹，在其中新建一个registration的文件夹，新建文件login.html，添加如下代码：

```
{% extends 'learning_logs/base.html' %}

{% block content %}

  {% if form.errors%}	
  #	若表单的error属性已设置，线是一条错误信息，指出输入的账户密码与数据库中存储的任何一对都不匹配
    <p>Your username and password didin't match.try again.</p>
  {% endif %}
  <form action="{% url 'accounts:login' %}" method='post'>
    {% csrf_token %}
    {{form.as_div}}
    <button name="submit">Log in</button>
  </form>
{% endblock content %}
```

注：一个应用程序中的模板可以继承另一个应用程序中的模板

**2.设置LOGIN_REDIRECT_URL**

用户成功登录后，重定向到主页，因此在ll_project中的settings.py的末尾添加如下代码：

```
#   我的设置
LOGIN_REDIRECT_URL = 'learning_logs:index'
```

**3.链接到登录页面**

将base.py文件修改成如下样式，让每个页面都包含它：

```
<p>
  <a href="{% url 'learning_logs:index' %}">Learning_Log</a> -
  <a href="{% url 'learning_logs:topics' %}">Topics</a> -
  {% if user.is_authenticated %}	
'''
在Django的身份验证系统中，每个对象都能使用user，该对象有一个is_authenticated属性：若用户已登录。该属性为True，否则为False
'''
    Hello,{{user.username}}
  {% else %}
    <a href="{% url 'accounts:login' %}">Log in</a>
  {% endif %}
</p>

{% block content %}{% endblock content %}
```

**4.使用用户页面**

若已使用管理员账户登录，访问http://localhost:8000/admin/退出登陆，接着访问http://localhost:8000/accounts/login/，可以看到如图所示页面：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-27 205245.png)

#### 4.2.1  注销

**1.在base.html中添加注销表单**

```
{% if user.is_authenticated %}
  <hr />
  <form action="{% url 'accounts:logout' %}" method='post'>
    {% csrf_token %}
    <button name="submit">Log out</button>
  </form>
{% endif %}
```

*此行代码插入到末尾*

**2.设置LOGOUT_REDIRECT_URL**

在ll_project中的settings.py的末尾添加如下代码：

```
LOGOUT_REDIRECT_URL = 'learning_logs:index'
```

#### 4.2.2  注册页面

我们使用Django提供的表单UserCreationForm,但是使用自己编写的视图和模板。

**1.URL模式**

在accounts/urls.py文件中添加如下代码

```
from .import views

    #   注册页面
    path('register/',views.register,name='register'),
```

**2.视图函数**

在accounts/views.py中添加如下代码：

```
from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    """注册新用户"""
    if request.method != 'POST':
        """显示空表单"""
        form = UserCreationForm()
    else:
        """处理填写好的表单"""
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            #   让用户自动登录，再重定向到主页
            login(request,new_user)
            return redirect('learning_logs:index')
    #   显示空表单或指出表单数据无效
    context = {'form':form}
    return render(request,'registration/register.html',context)
```

**3.注册模板**

新建register.html文件，添加如下代码：

```
{% extends 'learning_logs/base.html' %}

{% block content %}

  <form action="{% url 'accounts:register' %}" method='post' >
    {% csrf_token %}
    {{form.as_div}}
    <button name="submit">Register</button>
  </form>
  
{% endblock content %}
```

**4.链接到注册页面**

在base.html中添加如下代码：

```
    <a href="{% url 'accounts:register' %}">Register</a>
```

*注：此行代码添加在` {% else %}`后面*

### 4.3  让用户拥有自己的数据

我们将创建一个系统，使得用户的数据是受保护的，为此我们要确定各项数据所属的用户，再限制用户对页面的访问，让他们只能使用自己的数据。

#### 4.3.1  使用装饰器来限制访问

装饰器是放在函数定义前面的指令，用于改变函数的行为，若想了解更多请查阅另一篇笔记中的内容

>   **《Pyhton学习手册》，具体路径为python_note\test\test_class\test_survey.py**

**1。限制对页面topics的访问**

应该只允许已登录的用户请求页面topics，为此，在learning_logs/views.py中添加如下代码：

```
from django.contrib.auth.decorators import login_required

@login_required
def topics(request):
    """显示所有主题"""
    --snip--
```

仅当用户已登陆时，Django才运行topics()代码，若用户未登录，重定向到登录页面，为此，在ll_project/settings.py中实现这种重定向：

```
LOGIN_URL = 'accounts:login'
```

**2.全面限制对项目的访问**

在本项目中，除了对主业和注册页面不设限制外，其他页面都应该加以限制，为此需要在learning_logs/views.py中对除index()以外的视图都加以装饰器。

#### 4.3.2  将数据关联到用户

现在需要将数据关联到提交它们的用户，只要每个主题都归属于特定的用户，就能确定数据库中每个条目的所有者。现在来修改模型Topic，在其中添加一个关联到用户的外键，之后对数据库进行迁移。

**1.修改模型Topic**

对文件learning_logs/models.py的修改只涉及两行代码：

```
from django.contrib.auth.models import User

class Topic(models.Model):
	--snip--
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    --snip--
```

**2.确定当前有哪些用户**

在迁移数据库时，Django会对数据库进行修改，使其能够存储主题和用户之间的关联，为执行迁移，Django需要知道该将各个既有主题关联到哪个用户，对此最简单的做法是将所有主题关联到一个用户，如超级用户。为此，需要知道用户ID。

启动一个Django shell会话，执行如下命令：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-29 212152.png)

**3.迁移数据库**

知道用户ID后就可以迁移数据库了，在迁移是Python会询问是要暂时将模型Topic关联到特定的用户，还是在文件models.py中指定默认用户，选择第一个选项：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-29 212449.png)

*第一处选择第一个选项第二处意思是为了将所有既有主题关联到超级用户，输入用户的ID值1。*

现在可以进行迁移了：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-29 212812.png)

为了验证迁移符合预期，可以在shell中这样做：

![](C:\Users\22317\Pictures\Screenshots\屏幕截图 2024-08-29 212911.png)

结果一切如同预期。

#### 4.3.3  只允许用户访问自己的主题

当前，不管以哪个用户登录，都能够看到所有的主题，现在我们要改变这一点。

在vies.py中，对Topic()函数作如下修改：

```
def topics(request):
	"""显示所有主题"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	--snip--
```

request对象有一个request.user属性，其中包含有关该当前用户的信息，Topic.objects.filter(owner=request.user)让Django只从数据库中获取owner属性为当前用户的Topic对象。

#### 4.3.4  保护用户的主题

当前，任何已登录用户都可输入形如http://localhost:8000/topics/1/的URL来访问显示相应主题的页面，即使这个主题不属于他，为了修复这个问题，我们在views.py中对topic()获取请求的条目前进行检查：

```
from django.http import Http404

#   确认请求的主题属于当前用户
def check_topic_owner(owner,user):
    if owner != user:
        raise Http404
        
def topic(request,topic_id):
    """显示单个主题的所有条目"""
    topic = Topic.objects.get(id=topic_id)        
	check_topic_owner(topic.owner,request.user)
	--snip--
```

现在，如果试图访问其他用户的主题的条目，将看到404调试页面，在下一章我们将对这个页面进行配置，让用户看到更合适的错误页面而不是调试页面。

#### 4.3.5  保护页面

当前，任何已登录用户都可输入形如http://localhost:8000/edit_entry/entry_id/的URL来访问显示相应主题的编辑页面，现在我们修复这个问题，在views.py中对edit_entry()添加相同的代码：

```
def edit_entry(request,entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic.owner,request.user)
```

**相同的方法来修改new_entry页面。**

#### 4.3.6  将新主题关联到当前用户

当前，用于添加新主题的页面存在问题——没有将新主题关联到特定的用户，对此有一个简单的修复方案，在learning_logs/views.py中添加如下代码：

```
def new_topic(request):
    """添加新主题"""
    --snip--
        if form.is_valid(): #   is_valid()核实用户填写了所有必不可少的字段，且输入的
                            #   数据与要求的字段类型一致
            
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
			--snip--
```

注：第7行中传递实参commit=False，因为要先修改新主题，再将其保存到数据库中。

>   [!IMPORTANT]
>
>   至此，我们创建了一个功能齐全的项目，它运行在本地计算机上，在下一章我们将设置这个项目的样式，使它变得更漂亮，并将它部署在服务器上，供所有人都能通过互联网注册并创建账户。


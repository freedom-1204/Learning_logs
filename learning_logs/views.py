from django.shortcuts import render,redirect
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

#   确认请求的主题属于当前用户
def check_topic_owner(owner,user):
    if owner != user:
        raise Http404
# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')
@login_required
def topics(request):
    """显示所有主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'learning_logs/topics.html',context)
@login_required
def topic(request,topic_id):
    """显示单个主题的所有条目"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic.owner,request.user)
    entries = topic.entry_set.order_by('-date_added')
    context = {
        'topic':topic,
        'entries':entries
    }
    return render(request,'learning_logs/topic.html',context)
@login_required
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
            
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics') #   redirect()的作用是将一个
                            #   视图作为参数，并将用户重定向到与该视图相关联的页面
    
    #   显示空表单或指出表单数据无效
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)
@login_required
def new_entry(request,topic_id):
    """添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic.owner,request.user)
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
@login_required
def edit_entry(request,entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(topic.owner,request.user)
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
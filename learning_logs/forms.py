from django import forms
from .models import Topic,Entry

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
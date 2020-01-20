from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class User(models.Model):
    id = models.AutoField(verbose_name='用户序号',unique=True,primary_key=True)
    name = models.CharField(verbose_name='用户名',max_length=128)
    password = models.CharField(verbose_name='用户密码',max_length=256)
    start = models.IntegerField(verbose_name='开始投诉文本序号')
    end = models.IntegerField(verbose_name='结束投诉文本序号')

    def __str__(self):
        return self.name

class FraudText(models.Model):
    textid = models.IntegerField(verbose_name='投诉文本序号')
    text = models.TextField(verbose_name='投诉文本')
    #reviewer = models.IntegerField(verbose_name='标注人序号')

    def __str__(self):
        return self.text

class TagText(models.Model):
    id = models.AutoField(verbose_name='记录序号', unique=True, primary_key=True)
    textid = models.IntegerField(verbose_name='投诉文本序号')
    sentid = models.IntegerField(verbose_name='分句序号')
    text = models.TextField(verbose_name='分句内容')
    secid = models.IntegerField(verbose_name='动作序号')
    tagid = models.IntegerField(verbose_name='标签序号')
    reviewer = models.IntegerField(verbose_name='用户id')
    savedate = models.DateTimeField('保存日期', default=timezone.now)

    def __str__(self):
        return self.text

class FraudClass(models.Model): #下拉菜单的分类标签
    cid = models.IntegerField(verbose_name='动作序号')
    method = models.TextField(verbose_name='标签')
    pid = models.IntegerField(verbose_name='标签序号')

    def __str__(self):
        return self.method

class FinalTag(models.Model):
    id = models.AutoField(verbose_name='记录序号', unique=True, primary_key=True)
    textid = models.IntegerField(verbose_name='投诉文本序号')
    sentid = models.IntegerField(verbose_name='分句序号')
    text = models.TextField(verbose_name='分句内容')
    tagid = models.IntegerField(verbose_name='标签序号')

    def __str__(self):
        return self.text





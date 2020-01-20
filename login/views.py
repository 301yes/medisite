from django.shortcuts import render
from django.shortcuts import redirect
import json
import re
import os

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.http import FileResponse

from django.http import JsonResponse

from . import models
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

piter = 100 ##?
person = 2  ##?
#####

def taghome(request):
    return redirect('/login/')

def index(request):
    if request.session.get('is_login', None):
        reviewerid = request.session['userid']
        lasttext = models.TagText.objects.filter(reviewer=reviewerid).order_by('-textid')
        userstart = models.User.objects.get(id=reviewerid).start
        userend = models.User.objects.get(id=reviewerid).end
        text_exist = lasttext.exists()
        if text_exist:
            textlist = models.TagText.objects.filter(reviewer=reviewerid,sentid=0).order_by('textid').values('textid')
            complete_text = len(list(textlist))
            total_text = userend-userstart+1
            complete_percent = int((complete_text/total_text)*100)
            undo_text = userend-userstart-complete_text+1
            undo_percent = int((undo_text/total_text)*100)
            return render(request, 'index.html', {'complete': complete_text,'percent1':complete_percent,'undo':undo_text,'percent2':undo_percent})
        else:
            last_textid = 0
            undo_text = userend-userstart+1
            complete_percent = 0
            undo_percent = 100
            return render(request, 'index.html', {'complete': last_textid, 'percent1': complete_percent, 'undo': undo_text,'percent2': undo_percent})

    else:
        message = "您尚未登陆！"
        return render(request, 'page-login.html', {'message': message})

def example1(request):
    if request.session.get('is_login', None):
        return render(request, 'example1.html')
    else:
        message = "您尚未登录！"
        return render(request, 'page-login.html', {'message': message})

def example2(request):
    if request.session.get('is_login', None):
        return render(request, 'example2.html')
    else:
        message = "您尚未登录！"
        return render(request, 'page-login.html', {'message': message})

def example3(request):
    if request.session.get('is_login', None):
        return render(request, 'example3.html')
    else:
        message = "您尚未登录！"
        return render(request, 'page-login.html', {'message': message})


def taglogistic(request):
    if request.session.get('is_login', None):
        filepath = '/home/LT/fraudsite/login/templates/taglogistic.pdf'
        file = open(filepath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="taglogistic.pdf"'
        return response
    else:
        message = "您尚未登录！"
        return render(request, 'page-login.html', {'message': message})

@csrf_exempt
def login(request):
    if request.session.get('is_login', None): # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:#用户名和密码非空
            try:
                print('username:',username)
                user = models.User.objects.get(name=username)
            except :
                message = '用户不存在！'
                return render(request, 'page-login.html', {'message': message})

            if user.password == password:
                #print(username, password)
                request.session.set_expiry(0)
                request.session['is_login'] = True
                request.session['userid'] = user.id
                request.session['username'] = user.name
                request.session['userstart'] = user.start
                request.session['userend'] = user.end
                return redirect("/index/")

            else:
                message = '密码不正确！'
                return render(request, 'page-login.html', {'message': message})
        else:
            message = '用户名和密码不能为空'
            return render(request, 'page-login.html', {'message': message})
    return render(request, 'page-login.html')


def register(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username.strip() and password:
            same_name_user = models.User.objects.filter(name=username)
            if same_name_user:
                message = '用户名已经存在'
                return render(request, 'page-register.html', {'message': message})

            # 注册时即分配
            texts = models.FraudText.objects.all()
            text_len = texts.count()
            users = models.User.objects.all()
            user_len = users.count()

            zheng = user_len // person
            if text_len > (zheng * piter):
                start = zheng * piter + 1
                if text_len > (zheng + 1) * piter:
                    end = (zheng + 1) * piter
                else:
                    end = text_len
            else:
                message = '当前待标注样本已分配完毕，请联系管理员！'
                return render(request, 'page-register.html', {'message': message})

            new_user = models.User()
            new_user.name = username
            new_user.password = password
            new_user.start = start
            new_user.end = end

            new_user.save()
            return redirect("/login/")
        else:
            return render(request,'page-register.html')
    return render(request, 'page-register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")

def check(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    reviewerid = request.session['userid']
    lasttext = models.TagText.objects.filter(reviewer=reviewerid).order_by('-textid')
    text_exist = lasttext.exists()
    if not text_exist: #尚未开始标注
        message = "您尚未开始标注!"
        return render(request, 'check.html', {'message': message})
    else: #已有标注记录
        message = "您标注过以下文本："
        textlist = models.TagText.objects.filter(reviewer=reviewerid,sentid=0).order_by('textid').values('textid')        
        taggedlen = list(textlist)
        return render(request,'check.html', {'tagged':taggedlen,'message': message})

def check2(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    reviewerid = request.session['userid']
    lasttext = models.TagText.objects.filter(reviewer=reviewerid).order_by('-textid')
    text_exist = lasttext.exists()
    if not text_exist: #尚未开始标注
        message = "您尚未开始标注!请至标注主页面开始标注！"
        return render(request, 'check2.html', {'message': message})
    else: #已有标注记录
        message = "您遗漏了下述文本未标记："
        userstart = models.User.objects.get(id=reviewerid).start
        last_textid = int(lasttext.first().textid)+1
        comp = [i for i in range(userstart,last_textid)]
        textlist = models.TagText.objects.filter(reviewer=reviewerid,sentid=0).order_by('textid').values('textid')
        tagged = [x['textid'] for x in list(textlist)]
        taggedlen = list(set(comp).difference(set(tagged)))
        taggedlen.sort()
        return render(request,'check2.html', {'tagged':taggedlen,'message': message})

@csrf_exempt
def look(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")

    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)

    reviewerid = request.session['userid']
    nowtext = models.FraudText.objects.get(textid=nowtextid).text
    now_rows = list(models.TagText.objects.filter(textid=nowtextid,reviewer=reviewerid).values('sentid','text','secid','tagid'))
    for record in now_rows:
        secname = models.FraudClass.objects.get(cid=record['secid']).method
        tagname = models.FraudClass.objects.get(cid=record['tagid']).method
        record['secname'] = secname
        record['tagname'] = tagname
    return render(request,'look.html', context={'nowtext':nowtext,'nowtext_id':nowtextid,'nowrows': now_rows})

@csrf_exempt
def modify(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")

    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)

    sections = models.FraudClass.objects.filter(pid=0)
    res = []
    for i in sections:
        res.append([i.cid, i.method])

    nowtext = models.FraudText.objects.get(textid=nowtextid).text
    cutted_text = cutsent(nowtext)
    cutlen = [i for i in range(len(cutted_text))]
    cutted = dict(zip(cutlen, cutted_text))
    return render(request,'modify.html', context={'nowtext':nowtext,'nowtext_id':nowtextid,'cutted':cutted,'sections':res})

@csrf_exempt
def tagging(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")

    reviewerid = request.session['userid']
    lasttext = models.TagText.objects.filter(reviewer=reviewerid).order_by('-textid')
    text_exist = lasttext.exists()

    sections = models.FraudClass.objects.filter(pid=0)
    res = []
    for i in sections:
        res.append([i.cid, i.method])

    if not text_exist: #尚未开始标注
        userstart = models.User.objects.get(id=reviewerid).start
        now_id = userstart
        #now_textid = models.FraudText.objects.get(textid=now_id).textid
        nowtext = models.FraudText.objects.get(textid=now_id).text
        cutted_text = cutsent(nowtext)
        cutlen = [i for i in range(len(cutted_text))]
        cutted = dict(zip(cutlen, cutted_text))
        return render(request, 'tag.html', {'nowtext': nowtext, 'nowtext_id': now_id,'cutted':cutted,'sections':res})
    else: #已有标注记录
        #lasttext = list(models.TagText.objects.filter(reviewer=reviewerid,sentid=0).order_by('textid').values('textid'))
        #user_start = models.User.objects.get(id=reviewerid).start
        #user_end = models.User.objects.get(id=reviewerid).end+1
        #total = [i for i in range(user_start,user_end)]
        last_textid = int(lasttext.first().textid)
        #last_id = models.FraudText.objects.get(textid=last_textid).id
        topid = models.User.objects.get(id=reviewerid).end
        if last_textid < topid :
            now_id = last_textid+1
            #now_textid = models.FraudText.objects.get(id=now_id).textid
            nowtext = models.FraudText.objects.get(textid=now_id).text
            cutted_text = cutsent(nowtext)
            cutlen = [i for i in range(len(cutted_text))]
            cutted = dict(zip(cutlen,cutted_text))
            return render(request, 'tag.html', {'nowtext': nowtext, 'nowtext_id': now_id,'cutted':cutted,'sections':res})
        else:
            return render(request, 'tag.html', {'nowtext': '您已完成全部标注任务！', 'nowtext_id': topid+1})

@csrf_exempt
def tagnext(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)
        nowtextid = int(nowtextid)

    userid = request.session['userid']
    #lasttext_id = models.FraudText.objects.get(textid=nowtextid).id
    topid = models.User.objects.get(id=userid).end
    sections = models.FraudClass.objects.filter(pid=0)
    res = []
    for i in sections:
        res.append([i.cid, i.method])

    if nowtextid < topid:
        now_id = nowtextid + 1
        #now_textid = models.FraudText.objects.get(id=now_id).textid
        nowtext = models.FraudText.objects.get(textid=now_id).text
        cutted_text = cutsent(nowtext)
        cutlen = [i for i in range(len(cutted_text))]
        cutted = dict(zip(cutlen,cutted_text))

        return render(request, "test.html", context={"nowtext":nowtext,"nowtext_id": now_id,'cutted':cutted,'sections':res})
    else:
        return render(request, "test.html", context={"nowtext": '您已完成全部标注任务！', "nowtext_id": topid+1})

@csrf_exempt
def tagbefore(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)
        nowtextid = int(nowtextid)

    userid = request.session['userid']
    #lasttext_id = models.FraudText.objects.get(textid=nowtextid).id
    firstid = models.User.objects.get(id=userid).start
    sections = models.FraudClass.objects.filter(pid=0)
    res = []
    for i in sections:
        res.append([i.cid, i.method])

    if nowtextid > firstid:
        now_id = nowtextid - 1
        #now_textid = models.FraudText.objects.get(textid=now_id).textid
        print(now_id)
        nowtext = models.FraudText.objects.get(textid=now_id).text
        cutted_text = cutsent(nowtext)
        cutlen = [i for i in range(len(cutted_text))]
        cutted = dict(zip(cutlen,cutted_text))

        return render(request, "test.html", context={"nowtext":nowtext,"nowtext_id": now_id,'cutted':cutted,'sections':res})
    else:
        return render(request, "test.html", context={"nowtext": '已到达第一条您所负责的标注文本！', "nowtext_id": firstid-1})

def is_Chinese(word):
    for ch in word:
        if '\u4e00'<=ch<='\u9fff':
            return True
    return False

def cutsent(text):
    pattern = '，|,|。|？|！|!|；|、|\s|~|……|^|-|||,|:|：|_|\?'
    test_text = text.strip()
    re_text = re.split(pattern, test_text)
    result_text = [i for i in re_text if i != '' and is_Chinese(i)]
    return result_text

@csrf_exempt
def ajaxmethod(request):
    if request.is_ajax():
        pid = request.POST.get('pid',None)
    methods = models.FraudClass.objects.filter(pid=pid)
    cid_list = []
    method_list = []
    for i in methods:
        cid_list.append(i.cid)
        method_list.append(i.method)

    leng = len(method_list)
    return HttpResponse(json.dumps({"cid":cid_list,"methods":method_list,"leng":leng}, ensure_ascii=False))

@csrf_exempt
def savetag(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    userid = request.session['userid']

    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)
        sentid = request.POST.get('sentid', None)
        senttext = request.POST.get('senttext', None)
        secid = request.POST.get('secid', None)
        methodid = request.POST.get('methodid', None)

    search_dict = dict()

    if nowtextid:
        search_dict['textid'] = nowtextid
    if sentid:
        search_dict['sentid'] = sentid
    if userid:
        search_dict['reviewer'] = userid

    user_tag_info = models.TagText.objects.filter(**search_dict)
    text_exist = user_tag_info.exists()

    if text_exist:
        data = {'secid':secid, 'tagid':methodid,'reviewer':userid}
        user_tag_info.update(**data)
    else:
        new_tag = models.TagText()
        new_tag.textid = nowtextid
        new_tag.sentid = sentid
        new_tag.text = senttext
        new_tag.secid = secid
        new_tag.tagid = methodid
        new_tag.reviewer = userid

        new_tag.save()
    return HttpResponse(json.dumps({"msg": 'success'}))

@csrf_exempt
def modifytag(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    userid = request.session['userid']

    if request.is_ajax():
        nowtextid = request.POST.get('nowtextid', None)
        sentid = request.POST.get('sentid', None)
        senttext = request.POST.get('senttext', None)
        secid = request.POST.get('secid', None)
        methodid = request.POST.get('methodid', None)

    search_dict = dict()

    if nowtextid:
        search_dict['textid'] = nowtextid
    if sentid:
        search_dict['sentid'] = sentid
    if userid:
        search_dict['reviewer'] = userid

    user_tag_info = models.TagText.objects.filter(**search_dict)
    text_exist = user_tag_info.exists()

    if text_exist:
        data = {'secid':secid, 'tagid':methodid,'reviewer':userid}
        user_tag_info.update(**data)
    else:
        new_tag = models.TagText()
        new_tag.textid = nowtextid
        new_tag.sentid = sentid
        new_tag.text = senttext
        new_tag.secid = secid
        new_tag.tagid = methodid
        new_tag.reviewer = userid

        new_tag.save()
    return HttpResponse(json.dumps({"msg": 'success'}))



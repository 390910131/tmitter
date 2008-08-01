# -*- coding: utf-8 -*-
from django.http import HttpResponse,Http404, HttpResponseRedirect, HttpResponseServerError
from django.template import Context, loader
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from tmitter.settings import *
from tmitter.mvc.models import Note,User,Category
from tmitter.mvc.feed import RSSRecentNotes,RSSUserRecentNotes
from tmitter.utils import mailer,formatter

# #################
# common functions
# #################

# do login
def __do_login(request,_username,_password):
    _state = __check_login(_username,_password)
    if _state['success']:
         # save login info to session
        request.session['islogin'] = True
        request.session['userid'] = _state['userid']
        request.session['username'] = _username
        request.session['realname'] = _state['realname']
    
    return _state

# get session user id
def __user_id(request):
    return request.session.get('userid',-1)

# get sessio realname
def __user_name(request):
    return request.session.get('username','')

# return user login status
def __is_login(request):
     return request.session.get('islogin', False)

# check username and password
def __check_login(_username,_password):
    _state = {
        'success' : True,
        'message' : 'none',
        'userid' : -1,
        'realname' : '',
    }

    try:
        _user = User.objects.get(username = _username)
        
        # to decide password 
        if(_user.password == _password):
            _state['success']  = True
            _state['userid'] = _user.id
            _state['realname'] = _user.realname
        else:
            # password incorrect
            _state['success']  = False
            _state['message'] = u"密码不正确."
    except (User.DoesNotExist):
        # user not exist
        _state['success'] = False
        _state['message'] = '用户不存在.'

    
    return _state

# check user was existed
def __check_username_exist(_username):
    _exist = True
    
    try:
        _user = User.objects.get(username = _username)
        _exist = True
    except (User.DoesNotExist):
        _exist = False

    return _exist

# post signup data
def __do_signup(request,_userinfo):

    _state = {
            'success' : False,
            'message' : '',
        }

    # check username exist
    if(_userinfo['username'] == ''):
        _state['success'] = False
        _state['message'] = '用户名未输入.'
        return _state

    if(_userinfo['password'] == ''):
        _state['success'] = False
        _state['message'] = '密码未输入.'
        return _state

    if(_userinfo['realname'] == ''):
        _state['success'] = False
        _state['message'] = '姓名未输入.'
        return _state

    if(_userinfo['email'] == ''):
        _state['success'] = False
        _state['message'] = 'email未输入.'
        return _state
    
    # check username exist
    if(__check_username_exist(_userinfo['username'])):
        _state['success'] = False
        _state['message'] = '用户名已存在.'
        return _state

    

    # check password & confirm password
    if(_userinfo['password'] != _userinfo['confirm']):
        _state['success'] = False
        _state['message'] = '确认密码不正确.'
        return _state

    _user = User(username = _userinfo['username'],realname = _userinfo['realname'] , password = _userinfo['password'],email = _userinfo['email'])
    try:
        _user.save()
        _state['success'] = True
        _state['message'] = '注册成功.'
    except:
        _state['success'] = False
        _state['message'] = '程序异常,注册失败.'
    
    # send regist success mail
    mailer.send_regist_success_mail(_userinfo)

    return _state


# response result message page
def __result_message(request,_title=u'消息',_message='',_go_back_url=''):
    # body content
    _template = loader.get_template('result_message.html')
    
    _context = Context({
        'page_title' : _title,
        'message' : _message,
        'go_back_url' : _go_back_url,
    })
    
    _output = _template.render(_context)
    
    return HttpResponse(_output)
    
    

# #################
# view method
# #################

# home view
def index(request):
    return index_user(request,'')

# user messages view by self
def index_user_self(request):
    _user_name = __user_name(request)
    return index_user(request,_user_name)

# user messages view
def index_user(request,_username):
    return index_user_page(request,_username,1)

# index page
def index_page(request,_page_index):
    return index_user_page(request,'',_page_index)

# user messages view and page
def index_user_page(request,_username,_page_index):
    
    # get user login status
    _islogin = __is_login(request)
    _page_title = u'首页'
    
    try:
        # get post params
        _message = request.POST['message']        
        _is_post = True
    except (KeyError):
        _is_post = False
    
    # save message
    if _is_post:
        # check login
        if not _islogin:
            return HttpResponseRedirect('/signin/')
        
        # save messages
        _category = Category.objects.get(id = 1)
        try:
            _user = User.objects.get(id = __user_id(request))
        except:
            return HttpResponseRedirect('/signin/')        
        _note = Note(message = _message,category = _category , user = _user)
        _note.save()
        return HttpResponseRedirect('/user/' + _user.username)
          
    _userid = -1
    # get message list
    _offset_index = (int(_page_index) - 1) * PAGE_SIZE
    _last_item_index = PAGE_SIZE * int(_page_index)

    if _username != '':
        # there is get user's messages
        _user = get_object_or_404(User,username=_username)
        _userid = _user.id
        _notes = Note.objects.filter(user = _user).order_by('-addtime')
        _page_title = u'%s' % _user.realname
    else:
        # get all messages
        _user = None
        _notes = Note.objects.order_by('-addtime')

    # page bar
    _page_bar = formatter.pagebar(_notes,_page_index,_username)
    
    # get current page
    _notes = _notes[_offset_index:_last_item_index]
    
    # body content
    _template = loader.get_template('index.html')

    _context = Context({
        'page_title' : _page_title,
        'notes' : _notes,
        'islogin' : _islogin,
        'userid' : __user_id(request),
        'user' : _user,
        'page_bar' : _page_bar,
        })
    
    _output = _template.render(_context)    
    
    return HttpResponse(_output)



# detail view
def detail(request,_id):
    # get user login status
    _islogin = __is_login(request)
    
    _note = get_object_or_404(Note,id=_id)
    
    # body content
    _template = loader.get_template('detail.html')
    
    _context = Context({
        'page_title' : u'%s的消息 %s' % (_note.user.realname,_id),
        'item' :_note,
        'islogin' : _islogin,
        'userid' : __user_id(request),
    })
    
    _output = _template.render(_context)
    
    return HttpResponse(_output)

def detail_delete(request,_id):
    # get user login status
    _islogin = __is_login(request)    

    _note = get_object_or_404(Note,id=_id)
   
    _message = ""
    
    try:
        _note.delete()
        _message = u"消息已删除."
    except:
        _message = u"删除出错."
    
    return __result_message(request,u'消息 %s' % _id,_message) 
    

# signin view
def signin(request):
    
    # get user login status
    _islogin = __is_login(request)
   
    try:
        # get post params
        _username = request.POST['username']
        _password = request.POST['password']
        _is_post = True
    except (KeyError):
        _is_post = False
    
    # check username and password
    if _is_post:
        _state = __do_login(request,_username,_password)

        if _state['success']:
            return __result_message(request,u'登录成功',u'恭喜，您已经登录成功。') 
    else:
        _state = {
            'success' : False,
            'message' : '请登录'
        }

    # body content
    _template = loader.get_template('signin.html')
    _context = Context({
        'page_title' : u'登录',
        'state' : _state,
        })
    _output = _template.render(_context)
    return HttpResponse(_output)

def signup(request):
    # check is login
    _islogin = __is_login(request)

    if(_islogin):
        return HttpResponseRedirect('/')

    _userinfo = {
            'username' : '',
            'password' : '',
            'confirm' : '',
            'realname' : '',
            'email' : '',
        }
    
    try:
        # get post params
        _userinfo = {
            'username' : request.POST['username'],
            'password' : request.POST['password'],
            'confirm' : request.POST['confirm'],
            'realname' : request.POST['realname'],
            'email' : request.POST['email'],
        }
        _is_post = True
    except (KeyError):        
        _is_post = False

    if(_is_post):
        _state = __do_signup(request,_userinfo)
    else:
        _state = {
            'success' : False,
            'message' : '注册新用户'
        }
    
    if(_state['success']):
        return __result_message(request,u'注册成功',u'恭喜，您已经注册成功。') 

    _result = {
            'success' : _state['success'],
            'message' : _state['message'],
            'form' : {
                    'username' : _userinfo['username'],
                    'realname' : _userinfo['realname'],
                    'email' : _userinfo['email'],
                }
        }

    # body content
    _template = loader.get_template('signup.html')
    _context = Context({
        'page_title' : u'注册',
        'state' : _result,
        })
    _output = _template.render(_context)  
    return HttpResponse(_output)
    

# signout view
def signout(request):
    request.session['islogin'] = False
    request.session['userid'] = -1
    request.session['username'] = ''
    
    return HttpResponseRedirect('/')

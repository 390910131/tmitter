from django.http import HttpResponse,Http404, HttpResponseRedirect, HttpResponseServerError
from django.template import Context, loader
from django.shortcuts import get_object_or_404
from tmitter.settings import *
from tmitter.mvc.models import Note,User,Category
# Create your views here.



# #################
# common functions
# #################

# header template
def __get_header(_title,request):
    
    _template = loader.get_template('header.html')
    _context = Context({
        'title' : _title,
        'app_name' : APP_NAME,
        'beta' : True,
        'islogin' : __is_login(request),
        'username' : __user_name(request),
        })
    return _template.render(_context)

# footer template
def __get_footer():
    _template = loader.get_template('footer.html')
    _context = Context({
        'version' : '0.1'
        })
    return _template.render(_context)



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
            _state['message'] = 'password incorrect.'
    except (User.DoesNotExist):
        # user not exist
        _state['success'] = False
        _state['message'] = 'user does not exist.'

    
    return _state
    



# #################
# view method
# #################

# define header html from __get_header
header = ''
# define footer html from __get_header
footer = __get_footer()

# home view
def index(request):
    return index_param(request,'')

# user messages view
def index_param(request,_username):
    
    # get user login status
    _islogin = __is_login(request)
    
    # header
    _header = __get_header('Home',request)
    
    try:
        # get post params
        _message = request.POST['message']        
        _is_post = True
    except (KeyError):
        _is_post = False
    
    # save messag
    if _is_post:
        # check login
        if not _islogin:
            return HttpResponseRedirect('/signin/')
        
        # save message
        _category = Category.objects.get(id = 1)
        try:
            _user = User.objects.get(id = __user_id(request))
        except:
            return HttpResponseRedirect('/signin/')        
        _note = Note(message = _message,category = _category , user = _user)
        _note.save()
  
    # get message list
    if _username != '':
        # there is get user's messages
        _user = get_object_or_404(User,username=_username)
        _notes = Note.objects.filter(user = _user).order_by('-addtime')[0:PAGE_SIZE]
    else:
        # get all messages
        _notes = Note.objects.order_by('-addtime')[0:PAGE_SIZE]
        
    # body content
    _template = loader.get_template('index.html')
    _context = Context({
        'notes' : _notes,
        'islogin' : _islogin
        })
    
    _output = _header + _template.render(_context) + footer    
    
    return HttpResponse(_output)



# detail view
def detail(request,_id):
    # get user login status
    _islogin = __is_login(request)
    
    # header
    _header = __get_header('message %s' % _id,request)
    
    _note = get_object_or_404(Note,id=_id)
    # body content
    _template = loader.get_template('detail.html')
    _context = Context({
        'item' :_note 
        })
    
    _output = _header + _template.render(_context) + footer
    
    return HttpResponse(_output)



# signin view
def signin(request):
    
    # get user login status
    _islogin = __is_login(request)
    
    # header
    _header = __get_header('signin',request)
   
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
            return HttpResponseRedirect('/')
    else:
        _state = {
            'success' : False,
            'message' : 'please login'
        }

    # body content
    _template = loader.get_template('signin.html')
    _context = Context({
        'state' : _state,
        })
    _output = _header + _template.render(_context) + footer    
    return HttpResponse(_output)

# signout view
def signout(request):
    request.session['islogin'] = False
    request.session['userid'] = -1
    request.session['username'] = ''
    
    return HttpResponseRedirect('/')

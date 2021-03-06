from django import dispatch
from django.core.signals import request_started
from django.contrib.auth import login, logout, user_logged_in
from django.dispatch import receiver,Signal
from django.db.models.signals import pre_save


from .models import Profile

ten_req_done = Signal()

hello_signal = Signal()


def show_hello(*args,**kwargs):
    print("hello to you")

hello_signal.connect(show_hello)

@receiver(hello_signal,weak=False,dispatch_uid="show_helo")
def show_bye(*args, **kwargs):
    print("bye")
    print(hello_signal.receivers)



global count
count = 0

def check_request_integrity(sender,environ,*args, **kwargs):
    global count
    count = count + 1
    print(f'so far you have done {count} requests!')

    if count > 5 :
        hello_signal.send(sender=Profile)

request_started.connect(check_request_integrity)


from django.contrib.auth import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def be_ass_to_user(sender,request,user, *args, **kwargs):

    print(args)
    for kw in kwargs:
        print(type(kw))
    # print(user)
    # print(sender)
    # print(request)
    # login(request,user)
    print(f'Welcome to {user} from {__name__}')
    logout(request)
    
    



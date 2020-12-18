# Django Signals Training

## NEED (نیاز)
- To do some action based on an event
- SQL solution is triggers. which is not flexible and also handled via RDBMS (old syntax , ....)
- *Example*
  - if you want to save uesr last login date : user_logged_in
  - if you want to send a code vis SMS : pre_save
  - if you want to ..... ?!

## SETUP (راه اندازی)
- I.   **Define a reciver method**
```python
global count
count = 0
...
def check_request_integrity(sender,environ,*args, **kwargs):
  global count
  count = count + 1
  print(f'so far you have done {count} requests!')
```
- II. **Conneting reciver to sender**
  - ##### Annotate
      ```python
      from django.dispatch import receiver
      @reciver(Signal_name)
      def function_name(**kwargs):
        pass
      ```
  - ##### Connect attribute

      ```python
      Signal_name.connect(function_name)  
      ```
- III. **Connection Parameters**  _extras_
    - **receiver** <_function_> : function to be called when event happens
    - **sender** <_model/obj_> : who sent this -e.g. model-instance , can be a string 'Me' 
    - **weak** <_bool_> : prevent from beeing collected by garbage collector
    - **dispatch_uid** <_str_> : preventing duplication (جلوگیری از چند بار وصل شدن یک تابع به یک سیگنال)
      - _if None -> Dynamicly generates ... id(target.__self__), id(target.__func__)_
  
    

## PLACING (محل قرارگیری سیگنال)
-  In model.py or near view.py functionalities

```python
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

@receiver(pre_save,sender= Profile)
def create_user_before_profile_saves(instance,*args, **kwargs):
    try:
        user = User.objects.create(username = f'{instance.ful_name} - {instance.phonenumber}',password=instance.password) 
        instance.id = user
    except Exception:
        raise Exception
        
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.RESTRICT,primary_key=True,blank=True)
    password = models.CharField(max_length=128,blank=True, null=True)
    ful_name = models.CharField(max_length=40, null=False)

```
-  In a signal.py
    - Steps
      - I. change app config
      - II. import signal module in ready() function
      - III. you need to show django the new configs
        - in installed apps :  apps._foo_Config
        - in init file of each app :    'foo_name_ . apps . foo_Config_class_name'


## Custom Signals 
**(! signal is implicit -> trouble in debugging -> it's better to use explicit funtion call instead of signal)**
#### Steps
- I.    from django.dispatch import Signal
- II.   create instance
- III.  signal send() from the place you want to trigger 
- IV.   define reciver function
- V.    connect to signal instance
**PARAMETERS**
- use cahcing   _The cache is cleaned when .connect() or .disconnect() is called and populated on send()_


! each time server re runs all the attributes resets
<br>
! Your ready() method will run during startup of every management command. 
<br>
! weakref : if the connetion is weak garbage collector can delete connection 


- List of Built-in Signals
- https://docs.djangoproject.com/en/3.1/ref/signals/


- Extra : https://django-pynotify.readthedocs.io/

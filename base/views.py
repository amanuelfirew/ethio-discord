from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from . models import Room, Topic , Message ,User
from . forms import RoomForm,ProfileForm,MyUserCreationForm,MessageForm



"""two views are hidden here by the "django.contrib.auth.urls" method.
which render a page on login.html and logged_out.html"""

def home(request):
    query_room = request.GET.get('search') if request.GET.get('search') != None else ''
    """filtering data with queryset lookup(Q) its a way to add more search sets to find data from."""
    rooms = Room.objects.filter(
        # (|) means 'or' (&) means 'and'
        Q(topic__name__icontains=query_room) |
        Q(name__icontains=query_room) |
        Q(host__username__icontains=query_room) |
        Q(description__icontains=query_room))
    # make a count of all the rooms.
    count_rooms = rooms.count()
    topics = Topic.objects.all()[0:5]
    # filtering the messages.
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=query_room) |
        Q(user__username__icontains= query_room))
    context = {'rooms': rooms, 'topics': topics,'count':count_rooms,
    'messages':room_messages}
    return render(request, 'base/home.html', context)


def room(request, room_id):
    room = Room.objects.get(id=room_id)
    room_messages = room.message_set.all().order_by('-updated')
    participants= room.participants.all()
    if request.method == 'POST':
        # this creates a comments section with the specified user,room and body
        # of message(remember,request.POST.get('body') picks any thing we inserted
        # on the body section of our room.html file.)
        messages = Message.objects.create(
            user= request.user,
            room= room,
            body= request.POST.get('body'))
        room.participants.add(request.user)
        return redirect('base:room',room_id = room.id)
    context = {'room': room,'messages':room_messages,'participants':participants}
    return render(request, 'base/room.html', context)

@ login_required
def create_room(request):
    topics = Topic.objects.all()
    if request.method != 'POST':
        # if form is empty create one.
        form = RoomForm()
    else:
        # if form is filled then save and submit that form.
        topic_name = request.POST.get('topic')
        """the get_or_create method tries to get the value in the argument 'name'
        if it exists it assigns the value to topic and doesn't create a new topic
        ,if the value doesn't exist it will create a new topic by it self and 
        pass it to topic.""" 
        topic,created = Topic.objects.get_or_create(name=topic_name.lower())
        Room.objects.create(
            host=request.user,
            topic = topic,
            name=  request.POST.get('name'),
            description = request.POST.get('description')
            )
        #if form.is_valid:
         #   room =form.save(commit=False)
          #  room.host = request.user
           # room.save()
        return redirect('base:home')
    context = {'form': form,'topics':topics}
    return render(request, 'base/room_form.html', context)


@ login_required
def update_room(request, room_id):
    room = Room.objects.get(id=room_id)
    topics = Topic.objects.all()
    if request.user != room.host:
        raise Http404
    if request.method != 'POST':
        # create a prefilled form
        form = RoomForm(instance=room)
    else:
        # create a prefilled form, add any modifications made and submit the form.
        topic_name = request.POST.get('topic')
        topic,create = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        #form = RoomForm(request.POST, instance=room)
        #if form.is_valid():
        #   form.save()
        return redirect('base:room',room_id=room.id)
    context = {'form': form,'topics':topics,'room':room}
    return render(request, 'base/room_form.html', context)

@ login_required
def update_message(request,message_id):
    message = Message.objects.get(id=message_id)
    if request.user != message.user:
        raise Http404
    if request.method != 'POST':
        form = MessageForm(instance = message)
    else:
        form = MessageForm(request.POST,instance=message)
        if form.is_valid():
            form.save()
            return redirect('base:room',room_id=message.room.id)
    context= {'form':form}
    return render(request,'base/update_message.html',context)

@ login_required
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.user != room.host:
        raise Http404
    # delete a room from the database.
    if request.method == 'POST':
        room.delete()
        return redirect('base:home')
    context = {'object': room, 'room': room}
    return render(request, 'base/delete.html', context)


@ login_required
def delete_message(request, room_id):
    messages = Message.objects.get(id=room_id)
    room = messages.room
    if request.user != messages.user:
        raise Http404
    # delete a room from the database.
    if request.method == 'POST':
        messages.delete()
        return redirect('base:room',room_id=room.id)
    context = {'object': messages}
    return render(request, 'base/delete.html', context)


def user_profile(request,user_id):
    user= User.objects.get(id=user_id)
    rooms= user.room_set.all()
    user_message= user.message_set.all()
    topics = Topic.objects.all()[0:5]
    count_rooms = rooms.count()
    context = {'user':user,'rooms': rooms, 'topics': topics,'count':count_rooms,
    'messages':user_message}
    return render(request,'base/profile.html',context)

@ login_required
def logout_user(request):
    logout(request)
    return redirect('base:home')

def register(request):

    if request.method != 'POST':
        form = MyUserCreationForm()
    else:
        form = MyUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            new_user= form.save()
            login(request,new_user)
            return redirect('base:home')
    context = {'form':form}
    return render(request,'registration/register.html',context)


@ login_required
def update_user(request):
    form = ProfileForm(instance = request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('base:user_profile',user_id=request.user.id)
    context = {'forms':form}
    return render(request,'base/update-user.html',context)

def topics_page(request):
    topic_query = request.GET.get('search') if request.GET.get('search') != None else ''
    topics = Topic.objects.filter(
        Q(name__icontains= topic_query))
    room = Room.objects.all()
    count_topics = room.count()
    context = {'topics':topics,'count':count_topics}
    return render(request,'base/all_topics.html',context)

def activity_page(request):
    message= Message.objects.all()
    context = {'messages':message}
    return render(request,'base/activity.html',context)


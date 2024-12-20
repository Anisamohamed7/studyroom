from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm, MyUserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import MessageForm

User = get_user_model()

# def loginPage(request):

#     page = 'login'
#     if request.user.is_authenticated:
#         return redirect('home')

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         try:
#             user = User.objects.get(username = username)
#             print(user)
#         except:
#             messages.error(request, 'User does not exist')  
#         user = authenticate(request, username=username, password=password)
#         print(user)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username or Password does not exist')
#     context={'page': page}
#     return render(request, 'studyroom/login_register.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user directly
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Show an error if authentication fails (user doesn’t exist or password is wrong)
            messages.error(request, 'Username or Password is incorrect')
    
    context = {'page': page}
    return render(request, 'studyroom/login_register.html', context)
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "An error occurred during registration")
    return render(request, 'studyroom/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get("q")!=  None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'studyroom/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk) #returns one single object
    room_messages = room.message_set.all()
    participants = room.participants.all()
    

    if request.method =="POST":
        file = request.FILES.get('file')
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
            file = file if file else None
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages': room_messages, 
               'participants': participants}
    return render(request, 'studyroom/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 
               'room_messages':room_messages, 'topics':topics}
    return render(request, 'studyroom/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        user = request.user
        print(user.username)
        print(user.email)
        newUser = User.objects.get(username =user.username)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')


    context={'form': form, 'topics': topics}
    return render(request, 'studyroom/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host :
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance = room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'studyroom/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host :
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'studyroom/delete.html',{'obj':room} )

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user :
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'studyroom/delete.html',{'obj':message} )

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'studyroom/update-user.html', {'form':form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get("q")!=  None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'studyroom/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all
    return render(request, 'studyroom/activity.html', {'room_messages':room_messages})

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            form.save()
            return redirect('some_view')  # Redirect after successful submission
    else:
        form = MessageForm()

    return render(request, 'studyroom/room.html', {'form': form})
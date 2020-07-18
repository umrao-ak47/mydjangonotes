from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Note
from .forms import NewNote, UserRegistrationForm

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'notes/index.html')

@login_required(login_url='notes:login')
def note_detail(
    request: HttpRequest, year: int, month: int, 
    day: int, slug: str
    ) -> HttpResponse:
    user = request.user
    note = get_object_or_404(
        user.notes, slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(request, 'notes/detail.html', {'note': note})

@login_required(login_url='notes:login')
def user_home(request: HttpRequest) -> HttpResponse:
    note_list = request.user.notes.all()
    paginator = Paginator(note_list, 5)
    page = request.GET.get('page')
    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)
    return render(request, 'notes/user.html', {'notes': notes})

@login_required
def note_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = NewNote(request.POST)
        if form.is_valid():
            note: Note = form.save(commit=False)
            title: str = request.POST['title']
            slug = title.replace(' ', '-')
            note.slug = slug
            note.author = request.user
            note.save()
            return HttpResponseRedirect(redirect_to=reverse('notes:user_home'))
    else:
        form = NewNote()
    return render(request, 'notes/new.html', {'form': form})

@login_required
def note_delete(
    request: HttpRequest, year: int, month: int, 
    day: int, slug: str) -> HttpResponse:
    note: Note = get_object_or_404(
        request.user.notes, slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    note.delete()
    return HttpResponseRedirect(redirect_to=reverse('notes:user_home'))

@login_required
def note_update(
    request: HttpRequest, year: int, month: int, 
    day: int, slug: str) -> HttpResponse:
    note = get_object_or_404(
        request.user.notes, slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    form = NewNote(request.POST or None, instance=note)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse('notes:user_home'))
    return render(request, 'notes/new.html', {'form': form})

def register(request: HttpRequest) -> HttpResponse:
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            new_user: User = form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.save()
            return HttpResponseRedirect(redirect_to=reverse('notes:login'))
    return render(request, 'notes/register.html', {'form': form})
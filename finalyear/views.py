
# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.views import generic
from finalyear.models import Book, Author, Genre ,Language
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

def index(request):
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify
    paginate_by = 10

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'authors/my_arbitrary_template_name_list.html'  # Specify
    paginate_by = 10
    
class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        
        return render(request, 'finalyear/book_detail.html', context={'book': book})

class AuthorDetailView(generic.DetailView):
    model = Author
    def author_detail_view(request, primary_key):
        try:
            book = Author.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Author does not exist')
        
        return render(request, 'finalyear/author_detail.html', context={'author': author})

class AuthorCreate(PermissionRequiredMixin ,CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_birth': '05/01/2018'}
    permission_required='can add author'

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required='can change author'

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required='can delete author'

class BookCreate(PermissionRequiredMixin,CreateView):
    model = Book
    fields = '__all__'
    permission_required='can add book'

class BookUpdate(PermissionRequiredMixin,UpdateView):
    model = Book
    fields = ['title', 'author', 'langs', 'summary','isbn','genre','file_url','download_url']
    permission_required='can change book'


class BookDelete(PermissionRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required='can delete book'




def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = CustomUserCreationForm()

    return render(request, 'finalyear/register.html', {'form': f})

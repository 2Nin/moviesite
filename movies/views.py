from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .temp_data import movie_data

def detail_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if 'last_viewed' not in request.session:
        request.session['last_viewed'] = []
    request.session['last_viewed'] = [movie_id] + request.session['last_viewed']
    if len(request.session['last_viewed']) > 5:
        request.session['last_viewed'] = request.session['last_viewed'][:-1]
    context = {'movie': movie}
    return render(request, 'movies/detail.html', context)

from django.shortcuts import render



def list_movies(request):
    context = {"movie_list": movie_data}
    return render(request, 'movies/index.html', context)

def search_movies(request):
    context = {}
    if request.GET.get('query', False):
        context = {
            "movie_list": [
                m for m in movie_data
                if request.GET['query'].lower() in m['name'].lower()
            ]
        }
    return render(request, 'movies/search.html', context)

from django.http import HttpResponseRedirect
from django.urls import reverse

def create_movie(request):
    if request.method == 'POST':
        movie_data.append({
            'name': request.POST['name'],
            'release_year': request.POST['release_year'],
            'poster_url': request.POST['poster_url']
        })
        return HttpResponseRedirect(
            reverse('movies:detail', args=(len(movie_data), )))
    else:
        return render(request, 'movies/create.html', {})
    
class MovieListView(generic.ListView):
    model = Movie
    template_name = 'movies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'last_viewed' in self.request.session:
            context['last_movies'] = []
            for movie_id in self.request.session['last_viewed']:
                context['last_movies'].append(
                    get_object_or_404(Movie, pk=movie_id))
        return context
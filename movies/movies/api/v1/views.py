from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from movies.models import Filmwork, PersonFilmWork


class MoviesApiMixin(ListView):
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        filmworks = Filmwork.objects.values(
            'id', 'creation_date', 'rating', 'type', 'title', 'description'
        ).annotate(
            genres=ArrayAgg(
                'genres__name',
                distinct=True),
            actors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmWork.Role.ACTOR),
                distinct=True),
            directors=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmWork.Role.DIRECTOR),
                distinct=True),
            writers=ArrayAgg(
                'persons__full_name',
                filter=Q(personfilmwork__role=PersonFilmWork.Role.WRITER),
                distinct=True),
        )
        return filmworks
    
    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        prev_page = None
        next_page = None
        if page.has_previous():
            prev_page = page.previous_page_number()
        if page.has_next():
            next_page = page.next_page_number()
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": prev_page,
            "next": next_page,
            "results": list(queryset)
        }


class MoviesDetailApi(MoviesApiMixin, DetailView):
    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        context = queryset.get(id=self.kwargs['pk'])
        return context

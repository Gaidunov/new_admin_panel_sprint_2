# import os
# import django
# import datetime
# from django.db.models import Q, F
# from django.db import connection
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# django.setup()
# from django.db import connection
# from movies.models import Genre
# from movies.models import GenreFilmwork
# from movies.models import Filmwork
# from movies.models import Person



# genres = Genre.objects.all()
# connection.queries  # []
# print(genres)
# print(connection.queries)  # [{'sql': 'SELECT "content"."genre"."created_at", "content"."genre"."updated_at", "content"."genre"."id", "content"."genre"."name", "content"."genre"."description" FROM "content"."genre" LIMIT 21', 'time': '0.005'}]
# print(len(connection.queries))  # 1


# не оптимальный запрос
# filmworks_genres = GenreFilmwork.objects.all()[:3]
# for filmwork_genre in filmworks_genres:
#     print(filmwork_genre.film_work.title, filmwork_genre.genre.name) 
# оптимальный запрос 
# filmworks_genres = GenreFilmwork.objects.all().select_related('film_work', 'genre')[:3]
# for filmwork_genre in filmworks_genres:
#     print(filmwork_genre.film_work.title, filmwork_genre.genre.name)


# не оптимально (21 запрос к базе)
# star_wars_films = Filmwork.objects.filter(title__icontains='Star Wars')[:10]
# for filmwork in star_wars_films:
#     print(filmwork.genres.all())
#     print(filmwork.persons.all())
# этот же запрос (3 запроса к базе)
# star_wars_films = Filmwork.objects.prefetch_related('genres', 'persons').filter(title__icontains='Star Wars')[:10]
# for filmwork in star_wars_films:
#     print(filmwork.genres.all())
#     print(filmwork.persons.all())


# all_genres = Genre.objects.all()
# print(all_genres[:5])
# print(all_genres[5:10])

# star_wars_films = Filmwork.objects.prefetch_related('genres', 'persons').filter(title__icontains='Star Wars')[:10]
# for filmwork in star_wars_films:
#     print(filmwork.genres.all())
#     print(filmwork.persons.filter(full_name='Robert'))

# p = Filmwork.objects.filter(rating__gte=8, creation_date__gte=datetime.date(year=2020, month=1, day=1)) 
# print(p)
# исп OR
# p = Filmwork.objects.filter(Q(rating__gte=8)|Q(creation_date__gte=datetime.date(year=2020, month=1, day=1))) 

# print(p)
# Получаем кинопроизведения одного режисера
# need_to_increase_rating = Filmwork.objects.filter(persons__full_name='Samuli Torssonen')
# print(need_to_increase_rating)
# прибавить к рэйтингу +0,2 к фильмам одного режисера
# не оптимальный запрос 
# for film in need_to_increase_rating:
#     film.rating += 0.2
#     film.save()
# более оптимальный(выполняет все за один запрос)
# need_to_increase_rating.update(rating=F('rating')+0.2)

# выполнение SQL С ограничениями 
# film = Filmwork.objects.raw('SELECT id, age(creation_date) AS age FROM content.Filmwork;')[0]
# print(film.title, film.age)


# Выполнение любых SQL
# with connection.cursor() as cursor:
#     cursor.execute(r'''UPDATE "content"."person" SET full_name = regexp_replace(full_name, '(\w+)(\W+)(\w+)', '\3\2\1');''')


# что бы научить джангу использовать незнакомый метод

# from django.db.models import F, Func

# class SwitchFullname(Func):
#     function = 'regexp_replace'  
#     template = r'''%(function)s(%(expressions)s, '(\w+)(\W+)(\w+)', '\3\2\1')'''  

# Person.objects.update(full_name=SwitchFullname(F('full_name'))) 

# Person.objects.create(full_name='John Doe', birth_date=datetime.date.today()) 
from django.http import JsonResponse, HttpResponse

from users.models import Token

from .models import Track, Playlist



def valid_token_required(fn):
    def wrapped(request, *args, **kwargs):
        provided = request.headers.get('token')
        if provided:
            user = Token.validate_token(provided)
            if user is not None:
                request.user = user
                return fn(request, *args, **kwargs)
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    return wrapped


def tracks_list(request):
    tracks = Track.objects.all()
    return JsonResponse({'objects': [track.to_json() for track in tracks]})


@valid_token_required
def playlists_list(request):
    playlists = Playlist.objects.filter(owner=request.user).all()
    return JsonResponse({'objects': [pl.to_json() for pl in playlists]})
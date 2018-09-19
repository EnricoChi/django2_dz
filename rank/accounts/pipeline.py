def user_activate(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        user.is_active = True
        user.save()
    return

# TODO: ловить аватар юзера из гугла

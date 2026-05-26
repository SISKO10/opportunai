from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def login_view(request):
    """
    Vue de la page de connexion
    """

    # Si l'utilisateur est déjà connecté
    # on le redirige vers l'accueil
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        # On récupère les données du formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')

        # On vérifie les identifiants
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Identifiants corrects → on connecte
            login(request, user)
            messages.success(request, f'Bienvenue {username} !')
            return redirect('/')
        else:
            # Identifiants incorrects → message d'erreur
            messages.error(request, 'Identifiants incorrects !')

    return render(request, 'accounts/login.html')


def register_view(request):
    """
    Vue de la page d'inscription
    """

    # Si l'utilisateur est déjà connecté
    # on le redirige vers l'accueil
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        # On utilise le formulaire Django intégré
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # Formulaire valide → on crée l'utilisateur
            user = form.save()

            # On connecte automatiquement après inscription
            login(request, user)
            messages.success(request, f'Compte créé avec succès !')
            return redirect('/')
        else:
            # Formulaire invalide → on affiche les erreurs
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    """
    Vue de déconnexion
    """
    logout(request)
    messages.success(request, 'Vous avez été déconnecté !')
    return redirect('/login/')

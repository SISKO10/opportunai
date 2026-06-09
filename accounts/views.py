from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordChangeForm


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



@login_required(login_url='/login/')
def profil_view(request):
    """
    Vue de la page de profil utilisateur
    """

    # Nombre d'alertes actives de l'utilisateur
    from opportunities.models import Alert
    nb_alertes = Alert.objects.filter(
        email=request.user.email,
        is_active=True
    ).count()

    context = {
        'nb_alertes': nb_alertes,
    }

    return render(request, 'accounts/profil.html', context)


@login_required(login_url='/login/')
def modifier_profil_view(request):
    """
    Vue de modification du profil
    """
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Mettre à jour l'utilisateur
        request.user.email = email
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.save()

        messages.success(request, 'Profil mis à jour avec succès !')
        return redirect('/profil/')

    return render(request, 'accounts/modifier_profil.html')



@login_required(login_url='/login/')
def changer_mot_de_passe_view(request):
    """
    Vue de changement de mot de passe
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            # Sauvegarde le nouveau mot de passe
            user = form.save()

            # Maintient la session active après changement
            update_session_auth_hash(request, user)

            messages.success(
                request,
                'Mot de passe modifié avec succès !'
            )
            return redirect('/profil/')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'accounts/changer_mot_de_passe.html',
        {'form': form}
    )

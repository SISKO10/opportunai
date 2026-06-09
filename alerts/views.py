from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from opportunities.models import Alert


@login_required(login_url='/login/')
def alertes_view(request):
    """
    Vue de gestion des alertes
    Affiche les alertes de l'utilisateur
    et permet d'en créer de nouvelles
    """

    # Récupère les alertes de l'utilisateur connecté
    mes_alertes = Alert.objects.filter(
        email=request.user.email,
        is_active=True
    )

    if request.method == 'POST':

        # Récupère les données du formulaire
        keywords = request.POST.get('keywords')
        country = request.POST.get('country', '')
        type_offre = request.POST.get('type', '')

        # Vérifie que l'email est renseigné
        if not request.user.email:
            messages.error(
                request,
                'Veuillez renseigner votre email dans votre profil !'
            )
            return redirect('/profil/modifier/')

        # Crée l'alerte
        Alert.objects.create(
            email=request.user.email,
            keywords=keywords,
            country=country,
            type=type_offre,
            is_active=True
        )

        messages.success(
            request,
            f'Alerte créée ! Vous recevrez les opportunités contenant "{keywords}"'
        )
        return redirect('/alertes/')

    context = {
        'mes_alertes': mes_alertes,
    }

    return render(request, 'alerts/alertes.html', context)


@login_required(login_url='/login/')
def supprimer_alerte_view(request, pk):
    """
    Vue de suppression d'une alerte
    """
    try:
        alerte = Alert.objects.get(
            id=pk,
            email=request.user.email
        )
        alerte.is_active = False
        alerte.save()
        messages.success(request, 'Alerte supprimée !')
    except Alert.DoesNotExist:
        messages.error(request, 'Alerte introuvable !')

    return redirect('/alertes/')

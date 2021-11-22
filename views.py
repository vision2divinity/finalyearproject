import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from src_votting.settings import EMAIL_HOST_USER

from .models import Candidate, Vote, Voter


def Home(request):
    if request.method == 'POST' and 'Login' in request.POST:
        # Getting data from form submitted
        data = request.POST

        # Check School Email
        if not User.objects.filter(email = data['school_email']).exists():
            messages.info(request, 'Email does not exist')
        else:
            user = authenticate(
                username=data['school_email'], password=data['password'])

            # Create voter with email
            new_voter = Voter(email=data['school_email'])
            if not Voter.objects.filter(email=data['school_email']).exists():
                new_voter.save()

            # GET AND CHECK STATUS OF CODE
            get_code = Voter.objects.get(email=data['school_email'])
            if get_code.sent_code == False:
                subject = "Code for votting"
                message = f'Your 6 digit pin for votting is {get_code.code}'
                recepient = data['school_email']
                # Send mail
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
                get_code.sent_code = True
                get_code.save()

            # Log user in
            if user is not None:
                login(request, user)
                return redirect('comfirmation')
            else:
                messages.info(request, 'Invalid credientails')

    return render(request, 'votting/index.html')


@login_required(login_url='home')
def comfirmCode(request):
    if request.method == 'POST':
        data = request.POST
        code = data['code']
        
        #Check if code exist in database
        if Voter.objects.filter(code=code).exists():
            return redirect('votting')
        else:
            messages.warning(request, 'Invalid code')
            logout(request)
            redirect('home')


    return render(request, 'votting/comfirmation.html')


def password_reset_request(request):
    if request.method == "POST":
        data = request.POST
        associated_users = User.objects.filter(Q(email=data['email']))
        # Check if user exists
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name_path = 'votting/password_reset_email.txt'
                c = {
                    "email": user.email,
                    "domain": 'aitsrcvoting.tech',
                    'site_name': 'Ait src voting',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http'
                }
                email = render_to_string(email_template_name_path, c)
                try:
                    send_mail(subject, email, EMAIL_HOST_USER, [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('password_reset_done')

    return render(request, 'votting/password_reset.html')


@login_required(login_url='home')
def VottingPage(request):
    candidates = Candidate.objects.all()
    if request.method == 'POST' and 'Submit Ballot' in request.POST:
        logout(request)
        return redirect('success')

    context = {
        'candidates': candidates,
    }
    return render(request, 'votting/voting.html', context)


def SuccessPage(request):
    return render(request, 'votting/voting-success.html')


def results(request):
    total_votes = Vote.objects.all()
    # Pie chart
    labels = []
    data = []

    for vote in total_votes:
        labels.append(vote.candidate)
        data.append(vote.votes)


    context = {
        'total_votes': total_votes,
        'labels':labels,
        'data':data
    }
    return render(request, 'votting/results.html', context)

@login_required(login_url='home')
def handleVote(request):
    data = json.loads(request.body)
    candidateID = data['id']
    candidate = Candidate.objects.get(id=candidateID)

    # Authenticating user
    if request.user.is_authenticated:
        # new_vote = Vote.objects.all()
        new_vote = Vote.objects.get(candidate=candidate)
        user = request.user
        # Update vote or create new vote
        if not Vote.objects.filter(voter=request.user):
            new_vote.votes += 1
            new_vote.voter.add(request.user)
            new_vote.save()
            messages.info(
                request, "Thank you for voting in this election. Meanwhile kindly use this link to view election result as its ongoing ")
        else:
            messages.info(request, "Sorry you can not vote twice")

    return JsonResponse('Get id', safe=False)

from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from .forms import SignUpForm, UserUpdateForm, PollForm, ChoiceFormSet
from .models import Poll, Choice, Vote

def home(request):
    """Home page showing all polls with filtering."""
    polls = Poll.objects.all()

    # Filtering logic
    creator_name = request.GET.get('creator_name')
    voted_status = request.GET.get('voted_status')
    poll_status = request.GET.get('poll_status')

    if creator_name:
        # Filter by username containing the search phrase (case-insensitive)
        polls = polls.filter(created_by__username__icontains=creator_name)

    if poll_status:
        now = timezone.now()
        if poll_status == 'ongoing':
            polls = polls.filter(start_date__lte=now, end_date__gt=now)
        elif poll_status == 'ended':
            polls = polls.filter(end_date__lte=now)
        elif poll_status == 'not_started':
            polls = polls.filter(start_date__gt=now)

    if request.user.is_authenticated and voted_status:
        voted_poll_ids = request.user.user_votes.values_list('poll_id', flat=True)
        if voted_status == 'voted':
            polls = polls.filter(id__in=voted_poll_ids)
        elif voted_status == 'not_voted':
            polls = polls.exclude(id__in=voted_poll_ids)

    # If the user is not a manager, hide suspended polls
    if not request.user.has_perm('comm_polls.can_suspend_poll'):
        polls = polls.filter(is_suspended=False)

    context = {
        'polls': polls,
        'filters': request.GET,
    }
    return render(request, "comm_polls/home.html", context)


@login_required
def polls_list(request):
    """Show all polls created by the user."""
    polls = Poll.objects.filter(created_by=request.user)
    return render(request, "comm_polls/polls_list.html", {"polls": polls})


@login_required
def my_votes(request):
    """Show polls the user has voted on."""
    user_votes = Vote.objects.filter(voter=request.user).select_related(
        'poll', 'choice'
    ).prefetch_related(
        'poll__choices'  # Efficiently prefetch all choices for the polls
    )
    return render(request, "comm_polls/my_votes.html", {"user_votes": user_votes})


@login_required
def create_poll(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)
        if poll_form.is_valid() and choice_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()
            # Save choices
            choice_formset.instance = poll
            choice_formset.save()
            messages.success(request, 'Poll created successfully!')
            return redirect('comm_polls:polls')
    else:
        poll_form = PollForm()
        choice_formset = ChoiceFormSet()

    return render(
        request, 
        'comm_polls/create_poll.html', 
        {'poll_form': poll_form, 'choice_formset': choice_formset}
    )


@login_required
def manage_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)

    if request.method == 'POST':
        if 'close_poll' in request.POST:
            poll.end_date = timezone.now()
            poll.save()
            messages.success(request, 'Poll has been closed.')
            return redirect('comm_polls:manage_poll', poll_id=poll.id)

    # Sort choices by vote count
    choices = poll.choices.all().order_by('-votes_count')

    return render(request, "comm_polls/manage_poll.html", {"poll": poll, "choices": choices})


@login_required
def delete_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, created_by=request.user)
    if request.method == 'POST':
        poll.delete()
        messages.success(request, 'Poll deleted successfully.')
        return redirect('comm_polls:polls')
    return render(request, 'comm_polls/delete_poll.html', {'poll': poll})


@login_required
@permission_required('comm_polls.can_suspend_poll', raise_exception=True)
def suspend_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    # Toggle the suspended state
    poll.is_suspended = not poll.is_suspended
    poll.save()
    return redirect('comm_polls:home')


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.has_started:
        return redirect('comm_polls:poll_countdown', poll_id=poll.id)

    if poll.has_ended:
        messages.warning(request, 'This poll has already ended.')
        return redirect('comm_polls:results', poll_id=poll.id)

    if poll.poll_votes.filter(voter=request.user).exists():
        messages.warning(request, 'You have already voted on this poll.')
        return redirect('comm_polls:results', poll_id=poll.id)

    if request.method == 'POST':
        try:
            selected_choice_id = request.POST['choice']
            selected_choice = poll.choices.get(id=selected_choice_id)
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'comm_polls/vote.html', {
                'poll': poll,
                'error_message': "You didn't select a choice.",
            })
        else:
            with transaction.atomic():
                Vote.objects.create(poll=poll, choice=selected_choice, voter=request.user)
                selected_choice.votes_count += 1
                selected_choice.save()

            messages.success(request, 'Your vote has been recorded!')
            return redirect('comm_polls:results', poll_id=poll.id)
    
    return render(request, "comm_polls/vote.html", {"poll": poll})


@login_required
def results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = poll.choices.order_by('-votes_count')

    # Get the user's vote for this poll, if it exists
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(poll=poll, voter=request.user)
        except Vote.DoesNotExist:
            user_vote = None

    context = {
        "poll": poll,
        "choices": choices,
        "user_vote": user_vote,
    }
    return render(request, "comm_polls/results.html", context)


@login_required
def poll_countdown(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if poll.has_started:
        return redirect('comm_polls:vote', poll_id=poll.id)
    return render(request, "comm_polls/poll_countdown.html", {"poll": poll})


def poll_results_api(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = poll.choices.all()
    results = {choice.id: choice.votes_count for choice in choices}
    return JsonResponse(results)


def signup(request):
    """Sign-up view for new users."""
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("comm_polls:home")
    else:
        form = SignUpForm()
    return render(request, "comm_polls/signup.html", {"form": form})


@login_required
def account_settings(request):
    """Allow users to update account details."""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details have been updated.')
            return redirect('comm_polls:account_settings')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'comm_polls/account_settings.html', {'form': form})

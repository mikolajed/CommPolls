from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserUpdateForm, PollForm, ChoiceFormSet
from .models import Poll

def home(request):
    """Home page showing all polls."""
    polls = Poll.objects.all()
    return render(request, "comm_polls/home.html", {"polls": polls})


@login_required
def polls_list(request):
    """Show all polls created by the user."""
    polls = Poll.objects.filter(created_by=request.user)
    return render(request, "comm_polls/polls_list.html", {"polls": polls})


@login_required
def my_votes(request):
    """Show polls the user has voted on (placeholder)."""
    return render(request, "comm_polls/my_votes.html")


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
    """Manage a specific poll (placeholder)."""
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, "comm_polls/manage_poll.html", {"poll": poll})


@login_required
def vote(request, poll_id):
    """Vote on a poll (placeholder)."""
    poll = get_object_or_404(Poll, id=poll_id)
    return render(request, "comm_polls/vote.html", {"poll": poll})


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

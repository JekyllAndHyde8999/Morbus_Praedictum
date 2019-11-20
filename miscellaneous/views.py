from django.shortcuts import render
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='P_login')
def feedbackView(request):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.username = request.user.username
            feedback.save()
        else:
            messages.error(request, "Error")
    return render(request, 'miscellaneous/feedback.html', {'form':form})
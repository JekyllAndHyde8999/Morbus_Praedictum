from django.shortcuts import render
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def feedbackView(request):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.save()
    return render(request, 'miscellaneous/feedback.html', {'form': form})
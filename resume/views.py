from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Job, Application, Profile
from .forms import ProfileForm, JobApplicationForm
from .models import Application
from .models import Resume
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    return render(request, 'resume/home.html')

@login_required
def dashboard(request):
    user = request.user
    applications = Application.objects.filter(user=user)
    total_applications = applications.count()
    pending_count = applications.filter(status="Pending").count()
    approved_count = applications.filter(status="Approved").count()
    rejected_count = applications.filter(status="Rejected").count()

    context = {
        "user": user,
        "total_applications": total_applications,
        "pending_count": pending_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
    }
    return render(request, "resume/dashboard.html", context)


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "Account created! Please login.")
        return redirect('login')

    return render(request, 'resume/register.html')

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        profile.bio = request.POST.get('bio')
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()

        return redirect('profile')

    return render(request, 'resume/edit_profile.html', {'profile': profile})

@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'resume/job_list.html', {'jobs': jobs})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    existing_application = Application.objects.filter(user=request.user, job=job).first()
    if existing_application:
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_list')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.job = job
            try:
                application.save()

                # ✅ Send email
                subject = "Job Application Submitted"
                message = (
                    f"Hi {request.user.first_name},\n\n"
                    f"You have successfully applied for the position: {job.title}.\n\n"
                    f"We will review your application and get back to you soon.\n\n"
                    f"Best regards,\nTeam Resume Portal"
                )
                recipient_list = [request.user.email]
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

                messages.success(request, 'Your application has been submitted successfully!')
                return redirect('job_list')
            except Exception as e:
                messages.error(request, 'Error submitting application. Please try again.')
    else:
        form = JobApplicationForm()

    return render(request, 'resume/apply_job.html', {
        'form': form,
        'job': job
    })

@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-applied_at')
    return render(request, 'resume/my_applications.html', {'applications': applications})

@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    return render(request, 'resume/profile.html', {'profile': profile})
def submit_resume(request):
    # your logic to save resume
    return redirect('home')


def edit_resume(request, id):
    resume = get_object_or_404(Resume, pk=id)

    if request.method == 'POST':
        resume.name = request.POST.get('name')
        resume.email = request.POST.get('email')
        resume.phone = request.POST.get('phone')
        resume.position = request.POST.get('position')
        resume.skills = request.POST.get('skills')

        if 'resume_file' in request.FILES:
            resume.resume_file = request.FILES['resume_file']

        resume.save()
        return redirect('home')

    return render(request, 'resume/edit_resume.html', {'resume': resume})

def delete_resume(request, id):
    resume = get_object_or_404(Resume, pk=id)
    resume.delete()
    return redirect('home')
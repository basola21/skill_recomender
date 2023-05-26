from django.shortcuts import render,redirect
from .models import Job,Profile,Blog,Skill
from .forms import RegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Q
from .recommendation import get_best_skills


def index(request):
    # getting the information technology jobs
    it_job_count = Job.objects.filter(skills__name__in=['information technology']).count()

    # getting all jobs with the skill of sales
    sales_job_count = Job.objects.filter(skills__name__in=['sales']).count()

    # getting all jobs with the skill of software engineering
    se_job_count = Job.objects.filter(skills__name__in=['software engineering']).count()

    # getting all jobs with the skill of programming
    programming_job_count = Job.objects.filter(skills__name__in=['python']).count()

    context = {
        'it_job_count': it_job_count,
        'sales_job_count': sales_job_count,
        'se_job_count': se_job_count,
        'programming_job_count': programming_job_count
    }

    return render(request, 'app/index.html', context)


def about(request):
    return render(request, 'app/about.html')



def jobs(request):
    job_list = Job.objects.all()
    interests = ['Enterprising', 'Conventional', 'Artistic', 'Social', 'Investigative', 'Realistic']

    # Handle form submission and search query
    query = request.GET.get('q')
    interest = request.GET.get('interest')
    
    if query:
        job_list = job_list.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if interest:
        job_list = job_list.filter(interest=interest)

    # Create paginator and get current page number
    paginator = Paginator(job_list, 10)
    page = request.GET.get('page')

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    context = {'jobs':jobs}

    return render(request, 'app/job-list.html',context)


def job_details(request,id):
    job_detail = Job.objects.get(id)
    context = {'job':job_detail}
    return render(request, 'app/job_details.html',context)

def blog(request):
    blogs = Blog.objects.all()
    context = {"blogs":blogs}
    return render(request, 'app/blog.html',context)

def contact(request):

    if request.method == 'POST':
        return

    return render(request, 'app/contact.html')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
	
    form = AuthenticationForm()

    return render(request, 'app/sign-in.html',context={"form":form})

def register(request):
    form = RegisterForm
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.error(request, 'Please enter correct details')
            return render(request, 'app/sign-up.html', {'form': form})

    return render(request, 'app/sign-up.html', {'form': form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("index")



@login_required
def profile(request):

    try:
        profile = request.user.profile  # changed to lowercase profile
    except Profile.DoesNotExist:  # changed to uppercase Profile
        # create a new profile for the user
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)  # changed to uppercase Profile

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)  # changed to uppercase Profile

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'app/profile.html', context)

def skills(request):
    job = request.GET.get('job')

    if job:
        skills = get_best_skills(job)
        print(skills)

    else:
        skills = []


    context = {'skills': skills}
    return render(request, 'app/skills.html', context)




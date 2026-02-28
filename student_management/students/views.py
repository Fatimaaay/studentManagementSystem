
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from .models import Student, UserProfile


def signup(request):
    if request.method == 'POST':
        # Get data from form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('signup')

        # Create user (but don't activate yet)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_active = False  # User can't login until email verified
        user.save()

        # Create user profile with verification token
        profile = UserProfile.objects.create(user=user)

        # Send verification email
        current_site = get_current_site(request)
        verification_link = f"http://{current_site.domain}/verify-email/{profile.verification_token}/"

        subject = 'Verify Your Email - Student Management System'
        message = f"""
Hello {username},

Thank you for registering!

Please click the link below to verify your email address:
{verification_link}

This link will expire in 24 hours.

If you didn't create this account, please ignore this email.

Best regards,
Student Management Team
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(request, 'Registration successful! Please check your email to verify your account.')
        return redirect('login')

    return render(request, 'signup.html')


from django.shortcuts import get_object_or_404


def verify_email(request, token):
    # Find the profile with this token
    profile = get_object_or_404(UserProfile, verification_token=token)

    # Check if token is still valid
    if not profile.is_token_valid():
        messages.error(request, 'Verification link has expired!')
        return redirect('signup')

    # Check if already verified
    if profile.email_verified:
        messages.info(request, 'Email already verified! You can login.')
        return redirect('login')

    # Activate the user
    profile.email_verified = True
    profile.save()

    user = profile.user
    user.is_active = True
    user.save()

    messages.success(request, 'Email verified successfully! You can now login.')
    return redirect('login')


from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if email is verified
            try:
                profile = UserProfile.objects.get(user=user)
                if not profile.email_verified:
                    messages.error(request, 'Please verify your email first!')
                    return redirect('login')
            except UserProfile.DoesNotExist:
                pass  # Old users without profile can still login

            # Login the user
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


from django.contrib.auth.decorators import login_required
from .models import Student
from django.db.models import Q


@login_required(login_url='login')
def dashboard(request):
    # Get search query if exists
    search_query = request.GET.get('search', '')

    # Get all students or filter by search
    if search_query:
        students = Student.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(course__icontains=search_query)
        )
    else:
        students = Student.objects.all()

    # Count total students
    total_students = Student.objects.count()

    context = {
        'students': students,
        'total_students': total_students,
        'search_query': search_query,
    }

    return render(request, 'dashboard.html', context)





@login_required(login_url='login')
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        course = request.POST['course']

        # Validation
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Student with this email already exists!')
            return redirect('add_student')

        # Create student
        Student.objects.create(
            name=name,
            email=email,
            phone=phone,
            course=course
        )

        messages.success(request, f'Student {name} added successfully!')
        return redirect('dashboard')

    return render(request, 'add_student.html')


@login_required(login_url='login')
def edit_student(request, student_id):
    # Get the student or show 404
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.phone = request.POST['phone']
        student.course = request.POST['course']

        # Check if email changed and if new email exists
        if Student.objects.filter(email=student.email).exclude(id=student_id).exists():
            messages.error(request, 'Email already exists!')
            return redirect('edit_student', student_id=student_id)

        student.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('dashboard')

    context = {'student': student}
    return render(request, 'edit_student.html', context)


@login_required(login_url='login')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student_name = student.name
    student.delete()

    messages.success(request, f'Student {student_name} deleted successfully!')
    return redirect('dashboard')
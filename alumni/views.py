from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import User, AlumniProfile, OTP
from .forms import AlumniRegistrationForm, ProfileEditForm
from .services.email import EmailService


def home(request):
    recent_alumni = AlumniProfile.objects.select_related('user').order_by('-created_at')[:6]
    return render(request, 'alumni/home.html', {'recent_alumni': recent_alumni})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('directory')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'No account found with this email.')
            return render(request, 'alumni/login.html', {'email': email})

        otp = OTP.generate(email)
        EmailService.send_otp(email, otp.code)

        request.session['login_email'] = email
        messages.success(request, f'OTP sent to {email}. Please check your inbox.')
        return redirect('login_verify_otp')

    return render(request, 'alumni/login.html')


def login_verify_otp(request):
    if request.user.is_authenticated:
        return redirect('directory')

    if request.method == 'POST':
        code = request.POST.get('otp_code', '').strip()
        email = request.session.get('login_email')

        if not email:
            messages.error(request, 'Session expired. Please login again.')
            return redirect('login')

        user = User.objects.filter(email=email).first()
        if not user or not user.alumni_profile:
            messages.error(request, 'No account found with this email.')
            request.session.pop('login_email', None)
            return redirect('login')

        otp = OTP.objects.filter(email=email, code=code).first()

        if not otp or not otp.is_valid():
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            return render(request, 'alumni/login_verify_otp.html', {'email': email})

        otp.delete()
        request.session.pop('login_email', None)

        login(request, user)
        messages.success(request, f'Welcome back, {user.get_full_name() or user.email}!')
        return redirect('directory')

    return render(request, 'alumni/login_verify_otp.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            email = cleaned['email']

            existing_user = User.objects.filter(email=email).first()
            if existing_user and existing_user.alumni_profile:
                messages.error(request, 'This email is already registered.')
                return render(request, 'alumni/register.html', {
                    'form': form,
                    'departments': settings.DEPARTMENTS,
                    'visit_freq_choices': [
                        ('monthly', 'Monthly'),
                        ('quarterly', 'Quarterly'),
                        ('yearly', 'Yearly'),
                        ('rarely', 'Rarely'),
                        ('never', 'Never'),
                    ],
                    'support_mode_choices': [
                        ('online', 'Online'),
                        ('offline', 'Offline'),
                        ('both', 'Both Online & Offline'),
                        ('not_possible', 'Not Possible'),
                    ],
                })

            otp = OTP.generate(email)
            EmailService.send_otp(email, otp.code)

            request.session['reg_data'] = {
                'first_name': cleaned['first_name'],
                'last_name': cleaned['last_name'],
                'email': cleaned['email'],
                'phone': cleaned['phone'],
                'department': cleaned['department'],
                'year_of_passing': cleaned['year_of_passing'],
                'current_company': cleaned.get('current_company', ''),
                'current_role': cleaned.get('current_role', ''),
                'current_city': cleaned.get('current_city', ''),
                'native_location': cleaned.get('native_location', ''),
                'support_mode': cleaned.get('support_mode', ''),
                'visit_frequency_coimbatore': cleaned.get('visit_frequency_coimbatore', ''),
                'free_to_talk_days': cleaned.get('free_to_talk_days', ''),
                'willing_to_mentor': cleaned.get('willing_to_mentor', False),
                'support_offered': cleaned.get('support_offered', ''),
            }
            if 'profile_photo' in cleaned and cleaned['profile_photo']:
                import base64
                photo = cleaned['profile_photo']
                request.session['reg_data']['profile_photo'] = {
                    'name': photo.name,
                    'content': base64.b64encode(photo.read()).decode('utf-8'),
                }

            messages.success(request, f'OTP sent to {email}. Please check your inbox.')
            return redirect('verify_otp')
        else:
            return render(request, 'alumni/register.html', {
                'form': form,
                'departments': settings.DEPARTMENTS,
                'visit_freq_choices': [
                    ('monthly', 'Monthly'),
                    ('quarterly', 'Quarterly'),
                    ('yearly', 'Yearly'),
                    ('rarely', 'Rarely'),
                    ('never', 'Never'),
                ],
                'support_mode_choices': [
                    ('online', 'Online'),
                    ('offline', 'Offline'),
                    ('both', 'Both Online & Offline'),
                    ('not_possible', 'Not Possible'),
                ],
            })

    return render(request, 'alumni/register.html', {
        'form': AlumniRegistrationForm(),
        'departments': settings.DEPARTMENTS,
        'visit_freq_choices': [
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
            ('rarely', 'Rarely'),
            ('never', 'Never'),
        ],
        'support_mode_choices': [
            ('online', 'Online'),
            ('offline', 'Offline'),
            ('both', 'Both Online & Offline'),
            ('not_possible', 'Not Possible'),
        ],
    })


def verify_otp(request):
    if request.method == 'POST':
        code = request.POST.get('otp_code', '').strip()
        reg_data = request.session.get('reg_data')

        if not reg_data:
            messages.error(request, 'Session expired. Please register again.')
            return redirect('register')

        email = reg_data['email']
        otp = OTP.objects.filter(email=email, code=code).first()

        if not otp or not otp.is_valid():
            messages.error(request, 'Invalid or expired OTP. Please try again.')
            return render(request, 'alumni/verify_otp.html', {
                'email': email,
            })

        otp.delete()

        user = User.objects.create_user(
            username=email,
            email=email,
            phone=reg_data['phone'],
            first_name=reg_data['first_name'],
            last_name=reg_data['last_name'],
        )

        profile = AlumniProfile.objects.create(
            user=user,
            first_name=reg_data['first_name'],
            last_name=reg_data['last_name'],
            email=email,
            phone=reg_data['phone'],
            department=reg_data['department'],
            year_of_passing=reg_data['year_of_passing'],
            current_company=reg_data.get('current_company', ''),
            current_role=reg_data.get('current_role', ''),
            current_city=reg_data.get('current_city', ''),
            native_location=reg_data.get('native_location', ''),
            support_mode=reg_data.get('support_mode', ''),
            visit_frequency_coimbatore=reg_data.get('visit_frequency_coimbatore', ''),
            free_to_talk_days=reg_data.get('free_to_talk_days', ''),
            willing_to_mentor=reg_data.get('willing_to_mentor', False),
            support_offered=reg_data.get('support_offered', ''),
        )

        if 'profile_photo' in reg_data:
            from django.core.files.base import ContentFile
            import base64
            photo_data = reg_data['profile_photo']
            profile.profile_photo.save(
                photo_data['name'],
                ContentFile(base64.b64decode(photo_data['content'])),
                save=False,
            )

        request.session.pop('reg_data', None)
        messages.success(request, 'Registration successful! You are now in the alumni directory.')
        return redirect('directory')

    return render(request, 'alumni/verify_otp.html')


def directory(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to access the alumni directory.')
        return redirect('login')

    sort = request.GET.get('sort', 'name_asc')
    profiles = AlumniProfile.objects.select_related('user')

    department = request.GET.get('department', '')
    year = request.GET.get('year', '')
    search = request.GET.get('search', '')

    if department:
        profiles = profiles.filter(department=department)
    if year:
        profiles = profiles.filter(year_of_passing=int(year))
    if search:
        profiles = profiles.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(current_company__icontains=search) |
            Q(current_role__icontains=search) |
            Q(email__icontains=search)
        )

    if sort == 'name_desc':
        profiles = profiles.order_by('-first_name', '-last_name')
    elif sort == 'year_asc':
        profiles = profiles.order_by('year_of_passing', 'first_name', 'last_name')
    elif sort == 'year_desc':
        profiles = profiles.order_by('-year_of_passing', 'first_name', 'last_name')
    else:
        profiles = profiles.order_by('first_name', 'last_name')

    departments = settings.DEPARTMENTS
    years = AlumniProfile.objects.values_list('year_of_passing', flat=True).distinct().order_by('year_of_passing')

    paginator = Paginator(profiles, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'departments': departments,
        'years': years,
        'selected_department': department,
        'selected_year': year,
        'search': search,
        'can_see_full': True,
    }
    return render(request, 'alumni/directory.html', context)


def view_profile(request, profile_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to view profiles.')
        return redirect('login')

    profile = get_object_or_404(AlumniProfile, id=profile_id)
    return render(request, 'alumni/view_profile.html', {'profile': profile})


def edit_profile(request, profile_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to edit your profile.')
        return redirect('login')

    profile = get_object_or_404(AlumniProfile, id=profile_id)

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email != profile.email:
            messages.error(request, 'Email does not match this record.')
            return render(request, 'alumni/edit_profile.html', {
                'profile': profile,
                'form': ProfileEditForm(initial={
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'email': profile.email,
                    'phone': profile.phone,
                    'department': profile.department,
                    'year_of_passing': profile.year_of_passing,
                    'current_company': profile.current_company,
                    'current_role': profile.current_role,
                    'current_city': profile.current_city,
                    'native_location': profile.native_location,
                    'support_mode': profile.support_mode,
                    'visit_frequency_coimbatore': profile.visit_frequency_coimbatore,
                    'free_to_talk_days': profile.free_to_talk_days,
                    'willing_to_mentor': profile.willing_to_mentor,
                    'support_offered': profile.support_offered,
                }),
                'departments': settings.DEPARTMENTS,
            })

        form = ProfileEditForm(request.POST, request.FILES, profile=profile)
        if form.is_valid():
            cleaned = form.cleaned_data
            profile.first_name = cleaned['first_name']
            profile.last_name = cleaned['last_name']
            profile.phone = cleaned['phone']
            profile.department = cleaned['department']
            profile.year_of_passing = cleaned['year_of_passing']
            profile.current_company = cleaned.get('current_company', '')
            profile.current_role = cleaned.get('current_role', '')
            profile.current_city = cleaned.get('current_city', '')
            profile.native_location = cleaned.get('native_location', '')
            profile.support_mode = cleaned.get('support_mode', '')
            profile.visit_frequency_coimbatore = cleaned.get('visit_frequency_coimbatore', '')
            profile.free_to_talk_days = cleaned.get('free_to_talk_days', '')
            profile.willing_to_mentor = cleaned.get('willing_to_mentor', False)
            profile.support_offered = cleaned.get('support_offered', '')
            if 'profile_photo' in cleaned and cleaned['profile_photo']:
                profile.profile_photo = cleaned['profile_photo']
            profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('view_profile', profile_id=profile.id)
        else:
            messages.error(request, 'Please fix the errors below.')

    initial = {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email,
        'phone': profile.phone,
        'department': profile.department,
        'year_of_passing': profile.year_of_passing,
        'current_company': profile.current_company,
        'current_role': profile.current_role,
        'current_city': profile.current_city,
        'native_location': profile.native_location,
        'support_mode': profile.support_mode,
        'visit_frequency_coimbatore': profile.visit_frequency_coimbatore,
        'free_to_talk_days': profile.free_to_talk_days,
        'willing_to_mentor': profile.willing_to_mentor,
        'support_offered': profile.support_offered,
    }
    form = ProfileEditForm(initial=initial, profile=profile)
    return render(request, 'alumni/edit_profile.html', {
        'profile': profile,
        'form': form,
        'departments': settings.DEPARTMENTS,
        'visit_freq_choices': [
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
            ('rarely', 'Rarely'),
            ('never', 'Never'),
        ],
        'support_mode_choices': [
            ('online', 'Online'),
            ('offline', 'Offline'),
            ('both', 'Both Online & Offline'),
            ('not_possible', 'Not Possible'),
        ],
    })

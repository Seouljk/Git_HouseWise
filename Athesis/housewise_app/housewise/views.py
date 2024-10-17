from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import json
import time
#SCRIPTS

#MOBILE APP PACKAGES 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import Q
from .models import UserHousewise, LoginSession, UserType, Materials, MaterialPrice

#MOBILE APP API
@api_view(['POST'])
def login_user(request):
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    if username_or_email is None or password is None:
        return Response({"error": "Please provide both username/email and password"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # First try to get user by username
        try:
            user = UserHousewise.objects.get(username=username_or_email)
        except UserHousewise.DoesNotExist:
            # Then try to get user by email
            try:
                user = UserHousewise.objects.get(email=username_or_email)
            except UserHousewise.DoesNotExist:
                user = None

        # Check if the user exists and verify the password
        if user and user.check_password(password):
            # Perform actions upon successful login
            if user.user_type.user_type == 'user':  # Modify to check for user type
                user.last_login = timezone.now()
                user.save()

                # Create a new login session
                login_session = LoginSession.objects.create(user=user, login_time=user.last_login)

                # You might want to return session details or tokens here
                return Response({
                    "message": "Login successful",
                    "user_id": user.user_id,  # Correct access to the primary key
                    "username": user.username,
                    "email": user.email,
                    "login_session_id": login_session.loginsession_id  # Include the session ID if needed
                }, status=status.HTTP_200_OK)

            return Response({"error": "You do not have permission to access this area."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
def login_view(request):
    if request.method == 'POST':  # Handle login
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        
        try:
            user = UserHousewise.objects.get(username=username_or_email)
        except UserHousewise.DoesNotExist:
            try:
                user = UserHousewise.objects.get(email=username_or_email)
            except UserHousewise.DoesNotExist:
                user = None

        if user and user.check_password(password):
            if user.is_staff:  # Using the is_staff property
                login(request, user)
                user.last_login = timezone.now()
                user.save()

                # Create a new login session
                login_session = LoginSession.objects.create(user=user, login_time=user.last_login)
                request.session['login_session_id'] = login_session.loginsession_id  # Store session ID in session
                messages.success(request, 'Login successfully')
                next_url = request.GET.get('next')
                return redirect(next_url if next_url else reverse('menu', args=[user.username]))

            messages.error(request, 'You do not have permission to access this area.')
        else:
            messages.error(request, 'Invalid username or password.')

        return redirect('login')

    return render(request, "housewise/login.html")


@login_required(login_url='/housewise/')
@never_cache
def logout_view(request):
    if request.method == 'DELETE':  # Handle logout via a DELETE request
        if request.user.is_authenticated:
            login_session_id = request.session.pop('login_session_id', None)
            if login_session_id:
                try:
                    login_session = LoginSession.objects.get(loginsession_id=login_session_id)
                    login_session.logout_time = timezone.now()
                    login_session.login_duration = login_session.logout_time - login_session.login_time
                    login_session.save()
                except LoginSession.DoesNotExist:
                    pass

            logout(request)

            # Clear all messages after logout to prevent old messages from showing up
            storage = messages.get_messages(request)
            storage.used = True  # Marks all messages as read
            messages.info(request, 'You have been logged out.')  # Optional logout message
            # Send logout success response
            return JsonResponse({'message': 'Logged out successfully'}, status=200)

    return redirect('login')

@login_required(login_url='/housewise/')
@never_cache
def menu_view(request, username):
    return render(request, 'housewise/menu.html', {'username': username})

@login_required(login_url='/housewise/')
@never_cache
def user_list(request, username):
    user_type_user = UserType.objects.get(user_type='user')  # Get UserType object
    users = UserHousewise.objects.filter(user_type=user_type_user).order_by('-created_at')  # Fetch users
    
    # Get login sessions for each user
    selected_user = None
    login_sessions = []
    
    if 'selected_user_id' in request.GET:
        selected_user_id = request.GET.get('selected_user_id')
        selected_user = UserHousewise.objects.get(user_id=selected_user_id)
        login_sessions = selected_user.login_sessions.all().order_by('-login_time')  # Order by latest login time

    return render(request, 'housewise/user.html', {
        'users': users,
        'login_sessions': login_sessions,
        'selected_user': selected_user
    })

@login_required(login_url='/housewise/')
@never_cache
def user_login_sessions(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        try:
            user = UserHousewise.objects.get(user_id=user_id)
            login_sessions = user.login_sessions.all().order_by('-login_time')

            sessions_data = []
            for session in login_sessions:
                session_data = {
                    'login_time': session.login_time,
                    'login_duration': str(session.login_duration) if session.login_duration else None,
                }
                sessions_data.append(session_data)

            return JsonResponse({'sessions': sessions_data}, status=200)

        except UserHousewise.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='/housewise/')
@never_cache
def material_view(request, username):
    # Retrieve all materials
    materials = Materials.objects.all()
    
    # Create a list of materials with their latest prices
    materials_with_latest_price = []
    
    for material in materials:
        latest_price = MaterialPrice.objects.filter(materials=material).order_by('-date_time').first()
        if latest_price:
            materials_with_latest_price.append({
                'id': material.materials_id,  # Add material id for later AJAX use
                'name': material.materials_name,
                'latest_price': latest_price.amount
            })

    return render(request, 'housewise/materials.html', {
        'username': username,
        'materials_with_latest_price': materials_with_latest_price
    })


# New view to get all prices for a material
@login_required(login_url='/housewise/')
def get_material_prices(request):
    material_id = request.GET.get('material_id')
    if material_id:
        prices = MaterialPrice.objects.filter(materials_id=material_id).order_by('-date_time')
        price_data = [
            {'date_time': price.date_time.strftime('%Y-%m-%d %H:%M:%S'), 'amount': str(price.amount)}
            for price in prices
        ]
        return JsonResponse({'prices': price_data})
    return JsonResponse({'error': 'No material found'}, status=400)

@login_required(login_url='/housewise/')
@never_cache
def feedbacks_view(request, username):
    return render(request, 'housewise/feedbacks.html', {'username': username})

@login_required(login_url='/housewise/')
@never_cache
def script_view(request, username):
    return render(request, 'housewise/scripts.html', {'username': username})
    

@login_required(login_url='/housewise/')
@never_cache
def profile_view(request, username):
    user = get_object_or_404(UserHousewise, username=username)
    # Clear all messages after logout to prevent old messages from showing up
    storage = messages.get_messages(request)
    storage.used = True  # Marks all messages as read
    login_sessions = user.login_sessions.all().order_by('-login_time')

    if request.method == 'POST':
        # Update user fields if data is provided
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        age = request.POST.get('age')

        if name:  # Only update if a value is provided
            user.name = name
        if username:  # Only update if a value is provided
            user.username = username
        if email:  # Only update if a value is provided
            user.email = email
        if password:  # Only update if a password is provided
            user.set_password(password)  # Update password securely
        if age:  # Only update if a value is provided
            user.age = age

        user.save()  # Save the updated user profile
        return redirect('profile_view', username=user.username)  # Redirect to the profile view after saving

    return render(request, 'housewise/profile.html', {'user': user, 'login_sessions': login_sessions})

@csrf_exempt  # To exempt CSRF token validation for simplicity (in production, use proper CSRF handling)
def save_profile_changes(request, username):
    if request.method == 'POST':
        user = get_object_or_404(UserHousewise, username=username)
        
        data = json.loads(request.body)
        name = data.get('name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')  # Capture password if provided
        age = data.get('age')

        if name:
            user.name = name
        if username:
            user.username = username
        if email:
            user.email = email
        if password:  # Make sure to hash the password before saving
            user.set_password(password)  # Use set_password to hash
        if age:
            user.age = age

        user.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
import json
#SCRIPTS

#MAIL IMPORTS 
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.sessions.models import Session
from datetime import datetime, timedelta
import random
from django.utils.decorators import method_decorator


#MOBILE APP PACKAGES 
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


from django.db.models import Q
from .models import UserHousewise, LoginSession, UserType, Materials, MaterialPrice
from .serializers import UserHousewiseSerializer

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
                login_session = LoginSession.objects.create(user=user, login_time=user.last_login)
                request.session['login_session_id'] = login_session.loginsession_id  # Store session ID in session
                
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)

                # You might want to return session details or tokens here
                return Response({
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                        "email": user.email,
                        "age": user.age,
                    },
                    "token": token  # return JWT token
                }, status=status.HTTP_200_OK)

            return Response({"error": "You do not have permission to access this area."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    try:
         # Log the request headers and user details for debugging
        print(f"Request Headers: {request.headers}")
        print(f"Request User: {request.user}")

        user = request.user
        data = request.data

         # Ensure the user type is 'user'
        if user.user_type.user_type != 'user':
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)


        # Update fields
        user.name = data.get('name', user.name)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.age = data.get('age', user.age)

         # Handle password change
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if current_password and new_password and confirm_password:
            if not check_password(current_password, user.password):
                return Response({"error": "Current password does not match."}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                return Response({"error": "New password and confirm password do not match."}, status=status.HTTP_400_BAD_REQUEST)

            user.password = make_password(new_password)

        user.save()
        return Response({"message": "User profile updated successfully."}, status=status.HTTP_200_OK)

    except UserHousewise.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def check_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')

            # Check if the email exists in the database
            if UserHousewise.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email is already in use'}, status=400)
            else:
                return JsonResponse({'success': True, 'message': 'Email is available'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def check_username(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '')

            # Check if the email exists in the database
            if UserHousewise.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'username is already in use'}, status=400)
            else:
                return JsonResponse({'success': True, 'message': 'username is available'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Expiry time
        expiry_time = datetime.now() + timedelta(minutes=10)  # Set expiry time for 5 minutes
        request.session['verification_code_expiry'] = expiry_time.isoformat()

        subject = 'Your Verification Code'
        from_email = 'housewise.app@gmail.com'
        to_email = [email]
        text_content = (f'Hi, thanks much for creating an account with us. '
                        f'Your participation is very much appreciated.\n\n'
                        f'Here is your Verification Code: {verification_code}')
        html_content = (f'<p>Hi, thanks much for creating an account with us. '
                        f'Your participation is very much appreciated.</p>'
                        f'<p>Here is your Verification Code: <strong>{verification_code}</strong></p>')

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        
        try:
            msg.send()
            request.session['verification_code'] = verification_code
            return JsonResponse({'success': True, 'expires_in': 10})  # Return expiry time in minutes
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = request.session.get('verification_code')
        
        if code == stored_code:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid verification code'}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@api_view(['POST'])
def create_user_account(request):
    serializer = UserHousewiseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    return Response({"success": False, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_profile_icon(request):
    """
    Updates the user's profile icon.
    """
    user = request.user  # Authenticated user
    icon = request.data.get('icon', None)  # Get the icon from request data

    if not icon:
        return Response(
            {"error": "No icon provided."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.profile_icon = icon
    user.save()
    return Response(
        {"message": "Profile icon updated successfully.", "profile_icon": user.profile_icon},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_icon(request):
    """
    Retrieves the user's profile icon.
    """
    user = request.user  # Authenticated user
    return Response(
        {"profile_icon": user.profile_icon},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:

        print(f"User: {request.user}")  # Check if user is authenticated
        print(f"Session Data: {request.session.items()}")  # Check all session data

        # Get the current user's login session ID
        login_session_id = request.session.get('login_session_id')
        if login_session_id:
            # Get the LoginSession object and update logout details
            login_session = LoginSession.objects.get(loginsession_id=login_session_id)
            login_session.logout_time = timezone.now()
            login_session.login_duration = login_session.logout_time - login_session.login_time
            login_session.save()

            # Clear the session and log out the user
            logout(request)
            request.session.flush()  # Clear all session data

            # Send a response confirming successful logout
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'No active session found'}, status=status.HTTP_400_BAD_REQUEST)
    
    except LoginSession.DoesNotExist:
        return Response({'error': 'Login session not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#WEBSITE API
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

def login_view(request):
    if request.method == 'POST':  # Handle login
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')

        print(f"Received username_or_email: {username_or_email}")
        print(f"Received password: {password}")
        
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
    
    if 'selected_id' in request.GET:
        selected_id = request.GET.get('selected_id')
        selected_user = UserHousewise.objects.get(id=selected_id)
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
        id = request.GET.get('id')
        try:
            user = UserHousewise.objects.get(id=id)
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
    


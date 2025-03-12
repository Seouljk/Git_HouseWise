from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, logout, get_user_model
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
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.core.exceptions import ObjectDoesNotExist

    

from django.db.models import Q, Count, Avg, Max, Min
from .models import UserHousewise, LoginSession, UserType, Materials, MaterialPrice, Project, ProjectLike, Roof, Rooms, CR, HouseType, Feedback
from .serializers import UserHousewiseSerializer, ProjectSerializer, FeedbackSerializer
import logging
from .utils import generate_token  # Import the utility function


@api_view(['POST'])
@authentication_classes([])  # Allow unauthenticated access to this view
@permission_classes([AllowAny])
def login_user(request):
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    # Validate input
    if not username_or_email or not password:
        return Response(
            {"error": "Please provide both username/email and password."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        # Retrieve user by username or email
        user = UserHousewise.objects.filter(
            Q(username=username_or_email) | Q(email=username_or_email)
        ).first()

        if user and user.check_password(password):  # Verify password
            # Check user type
            if user.user_type.user_type.lower() == 'user':  # Case-insensitive check
                user.last_login = timezone.now()
                user.save()

                # Create login session
                login_session = LoginSession.objects.create(user=user, login_time=user.last_login)
                request.session['login_session_id'] = login_session.loginsession_id  # Save session ID
                
                # Generate JWT tokens
                tokens = generate_token(user)  # Use utility function for token generation

                return Response({
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                        "email": user.email,
                        "birthdate": user.birthdate,
                    },
                    "token": tokens['access'],  # Return access token
                    "refresh": tokens['refresh'],  # Optionally return refresh token
                }, status=status.HTTP_200_OK)
            
            return Response(
                {"error": "You do not have permission to access this area."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            return Response(
                {"error": "Invalid username or password."}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

User = get_user_model()
logger = logging.getLogger(__name__)

@csrf_exempt
def create_project(request):
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Extract and validate the token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization header missing or invalid'}, status=403)

        token = auth_header.split(' ')[1]  # Extract the token
        try:
            # Decode the token
            decoded_token = AccessToken(token)
            logger.info(f"Decoded token: {decoded_token}")
            user_id = decoded_token['user_id']
            user = User.objects.get(id=user_id)
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            return JsonResponse({'error': f'Invalid token: {str(e)}'}, status=403)

        # Check if the user is of type 'user'
        if user.user_type.user_type.lower() != 'user':
            return JsonResponse({'error': 'You do not have permission to create a project.'}, status=403)

        # Proceed with the rest of your logic (unchanged)
        data = json.loads(request.body)

        # Fetch HouseType
        house_type = HouseType.objects.get(description=data.get('houseType').lower())

        # Create Project
        project = Project.objects.create(
            user=user,
            project_name=data.get('projectName', 'Unnamed Project'),
            length=data.get('houseLength'),
            width=data.get('houseWidth'),
            height=data.get('houseWallHeight'),
            house_type=house_type
        )

        # Add Roof
        Roof.objects.create(
            project=project,
            roof_type=data.get('roofType'),
            trusses=data.get('trussType')
        )

        # Add CR if `crCount` is 1
        if data.get('crCount') == 1:
            CR.objects.create(
                project=project,
                cr_length=data.get('CrLengthValue'),
                cr_width=data.get('CrWidthValue')
            )

        # Add Rooms
        room_count = data.get('roomCount', 0)
        if room_count >= 1:
            Rooms.objects.create(
                project=project,
                room_number='1',
                room_length=data.get('room1Length'),
                room_width=data.get('room1Width'),
                active_button=data.get('activeButtonRoom1')
            )

        if room_count == 2:
            Rooms.objects.create(
                project=project,
                room_number='2',
                room_length=data.get('room2Length'),
                room_width=data.get('room2Width'),
                active_button=data.get('activeButtonRoom2')
            )

        # Update project counts
        project.update_counts()

        return JsonResponse({'message': 'Project created successfully', 'project_id': project.project_id}, status=201)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=400)

@csrf_exempt
def get_material_prices(request):
    if request.method == "GET":
        material_prices = {}
        materials = Materials.objects.all()

        for material in materials:
            prices = material.prices.all()
            if prices.exists():
                highest_price = prices.order_by('-amount').first().amount
                lowest_price = prices.order_by('amount').first().amount
                material_prices[material.materials_id] = {
                    "highest": highest_price,
                    "lowest": lowest_price
                }

        return JsonResponse(material_prices, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id):
    try:
        # Ensure the project exists and belongs to the authenticated user
        project = Project.objects.get(pk=project_id, user=request.user)
        project_name = project.project_name
        project.delete()

        return Response({'message': f'Project "{project_name}" deleted successfully.'}, status=status.HTTP_200_OK)

    except Project.DoesNotExist:
        return Response({'error': 'Project not found or you do not have permission to delete it.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def save_feedback(request, project_id):
    """
    Create or update feedback for a specific project.
    """
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    feedback, created = Feedback.objects.update_or_create(
        project=project,
        defaults={
            "rating": data.get("rating"),
            "feedback_description": data.get("feedback_description"),
        },
    )
    serializer = FeedbackSerializer(feedback)
    return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

@api_view(['GET'])
def get_feedback(request, project_id):
    try:
        feedback = Feedback.objects.filter(project__project_id=project_id).first()
        if feedback:
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data, status=200)
        # Return an empty object with a success response when no feedback exists
        return Response({}, status=200)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)

from datetime import datetime

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    try:
        print(f"Request Headers: {request.headers}")
        print(f"Request User: {request.user}")

        user = request.user
        data = request.data

        if user.user_type.user_type != 'user':
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        # Update fields
        user.name = data.get('name', user.name)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        # Handle birthdate
        if 'birthdate' in data and data['birthdate']:
            try:
                user.birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Expected YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Raw birthdate from request: {data.get('birthdate')}")
        print(f"Parsed birthdate: {user.birthdate}")

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

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_username(request):
    username = request.data.get('username', '').strip().lower()

    if not username:
        return JsonResponse({'exists': False, 'message': 'Username is required.'}, status=400)

    user_exists = UserHousewise.objects.filter(username=username).exists()

    return JsonResponse(
        {'exists': user_exists, 'message': 'Username exists.' if user_exists else 'Username does not exist.'},
        status=200 if user_exists else 404
    )

@csrf_exempt
@permission_classes([AllowAny])
def send_reset_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))  # Parse JSON body
            username = data.get('username', '').strip().lower()
        except (json.JSONDecodeError, AttributeError):
            return JsonResponse({'success': False, 'error': 'Invalid request payload'}, status=400)

        try:
            user = UserHousewise.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Username not found'}, status=404)

        email = user.email
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Expiry time
        expiry_time = datetime.now() + timedelta(minutes=10)
        request.session['verification_code_expiry'] = expiry_time.isoformat()

        subject = 'Your Password Reset Code'
        from_email = 'housewise.app@gmail.com'
        to_email = [email]
        text_content = (f'Hi {user.name},\n\n'
                        f'You requested to reset your password. Here is your verification code:\n\n'
                        f'{verification_code}\n\n'
                        f'This code is valid for 10 minutes.\n\n'
                        f'Do not Give your code to anyone else.')
        html_content = (f'<p>Hi {user.name},</p>'
                        f'<p>You requested to reset your password. Here is your verification code:</p>'
                        f'<p><strong>{verification_code}</strong></p>'
                        f'<p>This code is valid for 10 minutes.</p>'
                        f'<p>Do not Give your code to anyone else.</p>')

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
def resetverify_code(request):
    if request.method == 'POST':
        # Retrieve the 'code' from POST data
        code = request.POST.get('code')

        if not code:
            return JsonResponse({'success': False, 'error': 'Code is required'}, status=400)

        # Retrieve the stored verification code from the session
        resetstored_code = request.session.get('verification_code')

        if not resetstored_code:
            return JsonResponse({'success': False, 'error': 'No verification code found'}, status=400)

        if code == resetstored_code:
            return JsonResponse({'success': True, 'message': 'Verification successful'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid verification code'}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        new_password = data.get('new_password')
        verification_code = data.get('verification_code')

        if not username or not new_password or not verification_code:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

        # Fetch the user and verify the code
        try:
            user = UserHousewise.objects.get(username=username)
        except UserHousewise.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

        # Assuming you stored the verification code and expiry in the session or database
        resetstored_code = request.session.get('verification_code')
        expiry_time = request.session.get('verification_code_expiry')

        if not resetstored_code or resetstored_code != verification_code:
            return JsonResponse({'success': False, 'error': 'Invalid verification code'}, status=400)

        if expiry_time and datetime.fromisoformat(expiry_time) < datetime.now():
            return JsonResponse({'success': False, 'error': 'Verification code has expired'}, status=400)

        # Update the user's password
        user.password = make_password(new_password)
        user.save()

        # Clear the session values after use
        request.session.pop('verification_code', None)
        request.session.pop('verification_code_expiry', None)

        return JsonResponse({'success': True, 'message': 'Password reset successful'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

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

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_account(request):
    data = request.data

    # Parse and validate the birthdate field
    if 'birthdate' in data and data['birthdate']:
        try:
            data['birthdate'] = datetime.strptime(data['birthdate'], '%Y-%m-%d').date()
        except ValueError:
            return Response({"success": False, "message": "Invalid date format. Expected YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    # Use the serializer for validation and saving
    serializer = UserHousewiseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True, "message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    
    return Response({"success": False, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def published_projects_view(request):
    try:
        # Query for all published projects ordered by creation date (newest to oldest)
        published_projects = Project.objects.filter(is_published=True).order_by('-date_time_created')
        # Serialize the data
        serializer = ProjectSerializer(published_projects, many=True, context={'request': request})
        # Return the serialized data as JSON
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def user_owned_projects_view(request):
    try:
        # Filter projects owned by the logged-in user, ordered by most recent
        user_owned_projects = Project.objects.filter(user=request.user).order_by('-date_time_created')
        
        # Serialize the data
        serializer = ProjectSerializer(user_owned_projects, many=True, context={'request': request})
        
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_projects_view(request):
    try:
        # Fetch liked projects for the logged-in user, ordered by most recent
        user = request.user
        liked_projects = Project.objects.filter(project_likes__user=user).order_by('-date_time_created')
        
        # Serialize the data
        serializer = ProjectSerializer(liked_projects, many=True, context={'request': request})
        
        return Response(serializer.data, status=200)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def toggle_project_publish_status(request, pk):
    try:
        # Fetch the project owned by the user and matching the primary key
        project = Project.objects.get(pk=pk, user=request.user)
    except Project.DoesNotExist:
        return Response({"error": "Project not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

    # Toggle the is_published status
    is_published = request.data.get('is_published', None)
    if is_published is not None:
        project.is_published = is_published
        project.save()
        return Response({"success": True, "is_published": project.is_published}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def toggle_like(request, project_id):
    user = request.user  # Assumes user is authenticated
    project = get_object_or_404(Project, project_id=project_id)

    # Check if the user has already liked the project
    existing_like = ProjectLike.objects.filter(user=user, project=project).first()
    if existing_like:
        # Unlike
        existing_like.delete()
    else:
        # Like
        ProjectLike.objects.create(user=user, project=project)

    # Update likes_count and save the project
    project.likes_count = ProjectLike.objects.filter(project=project).count()
    project.save()

    liked = not bool(existing_like)  # True if liked, False if unliked
    return Response({"success": True, "liked": liked, "likes_count": project.likes_count})


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
@authentication_classes([JWTAuthentication])  # Ensure the request is authenticated
@permission_classes([IsAuthenticated])
def session_status(request):
    try:
        user = request.user
        login_session_id = request.session.get('login_session_id')

        if not login_session_id:
            return Response({'valid': False, 'error': 'No active session found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            login_session = LoginSession.objects.get(loginsession_id=login_session_id, user=user)
            
            # Check if the session is still active
            if login_session.logout_time:
                return Response({'valid': False, 'error': 'Session has ended'}, status=status.HTTP_401_UNAUTHORIZED)

            # Optionally, you can add a check for session expiry
            session_duration = timezone.now() - login_session.login_time
            if session_duration.total_seconds() > 604800:  # 7 days
                login_session.logout_time = timezone.now()
                login_session.save()
                return Response({'valid': False, 'error': 'Session has expired'}, status=status.HTTP_401_UNAUTHORIZED)

            # Return valid session status
            user_data = UserHousewiseSerializer(user).data
            return Response({'valid': True, 'user': user_data}, status=status.HTTP_200_OK)

        except LoginSession.DoesNotExist:
            return Response({'valid': False, 'error': 'Login session not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'valid': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        # Retrieve the refresh token from the request data
        refresh_token = request.data.get('refresh_token')  # Correct key: `refresh_token`
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the token

        # Handle login session updates
        login_session_id = request.session.get('login_session_id')
        if login_session_id:
            try:
                login_session = LoginSession.objects.get(loginsession_id=login_session_id)
                login_session.logout_time = timezone.now()
                login_session.login_duration = login_session.logout_time - login_session.login_time
                login_session.save()
            except LoginSession.DoesNotExist:
                return Response({'error': 'Login session not found'}, status=status.HTTP_404_NOT_FOUND)

        # Log out the user and clear the session
        logout(request)
        request.session.flush()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

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
    user_type_user = UserType.objects.get(user_type='user')
    users = UserHousewise.objects.filter(user_type=user_type_user).order_by('-created_at')

    selected_user = None
    login_sessions = []
    feedbacks = []
    
    if 'selected_id' in request.GET:
        selected_id = request.GET.get('selected_id')
        selected_user = UserHousewise.objects.get(id=selected_id)
        login_sessions = selected_user.login_sessions.all().order_by('-login_time')

        # Fetch feedbacks for the selected user
        feedbacks = Feedback.objects.filter(project__user=selected_user).order_by('-feedback_datetime')

        # Format login sessions for frontend
        formatted_sessions = [
            {
                "login_time": session.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                "logout_time": session.logout_time.strftime('%Y-%m-%d %H:%M:%S') if session.logout_time else "Active",
                "duration": str(session.login_duration) if session.logout_time else "Active",
                "is_active": session.logout_time is None
            }
            for session in login_sessions
        ]

        # Format feedbacks for frontend
        formatted_feedbacks = [
            {
                "project_name": feedback.project.project_name if feedback.project else "No Project",
                "project_created": feedback.project.date_time_created.strftime('%Y-%m-%d %H:%M:%S') if feedback.project else "N/A",
                "rating": feedback.rating,
                "description": feedback.feedback_description,
                "feedback_datetime": feedback.feedback_datetime.strftime('%Y-%m-%d %H:%M:%S')
            }
            for feedback in feedbacks
        ]
    else:
        formatted_sessions = []
        formatted_feedbacks = []

    return render(request, 'housewise/user.html', {
        'users': users,
        'login_sessions': formatted_sessions,
        'feedbacks': formatted_feedbacks,
        'selected_user': selected_user
    })

def dashboard_data_api(request):
    try:
        user_type_user = UserType.objects.get(user_type='user')

        # Total users of type 'User'
        total_users = UserHousewise.objects.filter(user_type=user_type_user).count()

        # Total users logged in
        total_users_logged_in = LoginSession.objects.filter(
            user__user_type=user_type_user,
            logout_time__isnull=False
        ).values('user').distinct().count()

        # Calculate users not logged in
        total_users_not_logged_in = total_users - total_users_logged_in

        # Total feedbacks received
        total_feedbacks = Feedback.objects.count()

        data = {
            'total_users': total_users,
            'total_users_logged_in': total_users_logged_in,
            'total_users_not_logged_in': total_users_not_logged_in,
            'total_feedbacks': total_feedbacks,
        }
    except UserType.DoesNotExist:
        data = {
            'total_users': 0,
            'total_users_logged_in': 0,
            'total_users_not_logged_in': 0,
            'total_feedbacks': 0,
            'error': "UserType 'User' does not exist",
        }

    return JsonResponse(data)




@login_required(login_url='/housewise/')
def user_login_sessions(request):
    if 'user_id' not in request.GET:
        return JsonResponse({"error": "No user_id provided"}, status=400)

    user_id = request.GET['user_id']
    try:
        user = UserHousewise.objects.get(id=user_id)
        sessions = user.login_sessions.all().order_by('-login_time')

        # Format the data for JSON response
        session_data = [
            {
                "login_time": session.login_time.strftime('%Y-%m-%d %H:%M:%S'),
                "logout_time": session.logout_time.strftime('%Y-%m-%d %H:%M:%S') if session.logout_time else "Active",
                "duration": str(session.login_duration) if session.logout_time else "Active",
                "is_active": session.logout_time is None
            }
            for session in sessions
        ]

        return JsonResponse({"login_sessions": session_data}, status=200)

    except UserHousewise.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    

@login_required(login_url='/housewise/')
def user_feedbacks(request):
    user_id = request.GET.get('user_id')
    if user_id:
        feedbacks = Feedback.objects.filter(project__user_id=user_id).order_by('-feedback_datetime')
        feedback_data = [
            {
                "project_name": feedback.project.project_name if feedback.project else "No Project",
                "project_created": feedback.project.date_time_created.strftime('%Y-%m-%d %H:%M:%S') if feedback.project else "N/A",
                "rating": feedback.rating,
                "description": feedback.feedback_description,
                "feedback_datetime": feedback.feedback_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for feedback in feedbacks
        ]
        return JsonResponse({"feedbacks": feedback_data}, safe=False)
    return JsonResponse({"feedbacks": []})

def graph_data_api(request):
    # Total projects created by all users
    total_projects = Project.objects.count()

    # Total projects rated (projects with at least one feedback)
    total_projects_rated = Project.objects.filter(feedbacks__isnull=False).distinct().count()

    # Calculate the average rating
    feedback_stats = Feedback.objects.aggregate(avg_rating=Avg('rating'))
    average_rating = feedback_stats.get('avg_rating', 0)

    # Add a print statement to debug
    print("Average Rating Calculated:", average_rating)

    # Format the average rating for display
    formatted_average_rating = f"{round(average_rating, 2)}/5" if average_rating else "0.00/5"

    data = {
        'total_projects': total_projects,
        'total_projects_rated': total_projects_rated,
        'average_rating': formatted_average_rating,
    }

    return JsonResponse(data)



def feedback_list_api(request):
    feedbacks = Feedback.objects.select_related('project', 'project__user').all()
    feedback_data = [
        {
            "feedback_id": feedback.feedback_id,
            "project_name": feedback.project.project_name if feedback.project else "N/A",
            "rating": feedback.rating,
            "feedback_datetime": feedback.feedback_datetime,
            "description": feedback.feedback_description,
            "user": feedback.project.user.username if feedback.project else "Unknown User",
        }
        for feedback in feedbacks
    ]
    return JsonResponse({"feedbacks": feedback_data})


@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = get_object_or_404(UserHousewise, id=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'message': 'Error deleting user.', 'error': str(e)}, status=500)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)



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
    


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
import json

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def register(request):
    # Handle GET request - show the form
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'users/register.html', {'form': form})
    
    # Handle POST request
    elif request.method == 'POST':
        # Check if it's a JSON request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                email = data.get('email', '')
                
                if not username or not password:
                    return Response({
                        'error': 'Username and password are required'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if User.objects.filter(username=username).exists():
                    return Response({
                        'error': 'Username already exists'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }, status=status.HTTP_201_CREATED)
                
            except json.JSONDecodeError:
                return Response({
                    'error': 'Invalid JSON'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Handle traditional form submission
        else:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                refresh = RefreshToken.for_user(user)
                # Store tokens in session for traditional auth
                request.session['access_token'] = str(refresh.access_token)
                request.session['refresh_token'] = str(refresh)
                auth_login(request, user)
                return redirect('tasks:tasks')
            else:
                return render(request, 'users/register.html', {'form': form})

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def login(request):
    # Handle GET request - show the form
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})
    
    # Handle POST request
    elif request.method == 'POST':
        # Check if it's a JSON request
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                
                if not username or not password:
                    return Response({
                        'error': 'Username and password are required'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = authenticate(username=username, password=password)
                
                if user is None:
                    return Response({
                        'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)
                
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }, status=status.HTTP_200_OK)
                
            except json.JSONDecodeError:
                return Response({
                    'error': 'Invalid JSON'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Handle traditional form submission
        else:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                auth_login(request, user)
                # Generate JWT tokens for session
                refresh = RefreshToken.for_user(user)
                request.session['access_token'] = str(refresh.access_token)
                request.session['refresh_token'] = str(refresh)
                
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                else:
                    return redirect("tasks:tasks")
            else:
                return render(request, 'users/login.html', {'form': form})

@api_view(['POST'])
def logout(request):
    if request.content_type == 'application/json':
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Handle traditional logout
        auth_logout(request)
        # Clear JWT tokens from session
        if 'access_token' in request.session:
            del request.session['access_token']
        if 'refresh_token' in request.session:
            del request.session['refresh_token']
        return redirect("home")
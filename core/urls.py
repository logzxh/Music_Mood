from django.urls import path
from core.views.mood import MoodDetectView
from core.views.recipe import GenerateRecipe, RecommendRecipe, SelectBudget, GroceryView
from core.views.audio import VoiceGuide
from core.views.navigation import StepNavigation
from core.views.user import UserProfileView
from rest_framework.authtoken.views import obtain_auth_token  # <-- Add this import

urlpatterns = [
    path('mood/', MoodDetectView.as_view(), name='mood-detect'),
    path('generate-recipe/', GenerateRecipe.as_view(), name='generate-recipe'),
    path('recommend-recipe/', RecommendRecipe.as_view(), name='recommend-recipe'),
    path('select-budget/', SelectBudget.as_view(), name='select-budget'),
    path('grocery/<int:recipe_id>/', GroceryView.as_view(), name='grocery'),
    path('voice-guide/', VoiceGuide.as_view(), name='voice-guide'),
    path('navigate/', StepNavigation.as_view(), name='navigate'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user-profile-detail'),  # detail route for GET/PUT/PATCH/DELETE
    path('user/', UserProfileView.as_view(), name='user-profile-list-create'),            # list/create route for GET (list) and POST

    # Token authentication endpoint for frontend login
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
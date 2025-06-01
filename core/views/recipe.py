from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist, ValidationError as MongoValidationError
from core.models import Recipe, UserProfile
from core.utils.grocery_calculator import calculate_groceries
from core.ai.mood_detector import detect_facial_mood
from core.serializers import RecipeSerializer

class GenerateRecipe(APIView):
    def post(self, request):
        dish = request.data.get("dish")
        user = request.user

        mood = detect_facial_mood()
        taste_profile = "spicy" if mood == "happy" else "mild"

        try:
            user_profile = UserProfile.objects.get(username=user.username)
        except DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        recipes = Recipe.objects(name__icontains=dish, taste=taste_profile)
        budget_tiers = {
            "low": recipes.filter(budget="low").first(),
            "medium": recipes.filter(budget="medium").first(),
            "high": recipes.filter(budget="high").first(),
        }

        grocery_lists = {
            tier: calculate_groceries(recipe) for tier, recipe in budget_tiers.items() if recipe
        }

        return Response({
            "mood": mood,
            "taste_profile": taste_profile,
            "recipes": {tier: recipe.name if recipe else None for tier, recipe in budget_tiers.items()},
            "groceries": grocery_lists
        })

class RecommendRecipe(APIView):
    def post(self, request):
        dish = request.data.get("dish")
        mood = detect_facial_mood()
        taste = "spicy" if mood == "happy" else "mild"
        recipes = Recipe.objects(name__icontains=dish, taste=taste)
        return Response({"recipes": [r.name for r in recipes]})

class SelectBudget(APIView):
    def post(self, request):
        tier = request.data.get("tier")
        recipe = Recipe.objects(budget=tier).first()
        if not recipe:
            return Response({"error": "Recipe not found for this budget tier."}, status=status.HTTP_404_NOT_FOUND)
        serializer = RecipeSerializer(recipe)
        return Response({"recipe": serializer.data})

class GroceryView(APIView):
    def get(self, request, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except (DoesNotExist, MongoValidationError):
            return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)
        groceries = calculate_groceries(recipe)
        return Response(groceries)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.ai.mood_detector import detect_facial_mood

class StepNavigation(APIView):
    def post(self, request):
        action = request.data.get("action")  # "back", "change_mood"
        current_step = request.data.get("step", 0)
        try:
            current_step = int(current_step)
        except (TypeError, ValueError):
            current_step = 0

        if action == "back":
            return Response({"step": max(current_step - 1, 0)})
        elif action == "change_mood":
            try:
                new_mood = detect_facial_mood()
                return Response({"mood": new_mood})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"message": "no action performed"}, status=status.HTTP_400_BAD_REQUEST)
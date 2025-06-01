from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.ai.mood_detector import detect_facial_mood

class MoodDetectView(APIView):
    def get(self, request):
        try:
            mood = detect_facial_mood()
            return Response({"mood": mood})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
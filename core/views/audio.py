from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.utils.voice_assistant import speak
from core.utils.beep_notifier import beep

class VoiceGuide(APIView):
    def post(self, request):
        step = request.data.get("step")
        if not step:
            return Response(
                {"error": "No instruction provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        speak(step)
        beep()
        return Response(
            {"message": "Instruction spoken."},
            status=status.HTTP_200_OK
        )
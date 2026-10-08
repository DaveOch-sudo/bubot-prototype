from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .services.rasa_client import send_message


def health(request):
    return JsonResponse({
        "status": "ok",
        "service": "bubot-backend",
    })


@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405,
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON."},
            status=400,
        )

    message = data.get("message")
    sender = data.get("sender", "anonymous")

    if not message:
        return JsonResponse(
            {"error": "Message is required."},
            status=400,
        )

    try:
        rasa_response = send_message(sender, message)

        return JsonResponse({
            "sender": sender,
            "responses": rasa_response,
        })

    except Exception as exc:
        return JsonResponse(
            {"error": str(exc)},
            status=502,
        )
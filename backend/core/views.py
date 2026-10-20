from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from ai.orchestration.orchestrator import ChatOrchestrator

orchestrator = ChatOrchestrator()

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
        answer = orchestrator.answer(message)
        return JsonResponse({
            "sender": sender,
            "response": answer,
        })

    except Exception as exc:
        return JsonResponse(
            {"error": str(exc)},
            status=502,
        )
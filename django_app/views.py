import socket
import psycopg2
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from .models import Note
import json


def api_info(request):
    hostname = socket.gethostname()
    now = datetime.utcnow().isoformat() + "Z"

    db_status = "ok"
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
            connect_timeout=2,
        )
        conn.close()
    except Exception as e:
        db_status = f"error: {e}"

    return JsonResponse({
        "service": "django-app",
        "hostname": hostname,
        "time": now,
        "database": {
            "name": settings.DATABASES['default']['NAME'],
            "user": settings.DATABASES['default']['USER'],
            "host": settings.DATABASES['default']['HOST'],
            "port": settings.DATABASES['default']['PORT'],
            "status": db_status
        }
    })


def health(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class NotesView(View):
    def get(self, request):
        notes = Note.objects.all().order_by('-created_at')[:10]
        data = [
            {"id": n.id, "text": n.text, "created_at": n.created_at.isoformat()}
            for n in notes
        ]
        return JsonResponse({"notes": data})

    def post(self, request):
        try:
            body = json.loads(request.body)
            text = body.get("text")
            if not text:
                return JsonResponse({"error": "text field required"}, status=400)
            note = Note.objects.create(text=text)
            return JsonResponse({
                "id": note.id,
                "text": note.text,
                "created_at": note.created_at.isoformat()
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid JSON"}, status=400)

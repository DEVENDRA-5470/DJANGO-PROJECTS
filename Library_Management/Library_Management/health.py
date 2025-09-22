from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
import os

def liveness(request):
    """
    Basic check: Is Django alive?
    Always returns 200 if the process is running.
    """
    return JsonResponse({"status": "alive"})


def readiness(request):
    """
    Deep check: Can Django talk to DB and write to media dir?
    Returns 200 if ready, 503 if not.
    """
    # 1. Check database
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return JsonResponse({"status": "db down"}, status=503)

    # 2. Check media folder write access (optional but recommended)
    media_root = os.getenv("MEDIA_ROOT", "media")
    if not os.access(media_root, os.W_OK):
        return JsonResponse({"status": "media not writable"}, status=503)

    return JsonResponse({"status": "ready"})

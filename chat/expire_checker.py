from .models import Message
from django.utils import timezone
import datetime
import time
from background_task import background


@background(schedule=60)
def expire_checker(ttl):
    # while True:
    expire_time = timezone.now()-datetime.timedelta(seconds=ttl)
    msgs= Message.objects.filter(created_at__lte=expire_time)
    msgs.delete()
        # time.sleep(interval)


# expire_checker(600,10)

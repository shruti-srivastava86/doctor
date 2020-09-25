import os
import uuid


def alert_video(instance, filename):
    extension = os.path.splitext(str(filename))[1]
    filename = str(uuid.uuid4()) + extension
    return 'alert_videos/' + filename

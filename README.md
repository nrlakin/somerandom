# somerandom
Web application that allows anyone to anonymously post to a common Twitter account. This is an experiment to see what people post they're really anonymous--sort of a dumb-simple Whisper. For fun, I'm using Celery to follow-back anyone who follows _some_random_ on Twitter.

Tech details:
-Python/Flask backend
-Celery/Redis for task scheduling
-Configured for Heroku hosting; will move to something more scaleable if anyone actually uses it.

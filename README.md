# somerandom
Web application that allows anyone to anonymously post to a common Twitter account. This is an experiment to see what people post they're really anonymous--sort of a dumb-simple Whisper. For fun, I'm using Celery to follow-back anyone who follows <a href="http://twitter.com/_some_random_">@_some_random_</a> on Twitter.

Tech details:

-Python/Flask backend

-Celery/Redis for task scheduling

-Configured for Heroku hosting; will move to something more scaleable if anyone actually uses it.

To Do's:

-More sophisticated task scheduling to get the most out of Twitter's rate limits. Would like to "spread out" posts to stay under the rate limit instead of getting errors.

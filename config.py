# Deploy suggestion:
# Gunicorn is the best, just call
# gunicorn -w 4 -b 127.0.0.1:5000 server:app -D

config = {
  "intropage": {
    "url": "https://github.com/houaa/intropage",
    "path": "/home/hao/intropage",
    "secret": "1234567890"
  }
}

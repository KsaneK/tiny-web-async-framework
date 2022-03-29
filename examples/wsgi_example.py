from tinyweb import TinyWeb

app = TinyWeb("localhost", 6820)


@app.route("/hello_world", methods=["GET"])
def hello_world(request):
    return "Hello from WSGI!"

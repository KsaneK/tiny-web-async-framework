from tinyweb import TinyWeb

app = TinyWeb("localhost", 6820)


@app.route("/hello_world", methods=["GET"])
def hello_world(request):
    return "<h1>Hello World!</h1>"


@app.route("/test/endpoint", methods=["GET"])
def test_endpoint(request):
    return "Test status 201", 201


app.run()

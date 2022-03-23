from tinyweb import TinyWeb
from tinyweb.templates import render

app = TinyWeb("localhost", 6820)


@app.route("/hello_world", methods=["GET"])
def hello_world(request):
    return render("templates/hello_world_template.html")


@app.route("/test/endpoint", methods=["GET"])
def test_endpoint(request):
    return "Test status 201", 201


@app.route("/test/500", methods=["GET"])
def test_endpoint(request):
    print("No return statement. I'm going to fail!")


app.run()

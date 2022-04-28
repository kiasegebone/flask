from io import StringIO

import flask


def test_suppressed_exception_logging():
    class SuppressedFlask(flask.Flask):
        def log_exception(self, exc_info):
            pass

    out = StringIO()
    app = SuppressedFlask(__name__)

    @app.route("/")
    def index():
        # OpenRefactory Warning: Raising 'Exception' and 'BaseException' directly will have a negative impact on any code trying to catch these exceptions.
        # Raise a more specific built-in exception or, create a custom one.
        raise Exception("test")

    rv = app.test_client().get("/", errors_stream=out)
    assert rv.status_code == 500
    assert b"Internal Server Error" in rv.data
    assert not out.getvalue()

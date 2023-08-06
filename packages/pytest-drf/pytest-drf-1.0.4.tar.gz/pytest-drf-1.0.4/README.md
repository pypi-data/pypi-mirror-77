# pytest-drf

[![PyPI version](https://badge.fury.io/py/pytest-drf.svg)](https://badge.fury.io/py/pytest-drf)
[![Build Status](https://travis-ci.org/theY4Kman/pytest-drf.svg?branch=master)](https://travis-ci.org/theY4Kman/pytest-drf)

pytest-drf is a [pytest](http://pytest.org) plugin for testing your [Django REST Framework](https://www.django-rest-framework.org/) APIs.

pytest-drf aims to do away with clunky setup code and boilerplate for DRF testing, replacing it with declarative scaffolds that encourage small, easy-to-follow tests with single responsibilities.

This is accomplished by performing one request per test, and providing the response as a fixture. All configuration of the request — the URL, the query params, the HTTP method, the POST data, etc — is also done through fixtures. This leaves the test methods containing only assertions about the response or the state of the app after the request succeeds.

For example, let's consider a public API endpoint that responds with the JSON string "Hello, World!" and a 200 status code to a GET request. Such an endpoint might be written like so

```python
# example/views.py

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view()
@permission_classes([permissions.AllowAny])
def hello_world(request):
    return Response('Hello, World!')
```

Let's route it to `/hello`, and give it a name, so we can easily generate URLs for it.

```python
# example/urls.py

from django.urls import path

from example import views

urlpatterns = [
    path('hello', views.hello_world, name='hello-world'),
]
```

With pytest-drf, we'd verify the behavior of our endpoint with something like this

```python
# tests/test_hello.py

class TestHelloWorld(
    APIViewTest,
    UsesGetMethod,
    Returns200,
):
    @pytest.fixture
    def url(self):
        return reverse('hello-world')

    def test_returns_hello_world(self, json):
        expected = 'Hello, World!'
        actual = json
        assert expected == actual
```

When we run pytest, we see two tests run

```
$ py.test

tests/test_hello.py::TestHelloWorld::test_it_returns_200 <- pytest_drf/status.py PASSED [ 50%]
tests/test_hello.py::TestHelloWorld::test_returns_hello_world PASSED                    [100%]
```

from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_swagger import renderers
from rest_framework.schemas import SchemaGenerator


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(title='Tempt API')
        schema = generator.get_schema(request=request)

        return Response(schema)


def home(request):
    return HttpResponse("Hello, World.")

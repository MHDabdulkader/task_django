from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Task
from .serializer import TaskSerializer


class CustomResponse:
    """Custom response api wrapper"""

    @staticmethod
    def success(data, message="Success", status_code=200):
        return Response(
            {"status": status_code, "message": message, "data": data},
            status=status_code,
        )

    @staticmethod
    def error(data=None, message="Error", status_code=400):
        return Response(
            {"status": status_code, "message": message, "data": data or {}},
            status=status_code,
        )


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  # pyright: ignore[reportAttributeAccessIssue]
    serializer_class = TaskSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "due_date"]

    # List
    def list(self, request: Request) -> Response:
      """GET /api/tasks/"""
      queryset = self.get_queryset()
      serializer = self.serializer_class(queryset, many=True)
      return CustomResponse.success(
        data = serializer.data,
        message="Tasks retrieved",
        status_code=200
      )
      
    # create
    def create(self, request: Request) -> Response:
      """POST /api/tasks/"""
      serializer = self.get_serializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return CustomResponse.success(
          data= serializer.data,
          message="Tasks created!",
          status_code=201
        )
      return CustomResponse.error(
        data=serializer.errors,
        message="Task create failed!",
        status_code=400
      )


    # Status updated
    @action(detail=False, methods=["get"])
    def by_status(self, request):
        """GET /tasks/by_status/?status=done"""
        status_filter = request.query_params.get("status")

        if status_filter:
            tasks = Task.objects.filter(  # pyright: ignore[reportAttributeAccessIssue]
                status=status_filter
            )  # pyright: ignore[reportAttributeAccessIssue]
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data)

        return Response(
            {"error": "status parameter required!"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Marks as complete
    @action(detail=True, methods=["patch"])
    def mark_as_completed(self, request):
        f"""PATCH /tasks/{id}/mark_complete/"""
        task = self.get_object()
        task.status = "done"
        task.save()
        serializer = self.get_serializer(task)

        return Response(serializer.data)

import json
import pickle
import numpy
from rest_framework import status
from app.tasks import run_global_controller
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_celery_results.models import TaskResult


@api_view(['POST'])
def run_gc(request):
    # p_forecast = request.data.get('pForecast', None)
    # r_forecast = request.data.get('rForecast', None)
    q_zero = request.data.get('q0', 0)
    #
    # if p_forecast is None:
    #     return Response({'result': 'Missing the pForecast required param'}, status=status.HTTP_400_BAD_REQUEST)
    #
    # if r_forecast is None:
    #     return Response({'result': 'Missing the rForecast required param'}, status=status.HTTP_400_BAD_REQUEST)
    #
    # if q_zero is None:
    #     return Response({'result': 'Missing the q0 required param'}, status=status.HTTP_400_BAD_REQUEST)

    # t = run_global_controller.delay(p_forecast, r_forecast, q_zero)
    t = run_global_controller.delay(None, None, q_zero)
    return Response({'task_id': t.id}, status=status.HTTP_200_OK)


@api_view(['GET'])
def gc_results(request):
    t_id = request.query_params.get('task_id', -999)
    if t_id == -999:
        return Response({'result': 'Please supply a task id to lookup'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        task = TaskResult.objects.get(task_id=t_id)
    except TaskResult.DoesNotExist:
        return Response({'result': 'The given id doesn\'t exist. The task may have not finished or the id is invalid.'},
                        status=status.HTTP_204_NO_CONTENT)
    return Response({'result': task.result}, status=status.HTTP_200_OK)

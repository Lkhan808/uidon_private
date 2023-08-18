from rest_framework.exceptions import ValidationError

from applications.profiles.models import ExecutorProfile, CustomerProfile


def get_all_executors():
    return ExecutorProfile.objects.all()


def get_executor(pk: int):
    try:
        return ExecutorProfile.objects.get(pk=pk)
    except ExecutorProfile.DoesNotExist:
        raise ValidationError("Executor not Found")


def create_executor(data):
    skills = data.pop("skills", [])
    executor = ExecutorProfile.objects.create(**data)
    executor.skills.set(skills)
    executor.save()
    return executor

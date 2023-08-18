from applications.qualifications.models import Skill


def get_all_skills():
    return Skill.objects.all()
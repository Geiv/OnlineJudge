from django.db import models
from rest_framework.exceptions import ValidationError

from school.models import School
from utils.models import JSONField
from django.contrib.postgres.fields import ArrayField
from account.models import User
from contest.models import Contest
from utils.models import RichTextField
from utils.constants import Choices


class ProblemTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "problem_tag"


class ProblemRuleType(Choices):
    ACM = "ACM"
    OI = "OI"


class ProblemDifficulty(object):
    High = "High"
    Mid = "Mid"
    Low = "Low"


class ProblemIOMode(Choices):
    standard = "Standard IO"
    file = "File IO"


def _default_io_mode():
    return {"io_mode": ProblemIOMode.standard, "input": "input.txt", "output": "output.txt"}


class Problem(models.Model):
    # display ID
    _id = models.TextField(db_index=True)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    # for contest problem
    is_public = models.BooleanField(default=False)
    title = models.TextField()
    # HTML
    description = RichTextField()
    input_description = RichTextField()
    output_description = RichTextField()
    # [{input: "test", output: "123"}, {input: "test123", output: "456"}]
    samples = JSONField()
    test_case_id = models.TextField()
    # [{"input_name": "1.in", "output_name": "1.out", "score": 0}]
    test_case_score = JSONField()
    hint = RichTextField(null=True)
    languages = JSONField()
    template = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)
    # we can not use auto_now here
    last_update_time = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # ms
    time_limit = models.IntegerField()
    # MB
    memory_limit = models.IntegerField()
    # io mode
    io_mode = JSONField(default=_default_io_mode)
    # special judge related
    spj = models.BooleanField(default=False)
    spj_language = models.TextField(null=True)
    spj_code = models.TextField(null=True)
    spj_version = models.TextField(null=True)
    spj_compile_ok = models.BooleanField(default=False)
    rule_type = models.TextField()
    visible = models.BooleanField(default=True)
    difficulty = models.TextField()
    tags = models.ManyToManyField(ProblemTag)
    source = models.TextField(null=True)
    # for OI mode
    total_score = models.IntegerField(default=0)
    submission_number = models.BigIntegerField(default=0)
    accepted_number = models.BigIntegerField(default=0)
    # {JudgeStatus.ACCEPTED: 3, JudgeStaus.WRONG_ANSWER: 11}, the number means count
    statistic_info = JSONField(default=dict)
    share_submission = models.BooleanField(default=False)

    class Meta:
        db_table = "problem"
        unique_together = (("_id", "contest"),)
        ordering = ("create_time",)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save(update_fields=["submission_number"])

    def add_ac_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save(update_fields=["accepted_number"])


class SimpleProblem(models.Model):
    lang_type = models.TextField()
    problem_type = models.TextField()
    problem_title = models.TextField()
    problem_content = RichTextField()
    # 问题是学校私有的还是公开的,默认是私有的，这个字段只有在school不为null时才生效
    private = models.BooleanField(default=False)
    # 问题所属学校
    school = models.ForeignKey(School, models.CASCADE, null=True, blank=True)
    # 不会真的有答案超过120个字符吧？不会吧？不会吧？
    options = ArrayField(models.CharField(max_length=120))
    answers = ArrayField(models.CharField(max_length=120))
    # 问题创建者
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not (self.lang_type in ['CPP', 'python', 'contest', 'innovation']):
            raise ValidationError('lang_type参数错误!')

        if not (self.problem_type in ['choice', 'question', 'comprehend', 'complete']):
            raise ValidationError('problem_type参数错误!')
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (("lang_type", "problem_type", "problem_title", "created_by"), ("lang_type", "problem_type", "problem_content", "created_by"))
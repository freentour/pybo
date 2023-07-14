from django.db import models
from django.contrib.auth.models import User
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
"""


# 기본 User 모델과 1:1 관계를 가지는 Profile 클래스 정의
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 기본 User 모델에 추가로 원하는 필드를 정의
    nickname = models.CharField(max_length=150)
    is_teacher = models.BooleanField(default=False)


"""
[주의]
아래와 같이 post_save 시그널을 이용하면 user 객체와 1:1로 연결된 profile 객체를 자동으로 생성하거나 수정할 수 있긴 함. 
하지만, 이렇게 시그널을 이용하는 방식은 코드의 복잡도를 높이고 결과적으로 유지보수를 어렵게 만드는 측면이 있음. 
따라서, 꼭 필요한 경우가 아니라면 시그널을 이용하기 보다는 다른 방법(custom manage에 helper 메소드를 구현하거나, 시그널을 발생시키는 모델의 메소드를 오버라이딩해서 사용하는)을 우선적으로 고려해 보는 것이 좋음. 
[Warning]
Signals can make your code harder to maintain. Consider implementing a helper method on a custom manager, to both update your models and perform additional logic, or else overriding model methods before using model signals.

다음 줄 부터가 실제 코드. 실제로도 여러 Exception이 발생하는 등 고려해야할 부분이 매우 많음. 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""

from rest_framework import serializers
from .models import Category

# name과 kind가 json으로 어떻게 표시될지 알려준다.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields or exclude 사용 : fields는 보여줄 것 , exclude는 제외할 것
        fields = (
            "pk",
            "name",
            "kind",
        )

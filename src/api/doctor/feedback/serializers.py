from api.generics.generics import CustomModelSerializer
from doctor.feedback.models import Feedback
from doctor.feedback.validators import Validations
from doctor.utils import send_email


class FeedbackListSerializer(CustomModelSerializer):

    def validate(self, attrs):
        return Validations.validate_message(
            attrs
        )

    def create(self, validated_data):
        feedback = Feedback.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        send_email(
            "Habits of Health Feedback from {}".format(self.context['request'].user.email),
            "Hello Admin,\n\nFeedback ID: {}\n\n{}\n\nRegards,\n{}".format(
                feedback.id,
                validated_data.get('message'),
                validated_data.get(
                    self.context['request'].user.get_name_or_email()
                )
            ),
            self.context['request'].user.email
        )
        return feedback

    class Meta:
        model = Feedback
        exclude = [
            "updated_at",
            "user"
        ]

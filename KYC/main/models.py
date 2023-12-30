from django.db import models
from users.models import User


class Document(models.Model):
    """Модель для хранения информации о загруженных документах."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"Document {self.user.email} Uploaded at {self.uploaded_at}"

    class Meta:
        verbose_name = "документ"
        verbose_name_plural = "документы"

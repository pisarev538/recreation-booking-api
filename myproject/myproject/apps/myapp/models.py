from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _ #(i18n)
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField(
        blank=True
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles"
    )

    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replites"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]

    def __str__(self):
        return f"Комментарий к статье {self.article}"
    
class UserProfile(models.Model):
    """
    Профиль пользователя.

    Данная модель хранит дополнительные данные пользователя:
    номер телефона, биографию и тд, которые не входят в стандартную User
    """

    # 1 к 1 User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователи")
    )

    # Иконка профиля пользователя
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        default="avatars/default.jpg",
        verbose_name=_("Аватар")
    )

    # Краткая информация о пользователе
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_("Биография")
    )

    # Дата рождения пользоватея
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Дата рождения")
    )

    # Местоположения пользователя
    location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Местоположение")
    )

    # Номер телефона пользователя
    phone_number = models.CharField(
        max_length=21,
        blank=True,
        verbose_name=_("Номер телефона")
    )

    # Показывает есть ли у пользвателя премиум статус
    is_premium = models.BooleanField(
        default=False,
        verbose_name=_("Премиум-статус")
    )

    # Хочет ли получать уведомления
    notifications_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Получать уведомления")
    )

    # Json социальные сети
    social_links = models.JSONField(
        default=dict, 
        null=True,
        blank=True,
        help_text=('Формат: {"vk": "url", "vk2": "url"}'),
        verbose_name=_("Социальные сети")
    )

    article_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name=_("Количество опубликовыанных статей")
    )

    comment_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name=("Количество комментариев")
    )

    followers_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name=("Количество подписчиков")
    )

    class Meta:
        verbose_name = _("Профиль пользователя")
        verbose_name_plural = _("Профили пользователей")
        ordering = ["user"]

    def __str__(self):
        """Вернет строковое представление пользователя"""
        return f"Профиль пользователя {self.user.username}"
    
    def get_age(self):
        """Вычисляет текущий возраст"""

        if not self.birth_date:
            return None

        today = date.today() # from datetime import date
        
        return (
            today - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        )
    
    def update_articles_count(self):
        """Обновляет кол-во опубликованных статей"""
        self.article_count = self.user.article_set.filter(is_published=True).count()
        self.save(update_fields=["article_count"])

    def update_comments_count(self):
        """Обновляет количество комментариев"""
        self.comment_count = Comment.objects.filter(author_name=self.user.username).count()
        self.save(update_fields=["comment_count"])

    def increment_followers(self):
        """Увеличивает кол-во подписчиков на 1"""
        self.followers_count += 1
        self.save(update_fields=["followers_count"])
    
    def decrement_followers(self):
        """Уменьшает кол-во подписчиков на 1"""
        if self.followers_count > 0:
            self.followers_count -= 1
            self.save(update_fields=["followers_count"])

    def has_custom_avatar(self):
        """Загружен ли у пользователя свой аватар"""
        return bool(
            self.avatar and self.avatar != "avatars/default.jpg"
        )
    
    def get_social_links(self, platform):
            """Веренет ссылку на соцсеть"""
            return self.social_links.get(platform)

    def set_social_links(self, platform, url):
        """Установит или обновит ссылку на соцсеть"""
        self.social_links[platform] = url
        self.save(update_fields=["social_links"])

    def get_full_name(self):
        """Вернет полное имя пользователя"""
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.user.username
    
    def get_published_article(self):
        """Список опубликованных статей"""
        return self.user.article_set.filter(is_published=True)

class Bookmark(models.Model):
    """
    Закладка пользователя на статью
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователи")
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        verbose_name=_("Статья")
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name=_("Дата добавления")
    )

    notes = models.TextField(
        blank=True,
        verbose_name=_("Заметки")
    )

    class Meta:
        verbose_name=_("Закладки")
        verbose_name_plural=("Закладки")
        ordering = ["-created_at"]

        constraints=[
            models.UniqueConstraint(
                fields=["user", "article"],
                name="unique_bookmark_per_user_article"
            )
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.article.title}"

class ArticleRating(models.Model):
    """оценка статьи полльзователя"""

    RATING_CHOICES = [ 
        (1, _("Очень плохо")),
        (2, _("Плохо")),
        (3, _("Сойдет")),
        (4, _("Хорошо")),
        (5, _("Отлично")),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь")
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name=_("Статья")
    )

    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        verbose_name=_("Рейтинг")
    )

    comment = models.TextField(
        blank=True,
        verbose_name=_("Комментарий к оценке")
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name=_("Дата добавления")
    )

    class Meta:
        verbose_name=_("Оценка статьи")
        verbose_name_plural=_("Оценки статей")
        ordering=["-created_at"]
        constraints=[
            models.UniqueConstraint(
                fields=["user", "article"],
                name="unique_rating_per_user_article"
            )
        ]

    def __str__(self):
        return f"{self.user.username}: {self.rating} для {self.article.title}"
    
    def clean(self):
        """Проверят корректность оценки статьи"""

        errors = {}

        # 1. Проверяет, что оценка находится в допустимом диапозоне
        valid_ratings = [choice[0] for choice in self.RATING_CHOICES]

        if self.rating not in valid_ratings:
            errors["rating"] = ("Оценка должна быть от 1 до 5.")

        # 2. Если указан комментарий, нужно хотя бы 5 символов
        cleaned_comment = (self.comment or "").strip()

        if cleaned_comment and len(cleaned_comment) < 5:
            errors["comment"] = (
                "Комментарий к оценке должен быть не короче 5 символов"
            )

        #3. Если пользователь ставит низкую оценку, то требуем комментарий
        if self.rating in (1, 2) and not cleaned_comment:
            errors["comment"] = (
                "Для низкой оценки нужно указывать причину в комментарии"
            )

        #4. Автор не должен мочьоценивать собственную статью
        if self.article.author_id and self.user_id:
            if self.article.author_id == self.user_id:
                errors["user"] = (
                    "Автор не может оценивать собственную работу."
                )

        if errors:
            raise ValidationError(errors)
    
    @property
    def rating_display(self):
        """Вернет текстовую оценку"""
        return self.get_rating_display()
    
class ArticleView(models.Model):
    """
    История просмотра стать
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="article_view",
        verbose_name=_("Пользователь")
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="views",
        verbose_name=_("Статья")
    )

    #ключ сессии
    session_key = models.CharField(
        max_length=40,
        blank=True,
        verbose_name=_("Ключ сессии")
    )

    viewed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата просмотра")
    )

    ip_adress = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP-адрес")
    )

    class Meta:
        verbose_name = _("Просмотр статьи")
        verbose_name_plural = _("Просмотры статей")
        ordering = ["-viewed_at"]
        indexes = [
            models.Index(fields=["article", "-viewed_at"]),
            models.Index(fields=["user", "-viewed_at"]),
            models.Index(fields=["session_key"]),
        ]

    def __str__(self):
        if self.user:
            return f"{self.user.username} посмотрел стать {self.article.title}"
        return f"Аноним посмотрел стать {self.article.title}"
    
class Notification(models.Model):
    """Уведомления для пользователей"""

    NOTIFICATION_TYPES = [
        ("comment", _("Новый комментарий")),
        ("reply", _("Ответ на комментарий")),
        ("like", _("Лайк")),
        ("mention", _("Упоминание")),
    ]

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Получатель")
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notification",
        verbose_name=_("Отправитель")
    )

    notification_type = models.CharField(
        choices=NOTIFICATION_TYPES,
        max_length=20,
        verbose_name=_("Тип уведомления")
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        verbose_name=_("Статья")
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications",
        verbose_name=_("Комментарий")
    )

    message = models.TextField(
        blank=True,
        verbose_name=_("Текст уведомления")
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name=_("Прочитано")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания")
    )

    class Meta:
        verbose_name = _("Уведомление")
        verbose_name_plural = _("Уведомления")
        ordering=["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.recipient.username}: {self.get_notification_type_display()}"
    
    def mark_as_read(self):
        """Пометит уведомление как прочитаное"""
        self.is_read = True
        self.save(update_fields=["is_read"])

class Subscription(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="subscriptions", 
        verbose_name="Подписчик"
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="author_followers", 
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "author") # Чтобы нельзя было подписаться дважды

    def __str__(self):
        return f"{self.user.username} -> {self.author.username}" 
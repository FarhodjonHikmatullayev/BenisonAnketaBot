from django.db import models


class User(models.Model):
    ROLE_CHOICES = (
        ('user', 'Oddiy foydalanuvchi'),
        ('admin', 'Admin')
    )
    LANGUAGE_CHOICES = (
        ('rus', 'Rus tili'),
        ('uzb', "O'zbek tili")
    )
    full_name = models.CharField(max_length=221, null=True, blank=True, verbose_name="F.I.Sh")
    username = models.CharField(max_length=221, null=True, blank=True, verbose_name="Username")
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user', null=True, blank=True,
                            verbose_name='Foydalanuvchi roli')
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    language = models.CharField(max_length=3, choices=LANGUAGE_CHOICES, default='uzb', null=True, blank=True,
                                verbose_name="Til")
    joined_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Qo'shilgan vaqti")

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.full_name}"


class Region(models.Model):
    name_uzb = models.CharField(max_length=221, null=True, blank=True, verbose_name="Viloyat nomi(Uzb)")
    name_rus = models.CharField(max_length=221, null=True, blank=True, verbose_name="Viloyat nomi(Rus)")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Vaqt")

    class Meta:
        db_table = 'region'
        verbose_name = 'Region'
        verbose_name_plural = 'Viloyatlar'

    def __str__(self):
        return f"{self.name_uzb}"


class Branch(models.Model):
    title_uzb = models.CharField(max_length=221, verbose_name="Filial nomi(Uzb)")
    title_rus = models.CharField(max_length=221, verbose_name="Filial nomi(Rus)")
    description_uzb = models.CharField(max_length=221, verbose_name="Qo'shimcha(Uzb)")
    description_rus = models.CharField(max_length=221, verbose_name="Qo'shimcha(Rus)")
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Viloyat")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Vaqt")

    class Meta:
        db_table = 'branch'
        verbose_name = 'Branch'
        verbose_name_plural = 'Filiallar'

    # 40.06949317549266, 64.74132203916554
    def __str__(self):
        return f"{self.title_uzb}"


class Category(models.Model):
    title_uzb = models.CharField(max_length=221, verbose_name="Kategoriya nomi(Uzb)")
    title_rus = models.CharField(max_length=221, verbose_name="Kategoriya nomi(Rus)")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Vaqt")

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Ish kategoriyalari'

    def __str__(self):
        return f"{self.title_uzb}"


class Vacancy(models.Model):
    title_uzb = models.CharField(max_length=221, verbose_name="Vakansiya nomi(Uzb)")
    title_rus = models.CharField(max_length=221, verbose_name="Vakansiya nomi(Rus)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    photo = models.ImageField(upload_to='vacancies/', verbose_name="Rasm")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Viloyat")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name="Filial")
    description_uzb = models.TextField(verbose_name="Vakansiya haqida(Uzb)")
    description_rus = models.TextField(verbose_name="Vakansiya haqida(Rus)")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Vaqt")

    class Meta:
        db_table = 'vacancy'
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vakansiyalar'

    def __str__(self):
        return self.title_uzb


class Resume(models.Model):
    GENDER_CHOICES = (
        ('male', 'Erkak'),
        ('female', 'Ayol')
    )
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Viloyat")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE,
                                 verbose_name="Ish yo'nalishi")
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Filial")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Vakansiya")
    first_name = models.CharField(max_length=221, null=True, blank=True, verbose_name="Ism")
    last_name = models.CharField(max_length=221, null=True, blank=True, verbose_name="Familiya")
    fathers_name = models.CharField(max_length=221, null=True, blank=True, verbose_name="Otasining ismi")
    gender = models.CharField(max_length=6, null=True, blank=True, choices=GENDER_CHOICES, verbose_name="Jins")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan kun")
    location = models.CharField(max_length=221, null=True, blank=True, verbose_name="Turar joy manzili")
    phone = models.CharField(max_length=221, null=True, blank=True, verbose_name="Telefon")
    email = models.CharField(max_length=221, null=True, blank=True, verbose_name="Elektron pochta")
    username = models.CharField(max_length=221, null=True, blank=True, verbose_name="Telegramdagi username")
    marital_status = models.CharField(max_length=221, null=True, blank=True, verbose_name="Oilaviy ahvoli")
    is_student = models.BooleanField(default=False, verbose_name="Talaba")
    education_form = models.CharField(max_length=221, null=True, blank=True, verbose_name="Ta'lim shakli")
    education_level = models.CharField(max_length=221, null=True, blank=True, verbose_name="Ta'lim darajasi")
    uzb_language_level = models.CharField(max_length=221, null=True, blank=True, verbose_name="O'zbek tili darajasi")
    rus_language_level = models.CharField(max_length=221, null=True, blank=True, verbose_name="Rus tili darajasi")
    computer_level = models.CharField(max_length=221, null=True, blank=True, verbose_name="Kompyuterni bilish darajasi")
    expected_salary = models.CharField(max_length=221, null=True, blank=True, verbose_name="Kutilayotgan ish haqi")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name="Surat")
    source_about_vacancy = models.CharField(max_length=221, null=True, blank=True,
                                            verbose_name="Vakansiya haqida qayerdan eshitdingiz?")
    agreement = models.CharField(max_length=221, null=True, blank=True,
                                 verbose_name="Ommaviy ofera bilan tanishib chiqing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="Foydalanuvchi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqt")

    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Rezyumelar"
        db_table = "resume"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

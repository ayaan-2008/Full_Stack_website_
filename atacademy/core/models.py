from django.db import models
from django.urls import reverse


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='AT Academy')
    tagline = models.CharField(max_length=200, default='Accelerating Triumph, Transforming Lives')
    phone = models.CharField(max_length=20, default='1800-120-4748')
    email = models.EmailField(default='support@atacademy.com')
    address = models.TextField(default='Secunderabad, Telangana')
    google_maps_url = models.URLField(blank=True, default='')
    social_media = models.JSONField(default=dict, blank=True)
    student_portal_url = models.URLField(blank=True, default='')
    header_logo = models.ImageField(upload_to='logos/', blank=True)
    footer_logo = models.ImageField(upload_to='logos/', blank=True)
    videos_url = models.URLField(blank=True, default='')

    career_guidance_icon = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Career Guidance feature')
    materials_icon = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Study Materials feature')
    interview_prep_icon = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Interview Preparation feature')
    placement_icon = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Placement Assistance feature')
    excel_banner = models.ImageField(upload_to='home/', blank=True, help_text='Banner image below the feature grid')

    nutshell_illustration = models.ImageField(upload_to='home/', blank=True, help_text='Large illustration for Career Services section')
    nutshell_1 = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Technical Seminars')
    nutshell_2 = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Resume Preparation')
    nutshell_3 = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Mock Interviews')
    nutshell_4 = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Placement Assistance')
    nutshell_5 = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Internship')
    nutshell_6 = models.ImageField(upload_to='home/', blank=True, help_text='Icon for Real-time Projects')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class NavigationItem(models.Model):
    label = models.CharField(max_length=100)
    href = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    has_dropdown = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class FooterLinkGroup(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Footer Link Groups'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    group = models.ForeignKey(FooterLinkGroup, on_delete=models.CASCADE, related_name='links')
    label = models.CharField(max_length=100)
    href = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.group.title} - {self.label}"


class SearchedTerm(models.Model):
    label = models.CharField(max_length=200)
    href = models.CharField(max_length=200, default='#')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Searched Terms'

    def __str__(self):
        return self.label


class Technology(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='technologies/', blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    fee = models.CharField(max_length=50, default='₹38,000')
    duration = models.CharField(max_length=50, default='4-6 Months')
    image = models.URLField(blank=True, default='')
    image_file = models.ImageField(upload_to='courses/', blank=True)
    description = models.TextField(blank=True, default='')
    features = models.JSONField(default=list, blank=True)
    category = models.CharField(max_length=50, blank=True, default='general')
    brochure = models.FileField(upload_to='brochures/', blank=True, help_text='PDF brochure for this course')
    order = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True, default='')
    meta_description = models.TextField(blank=True, default='')
    technologies = models.ManyToManyField(Technology, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        if self.image:
            return self.image
        return ''


class Branch(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    address = models.CharField(max_length=200, blank=True, default='')
    image = models.ImageField(upload_to='branches/', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    google_maps_url = models.URLField(blank=True, default='')
    order = models.IntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True, default='')
    meta_description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('branch_detail', kwargs={'slug': self.slug})


class Programme(models.Model):
    MODE_CHOICES = [
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
        ('offline', 'Offline'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='programmes')
    institution_name = models.CharField(max_length=200, default='AT Academy')
    institution_logo = models.ImageField(upload_to='programmes/', blank=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='online')
    duration = models.CharField(max_length=50, default='4-6 Months')
    fee_range = models.CharField(max_length=100, default='₹38,000 - ₹60,000')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} - {self.institution_name}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='testimonials/', blank=True)
    image_url = models.URLField(blank=True, default='')
    video_url = models.URLField(blank=True, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''


class SuccessStory(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='success_stories/', blank=True)
    image_url = models.URLField(blank=True, default='')
    video_url = models.URLField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Success Stories'

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''


class HiringPartner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/', blank=True)
    logo_url = models.URLField(blank=True, default='', help_text='External URL for logo (S3, CDN, etc.)')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_logo_url(self):
        if self.logo_url:
            return self.logo_url
        if self.logo:
            return self.logo.url
        return ''


class Certification(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='certifications/', blank=True)
    image_url = models.URLField(blank=True, default='', help_text='External URL for image')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='blogs/', blank=True)
    image_url = models.URLField(blank=True, default='')
    date = models.DateField(auto_now_add=True)
    meta_title = models.CharField(max_length=200, blank=True, default='')
    meta_description = models.TextField(blank=True, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''


class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    image_url = models.URLField(blank=True, default='')
    category = models.CharField(max_length=50, blank=True, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100, blank=True, default='')
    branch = models.CharField(max_length=100, blank=True, default='')
    qualification = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.course}"


class CallbackRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100, blank=True, default='')
    branch = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Callback Requests'

    def __str__(self):
        return f"{self.name} - {self.course}"


class RecruiterContact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    company_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Recruiter Contacts'

    def __str__(self):
        return f"{self.name} - {self.company_name}"


class BrochureRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='brochure_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Brochure Requests'

    def __str__(self):
        return f"{self.name} - {self.course.name}"


class CourseBrochure(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='brochures')
    title = models.CharField(max_length=200, help_text='e.g. Full Stack Python Syllabus 2026')
    file = models.FileField(upload_to='brochures/', help_text='PDF brochure')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Course Brochures'

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class LiveProject(models.Model):
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    tech_stack = models.CharField(max_length=200, blank=True, default='')
    duration = models.CharField(max_length=50, blank=True, default='')
    image = models.ImageField(upload_to='live_projects/', blank=True)
    image_url = models.URLField(blank=True, default='')
    abstract_file_1 = models.FileField(upload_to='abstracts/', blank=True)
    abstract_file_2 = models.FileField(upload_to='abstracts/', blank=True)
    abstract_file_3 = models.FileField(upload_to='abstracts/', blank=True)
    github_url = models.URLField(blank=True, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Live Projects'

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return ''


class Internship(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, default='')
    company = models.CharField(max_length=100, blank=True, default='')
    course = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    intern_image = models.ImageField(upload_to='internships/interns/', blank=True)
    intern_image_url = models.URLField(blank=True, default='')
    company_logo = models.ImageField(upload_to='internships/companies/', blank=True)
    company_logo_url = models.URLField(blank=True, default='')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Internships'

    def __str__(self):
        return f"{self.name} - {self.company}"

    def get_intern_image_url(self):
        if self.intern_image_url:
            return self.intern_image_url
        if self.intern_image:
            return self.intern_image.url
        return ''

    def get_company_logo_url(self):
        if self.company_logo_url:
            return self.company_logo_url
        if self.company_logo:
            return self.company_logo.url
        return ''

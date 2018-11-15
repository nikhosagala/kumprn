from django.db import models
from django.utils.text import slugify


def generate_slug(model_class: models.Model, base_text: str, tries=0) -> str:
    """ Create a unique slug for the given model_class.

    .. warning::

        Makes the slightly naive assumption that your slug field will be called 'slug'

    :param model_class: A django model class (NOT the instance)
    :param base_text: Some text to use as a base for the slug, such as the 'name'
    :param tries: Previous attempts to geenrate the slug
    :return: A unique slug for an item from the database.
    """
    candidate_slug = f'{slugify(base_text)}-{tries}' if tries else slugify(base_text)
    if model_class.objects.filter(slug=candidate_slug).exists():
        return generate_slug(model_class, base_text, tries + 1)
    return candidate_slug


class MonoLangSlugField(models.SlugField):
    """ Field that automatically generates a slug from a CharField before saving.
    """

    def __init__(self, from_field='title', *args, **kwargs):
        if 'unique' not in kwargs:
            kwargs['unique'] = True
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 150
        super(MonoLangSlugField, self).__init__(*args, **kwargs)
        self.from_field = from_field

    def pre_save(self, model_instance: any, add: bool):
        if not getattr(model_instance, self.attname):
            source = getattr(model_instance, self.from_field)
            setattr(
                model_instance,
                self.attname,
                generate_slug(model_instance.__class__, source)
            )
        return super(MonoLangSlugField, self).pre_save(model_instance, add)


class TimestampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimestampedModel):
    title = models.CharField(max_length=255)
    slug = MonoLangSlugField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Tag(BaseModel):
    pass

    class Meta:
        db_table = 'tag'


class News(BaseModel):
    draft = 'draft'
    deleted = 'deleted'
    publish = 'publish'

    STATUS = (
        (draft, 'Draft'),
        (deleted, 'Deleted'),
        (publish, 'Publish')
    )

    status = models.CharField(choices=STATUS, max_length=10)
    content = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tags')

    class Meta:
        db_table = 'news'

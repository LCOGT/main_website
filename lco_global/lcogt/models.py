from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.fields import RichTextField, FileField
from mezzanine.pages.models import RichTextPage, Page
from mezzanine.core.models import Displayable, RichText, Ownable
from mezzanine.utils.models import AdminThumbMixin
from mezzanine.utils.urls import slugify, unique_slug
from filebrowser_safe.fields import FileBrowseField


class LCOPage(Page):
    content = RichTextField(_("Main Content"), default="", help_text=_('Main content'), blank=True)
    extra_info = RichTextField(_("Extra info"), default="", help_text=_('This information will appear in the side bar or directly below title if No Side Block is checked'), blank=True)
    no_side_block = models.BooleanField(_("No side block"),default=False, help_text=_("Check this if you don't want a side block"))
    no_links = models.BooleanField(_("No links in footer"),default=False, help_text=_("Check this if you don't want a links section in the footer"))
    use_parent = models.BooleanField(_("Use parent's title"), default=False, help_text=_("Check if you want to use a longer title and have it appear below the bar"))
    class Meta:
        verbose_name = _("LCO Page+")
        verbose_name_plural = _("LCO Pages+")
        db_table = 'lcogt_lcopage'

class Activity(Page, Ownable):
    full_text = RichTextField(_("full text"),
            help_text=_("The full activity text"),
            default="", blank=True)
    goals = RichTextField(_("goals"),
        help_text=_("What are the overall aims of the activity."),
        default="", blank=True)
    summary = RichTextField(_("summary"),
        help_text=_("A catchy introductory paragraph."),
        default="", blank=True)
    observing_time = models.IntegerField(_('Observing time'),blank=True,null=True)
    archive_data = models.BooleanField(_('Archive data'),default=False)
    planning = RichTextField(_("planning"),
        help_text=_("What do you need to do in preparation."),
        default="", blank=True)
    background = RichTextField(_("background"),
        help_text=_("What background information would useful to a non-specialist."),
        default="", blank=True)
    next_steps = RichTextField(_("next steps"),
        help_text=_("What can the audience do after this activity?"),
        default="", blank=True)
    featured_image = FileBrowseField("Image", max_length=200, directory="files/", extensions=[".jpg",".png",".gif",'.jpeg'], blank=True, null=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related activities"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        db_table = 'lcogt_activity'

class Seminar(Page):
    abstract = RichTextField(_("abstract"),
            help_text=_("What the talk will be about."),
            default="", blank=True)
    seminardate = models.DateTimeField(_('Seminar date/time'), blank=True,null=True)
    speaker_name = models.CharField(max_length=255, default="tdb")
    speaker_institute = models.CharField(max_length=255, blank=True,null=True)
    speaker_picture = FileBrowseField(_("Speaker mugshot"), max_length=200, directory="speakers/", extensions=[".jpg",".png",".gif",'.jpeg',".JPEG",".JPG"], blank=True, null=True)
    speaker_biog =   RichTextField(_("biography"),
            help_text=_("This field can contain HTML and should contain a few paragraphs describing the background of the person."),
            default="", blank=True)
    speaker_link = models.URLField(help_text=_("Link to speaker's institutional page."))

    class Meta:
        db_table = 'lcogt_seminar'

    def last_name(self):
        if self.speaker_name:
            return self.speaker_name.split(' ')[-1]
        else:
            return None

    def save(self):
        slug = "seminar/{}".format(slugify(self.last_name()))
        slug_qs = Seminar.objects.exclude(id=self.id)
        self.slug = unique_slug(slug_qs, "slug", slug)
        super(Seminar, self).save()


class Profile(models.Model):
    """
    A person.
    """
    user = models.OneToOneField(User)
    mugshot = FileBrowseField(_("Mugshot"), max_length=200, directory="mugshots/", extensions=[".jpg",".png",".gif",'.jpeg'], blank=True, null=True)
    bio = RichTextField(_("biography"),
                          help_text=_("This field can contain HTML and should contain a few paragraphs describing the background of the person."),
                          default="", blank=True)
    job_title = models.CharField(_("job title"), max_length=60, blank=True, help_text=_("Example: Observatory Director"))
    research_interests = models.CharField(_("research interests"), max_length=255, blank=True, help_text=_("Comma separated list"))
    current = models.BooleanField(_("current staff"),default=True)
    science_team = models.BooleanField(_("member of the science team"), default=False)

    admin_thumb_field = "mugshot"
    search_fields = ("first_name", "last_name", "bio", "job_title",)

    class Meta:
        verbose_name = _("LCOGT Person")
        verbose_name_plural = _("LCOGT People")
        db_table = 'lcogt_profile'

    @property
    def full_name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @models.permalink
    def get_absolute_url(self):
        return ("person_detail", (), {"slug": self.slug})

    def __unicode__(self):
        return "Profile for %s, %s" % (self.user.last_name, self.user.first_name)

class SpacePage(Page):
    related_activity = models.ManyToManyField(Activity,
                                 verbose_name=_("Related activities"), blank=True)
    class Meta:
        verbose_name = _("SpaceBook page")

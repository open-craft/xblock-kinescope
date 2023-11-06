"""This XBlock embeds content from Kinescope through Iframes"""

from django.core.exceptions import ValidationError
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
try:
    from xblock.utils.studio_editable import StudioEditableXBlockMixin
except ModuleNotFoundError: # For compatibility with Palm and earlier
    from xblockutils.studio_editable import StudioEditableXBlockMixin
try:
    from xblock.utils.resources import ResourceLoader
except ModuleNotFoundError: # For compatibility with Palm and earlier
    from xblockutils.resources import ResourceLoader

from xblock.validation import ValidationMessage

from .utils import _, validate_parse_kinescope_url


loader = ResourceLoader(__name__)


class KinescopeXBlock(StudioEditableXBlockMixin, XBlock):
    """
    This XBlock renders Iframe for Kinescope videos.
    """

    video_link = String(
        display_name="Video Link/URL",
        default="",
        scope=Scope.content,
        help=_("Video link copied from Kinescope dashboard.")
    )

    editable_fields = ('display_name', 'video_link')


    def validate_field_data(self, validation, data):
        """
        Validate video link and video id
        """
        if not data.video_link:
            validation.add(ValidationMessage(ValidationMessage.ERROR, _("Video Link is mandatory")))
        else:
            try:
                validate_parse_kinescope_url(data.video_link)
            except ValidationError as e:
                for msg in e.messages:
                    validation.add(ValidationMessage(ValidationMessage.ERROR, msg))


    def student_view(self, context=None):
        """
        The primary view of the KinescopeXBlock, shown to students
        when viewing courses.
        """
        try:
            video_id = validate_parse_kinescope_url(self.video_link)
        except ValidationError:
            video_id = ""
        frag = Fragment(loader.render_django_template("static/html/kinescope.html", context=context))
        frag.add_css_url(self.runtime.local_resource_url(self, "public/css/kinescope.css"))
        frag.add_javascript_url(self.runtime.local_resource_url(self, "public/js/kinescope.js"))
        frag.initialize_js('KinescopeXBlock', {'video_id': video_id})
        return frag


    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("KinescopeXBlock",
             """<kinescope/>
             """),
            ("Multiple KinescopeXBlock",
             """<vertical_demo>
                <kinescope/>
                <kinescope/>
                <kinescope/>
                </vertical_demo>
             """),
        ]

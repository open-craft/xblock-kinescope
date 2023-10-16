"""This XBlock embeds content from Kinescope through Iframes"""

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
try:
    from xblock.utils.studio_editable import StudioEditableXBlockMixin
except ModuleNotFoundError: # For compatibility with Palm and earlier
    from xblockutils.studio_editable import StudioEditableXBlockMixin
from xblock.validation import ValidationMessage


from .utils import _, is_url, parse_valid_kinescope_url


class KinescopeXBlock(StudioEditableXBlockMixin, XBlock):
    """
    This XBlock renders Iframe for Kinescope videos.
    """

    display_name = String(
        display_name=_("Display name"),
        default=_("Kinescope"),
        scope=Scope.settings,
        help=_("Display name for this XBlock."),
    )

    video_link = String(
        display_name="Video Link/URL",
        default="",
        scope=Scope.content,
        help=_(
            "Video link copied from Kinescope dashboard. The video id below is extracted "
            "from this link if provided"
        )
    )

    video_id = String(
        display_name=_("Video ID"),
        default="",
        scope=Scope.content,
        help=_(
            "UUID of the video to embed."
        ),
        resettable_editor=False
    )

    editable_fields = ('display_name', 'video_link', 'video_id')


    def clean_studio_edits(self, data):
        """
        Parse video_link if provyided and populate video_id
        """
        if "video_link" in data and (video_id := parse_valid_kinescope_url(data["video_link"])):
            data["video_id"] = video_id


    def validate_field_data(self, validation, data):
        """
        Validate video link and video id
        """
        if not data.video_link and not data.video_id:
            validation.add(ValidationMessage(
                ValidationMessage.ERROR,
                u"Atleast one of Video Link or Video Id is mandatory"
            ))
        if data.video_link:
            if not parse_valid_kinescope_url(data.video_link):
                validation.add(ValidationMessage(ValidationMessage.ERROR, u"Invalid video link"))
        else :
            if is_url(data.video_id):
                validation.add(ValidationMessage(ValidationMessage.ERROR, u"Video ID cannot be an URL"))


    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")


    def student_view(self, context=None):
        """
        The primary view of the KinescopeXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/kinescope.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/kinescope.css"))
        frag.add_javascript(self.resource_string("static/js/src/kinescope.js"))
        frag.initialize_js('KinescopeXBlock')
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

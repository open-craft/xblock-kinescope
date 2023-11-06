/* Javascript for KinescopeXBlock. */
function KinescopeXBlock(runtime, element, data) {

    $(function ($) {
        $('.kinescope_iframe', element).attr('src', 'https://kinescope.io/embed/'+data['video_id'])
    });
}

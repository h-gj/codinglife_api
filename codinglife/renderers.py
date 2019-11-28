from rest_framework.renderers import JSONRenderer


class DDJsonRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        wrapped_data = {
            'code': 1000,
            'status': 'success',
            'data': data,
            'msg': ''
        }
        return super(DDJsonRenderer, self).render(wrapped_data, accepted_media_type=None, renderer_context=None)


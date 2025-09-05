from namer.models import *

class QueryFieldsMixin():

    include_arg_name = 'fields'
    exclude_arg_name = 'fields!'

    simple_fields = None

    delimiter = ','

    def __init__(self, *args, **kwargs):
        super(QueryFieldsMixin, self).__init__(*args, **kwargs)

        try:
            request = self.context['request']
            method = request.method
        except (AttributeError, TypeError, KeyError):
            return

        if method != 'GET':
            return

        try:
            query_params = request.query_params
        except AttributeError:
            query_params = getattr(request, 'QUERY_PARAMS', request.GET)

        includes = query_params.getlist(self.include_arg_name)
        include_field_names = {
            name for names in includes for name in names.split(self.delimiter)
            if name}

        excludes = query_params.getlist(self.exclude_arg_name)
        exclude_field_names = {
            name for names in excludes for name in names.split(self.delimiter)
            if name}

        if 'full' not in query_params and self.simple_fields:
            include_field_names.update(self.simple_fields)

        if not include_field_names and not exclude_field_names:
            return

        serializer_field_names = set(self.fields)

        fields_to_drop = serializer_field_names & exclude_field_names
        if include_field_names:
            fields_to_drop |= serializer_field_names - include_field_names

        for field in fields_to_drop:
            self.fields.pop(field)

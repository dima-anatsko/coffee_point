from django.contrib import admin
from error_log.models import RequestError


class RequestErrorAdmin(admin.ModelAdmin):
    list_display = (
        'exception_name',
        'exception_value',
        'request_method',
        'path',
        'created_at'
    )
    list_filter = ('exception_name', 'request_method', 'created_at')
    search_fields = ('exception_name', 'exception_value', 'path')
    readonly_fields = (
        'exception_name',
        'exception_value',
        'exception_tb',
        'query',
        'data',
        'request_method',
        'path',
        'created_at'
    )


admin.site.register(RequestError, RequestErrorAdmin)

from django.conf import settings
from django.views.debug import SafeExceptionReporterFilter, CLEANSED_SUBSTITUTE


class ExtraSensitiveReporterFilter(SafeExceptionReporterFilter):
    def get_post_parameters(self, *args, **kwargs):
        cleansed = super(ExtraSensitiveReporterFilter, self).get_post_parameters(*args, **kwargs).copy()
        for param_substring in settings.EXTRA_SENSITIVE_POST_PARAMETERS:
            for param in cleansed:
                if param_substring in param:
                    cleansed[param] = CLEANSED_SUBSTITUTE
                    break
        return cleansed

    def get_traceback_frame_variables(self, *args, **kwargs):
        cleansed = dict(super(ExtraSensitiveReporterFilter, self).get_traceback_frame_variables(*args, **kwargs))
        for param_substring in settings.EXTRA_SENSITIVE_VARIABLES:
            for param in cleansed:
                if param_substring in param:
                    cleansed[param] = CLEANSED_SUBSTITUTE
                    break
        return cleansed.items()

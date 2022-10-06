from django.forms import DateTimeInput


class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = "widgets/bootstrap_datetimepicker.html"

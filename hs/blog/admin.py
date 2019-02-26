from django.contrib import admin
from .models import Worker, Call, Letter, Meet, Stat

admin.site.register(Worker)
admin.site.register(Call)
admin.site.register(Letter)
admin.site.register(Meet)
admin.site.register(Stat)

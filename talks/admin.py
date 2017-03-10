from django.contrib import admin
from talks.models import Proposal, Talk_Type, Suggestion

class TalkAdmin(admin.ModelAdmin):
    list_display = ("title", "talk_type",)
    list_editable = ('status')

admin.site.register(Proposal)
admin.site.register(Talk_Type)
admin.site.register(Suggestion)

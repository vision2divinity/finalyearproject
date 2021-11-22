from django.contrib import admin
from .models import*


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'created')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'votes')


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'sent_code')


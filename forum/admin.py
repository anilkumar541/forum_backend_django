from django.contrib import admin
from .models import Tag, Question, Answer


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display= ["id", "tag"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display= ["id", "title", "body", "author", "get_tags", "created_at", "updated_at"]

    def get_tags(self, obj):
        # print(obj)
        return ", ".join([tag.tag for tag in obj.tags.all()])

    get_tags.short_description= "Tags"    



@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display= ["id", "question", "body", "author", "created_at", "updated_at"]
    

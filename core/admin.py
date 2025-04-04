from django.contrib import admin

from core.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'author')
    fields = ('h1', 'title', 'slug', 'description', 'content', 'image', 'created', 'updated', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created', 'updated')
    search_fields = ('title',)
    ordering = ('-title',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

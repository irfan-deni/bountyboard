from django.contrib import admin

from .models import Task, Bid, Review


class BidInline(admin.TabularInline):
    """Show a task's bids inline on the Task change page for quick moderation."""
    model = Bid
    extra = 0
    fields = ('hunter', 'message', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('hunter',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'poster', 'hunter', 'category',
        'bounty', 'status', 'deadline', 'created_at',
    )
    list_display_links = ('title',)
    list_filter = ('status', 'category', 'created_at', 'deadline')
    search_fields = (
        'title', 'description',
        'poster__username', 'hunter__username',
    )
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ('poster', 'hunter')
    list_per_page = 25
    inlines = (BidInline,)
    fieldsets = (
        ('Task', {
            'fields': (
                'title', 'description', 'category', 'bounty',
                'poster', 'hunter', 'deadline',
            ),
        }),
        ('Status & proof', {
            'fields': ('status', 'proof_image', 'created_at'),
        }),
    )


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('task', 'hunter', 'short_message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'hunter__username', 'message')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ('task', 'hunter')

    @admin.display(description='Message')
    def short_message(self, obj):
        if len(obj.message) > 50:
            return f'{obj.message[:50]}...'
        return obj.message


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('task', 'reviewer', 'reviewee', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = (
        'task__title', 'reviewer__username',
        'reviewee__username', 'comment',
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ('task', 'reviewer', 'reviewee')

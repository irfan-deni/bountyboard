from django.contrib import admin

from .models import Claim, Proof, Review, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster', 'hunter', 'category', 'bounty', 'status', 'deadline', 'created_at')
    list_display_links = ('title',)
    list_filter = ('status', 'category', 'created_at', 'deadline')
    search_fields = ('title', 'description', 'poster__username', 'hunter__username')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ('poster', 'hunter')
    list_per_page = 25
    fieldsets = (
        ('Task', {
            'fields': ('title', 'description', 'category', 'bounty', 'poster', 'hunter', 'deadline'),
        }),
        ('Status', {
            'fields': ('status', 'created_at'),
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('task', 'reviewer', 'reviewee', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('task__title', 'reviewer__username', 'reviewee__username', 'comment')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ('task', 'reviewer', 'reviewee')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('task', 'hunter', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('task__title', 'hunter__username')
    ordering = ('-created_at',)
    autocomplete_fields = ('task', 'hunter')


@admin.register(Proof)
class ProofAdmin(admin.ModelAdmin):
    list_display = ('task', 'hunter', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'hunter__username')
    ordering = ('-created_at',)
    autocomplete_fields = ('task', 'hunter')

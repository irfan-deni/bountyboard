from django.contrib import admin

from .models import Profile, Badge


class BadgeInline(admin.TabularInline):
    model = Badge
    extra = 0
    readonly_fields = ('earned_at',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'rank', 'xp', 'rating', 'badge_count')
    list_filter = ('role', 'rank')
    search_fields = ('user__username', 'user__email', 'bio')
    list_editable = ('role', 'rank')
    ordering = ('-xp',)
    autocomplete_fields = ('user',)
    list_per_page = 25
    inlines = (BadgeInline,)

    @admin.display(description='Badges')
    def badge_count(self, obj):
        return obj.badges.count()


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'earned_at')
    list_filter = ('earned_at',)
    search_fields = ('name', 'description', 'profile__user__username')
    date_hierarchy = 'earned_at'
    ordering = ('-earned_at',)
    readonly_fields = ('earned_at',)
    autocomplete_fields = ('profile',)

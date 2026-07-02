from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'admin/dashboard.html')

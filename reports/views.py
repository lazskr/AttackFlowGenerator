"""Views for the reports app."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReportForm
from .models import Report, convert_and_save


@login_required
def report_upload(request):
    """View that processes the request made by the user to have their incident report uploaded."""
    if request.method == "POST":
        #  ReportForm instance is created
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user  # assigning the logged-in user
            form.save()  # saves the form in the Report model
            return redirect("report_list")  # stay on the same html page (upload)
    else:
        # if the request is a GET => user is viewing page for the first time
        # hence, form instance is created and the upload html page is loaded with the
        # new form
        form = ReportForm()
    return render(request, "reports/upload.html", {"form": form})


@login_required
def report_update(request, id):
    """View for editing existing reports, using a similar template to the upload view."""
    report: Report = get_object_or_404(Report, id=id)

    if request.method == "POST":
        if "delete" in request.POST:
            report.delete()
            return redirect("report_list")
        else:
            form = ReportForm(request.POST, request.FILES, instance=report)
            if form.is_valid():
                updated_report = form.save()
                # Convert to PDF if it's a DOCX
                convert_and_save(updated_report)
                return redirect("report_list")
    else:
        form = ReportForm(instance=report)

    return render(request, "reports/update.html", {"form": form})


@login_required
def report_list(request):
    """View for showing all reports owned by the user."""
    if request.user.is_superuser:
        reports = Report.objects.all()
    else:
        reports = Report.objects.filter(user=request.user)

    return render(request, "reports/list.html", {"reports": reports})


@login_required
def report_details(request, id):
    """View for inspecting report details and annotations."""
    if request.user.is_superuser:
        report = get_object_or_404(Report, id=id)
    else:
        report = get_object_or_404(Report, id=id, user=request.user)
    return render(request, "reports/details.html", {"report": report})

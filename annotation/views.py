"""Views for the annotations app."""
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnnotationForm
from .models import Annotation, Report
from .utils import extract_text_from_pdf

# Create your views here.


@login_required
def annotation_edit(request, id):
    """View that renders the annotation interface template and handles submitting annotations."""
    report = get_object_or_404(Report, id=id, user=request.user)
    if request.method == "POST":
        print(request.body)
        form = AnnotationForm({"annotation": request.body})
        if form.is_valid():
            form.save(commit=False)
            form.instance.report = report
            form.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    annotation = report.annotation_set.order_by("-upload_date").first()
    if annotation is None:
        annotation = {"highlights": {}, "annotations": []}
    else:
        annotation = annotation.annotation

    return render(
        request,
        "annotation/edit.html",
        {"report": report, "annotation": annotation},
    )


@login_required
def annotation_view(request, id):
    """View that renders the annotation interface template and handles submitting annotations."""
    annotation = get_object_or_404(Annotation, id=id)
    report = annotation.report
    if not request.user.is_superuser and report.user != request.user:
        raise Http404()

    if request.method == "POST":
        # User attempting to verify annotation
        if request.user.is_superuser:
            annotation.verified = True
            annotation.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    return render(
        request,
        "annotation/view.html",
        {
            "report": report,
            "annotation": annotation.annotation,
            "verified": annotation.verified,
        },
    )


@login_required
def annotationInterfaceView(request):
    """View that renders the annotation interface template."""
    report_id = request.GET.get("report_id")
    if not report_id:
        return redirect("report_select")

    report = get_object_or_404(Report, id=report_id)
    text = extract_text_from_pdf(report.file.path)

    return render(
        request, "annotation/annotation.html", {"report_id": report_id, "text": text}
    )


@login_required
def selectReportView(request):
    """View that renders the report selection template."""
    return render(request, "annotation/report-list.html")

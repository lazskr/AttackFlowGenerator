"""Views for the visualisation app."""

from json import JSONDecodeError, dumps, loads

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from annotation.models import Annotation

from .mermaid import convert_json, convert_to_mermaid


def index(request):
    """View for visualising Attack Flows via server-side JSON to MMD conversion."""
    mermaid = ""
    uploaded_json = ""
    title = ""

    if request.method == "POST":
        try:
            mermaid = convert_to_mermaid(uploaded_json := request.POST["annotations"])
            title = next(
                entry
                for entry in loads(uploaded_json)["objects"]
                if entry["type"] == "attack-flow"
            )["name"]
        except JSONDecodeError:
            mermaid = "Invalid JSON provided"

    return render(
        request,
        "visualisation/view.html",
        {"mermaid": mermaid, "json": uploaded_json, "title": title, "tools": True},
    )


@login_required
def visualise_annotation(request, id):
    """View creates an Attack Flow visualisation for a user-created annotation."""
    report = get_object_or_404(Annotation, id=id)
    uploaded_json = convert_json(report.annotation)
    mermaid = convert_to_mermaid(uploaded_json)

    return render(
        request,
        "visualisation/view.html",
        {"mermaid": mermaid, "json": dumps(uploaded_json, indent=2)},
    )

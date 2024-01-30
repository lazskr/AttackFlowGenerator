"""Generate `Mermaid graphs <https://mermaid-js.github.io/mermaid/#/>`__ from Attack Flow.
Includes code from official attack flow repository <https://github.com/center-for-threat-informed-defense/attack-flow/>`__.
"""

import textwrap
import uuid

from stix2 import parse

_CONFIDENCE_NUM_TO_LABEL = [
    (0, 0, "Speculation"),
    (1, 20, "Very Doubtful"),
    (21, 40, "Doubtful"),
    (41, 60, "Even Odds"),
    (61, 80, "Probable"),
    (81, 99, "Very Probable"),
    (100, 100, "Certainty"),
]

# SDO types to ignore when making visualizations.
VIZ_IGNORE_SDOS = ("attack-flow", "extension-definition")

# Common properties to ignore when making visualizations.
VIZ_IGNORE_COMMON_PROPERTIES = (
    "created",
    "external_references",
    "id",
    "modified",
    "revoked",
    "spec_version",
    "type",
)


def convert_json(input_data):
    """Create a mapping between 'id' and 'technique_id' based on annotations."""
    id_to_technique_id = {}
    for annotation in input_data["annotations"]:
        if annotation["type"] == "attackAction":
            id_to_technique_id[annotation["id"]] = annotation["technique_id"]

    output_data = {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid4()}",
        "objects": [
            {
                "type": "attack-flow",
                "id": f"attack-flow--{uuid.uuid4()}",
                "name": "qwf",
                "description": "qfw",
                "scope": "qfw",
                "start_refs": ["fqw"],
            }
        ],
    }

    # Process highlights
    for highlight_key, highlight_list in input_data["highlights"].items():
        for highlight in highlight_list:
            if highlight["id"] in id_to_technique_id:
                highlight_id = id_to_technique_id[highlight["id"]]
            else:
                highlight_id = highlight["id"]

            action_object = {
                "type": "attack-action",
                "id": highlight_id,
                "technique_id": "",
                "name": "",
                "technique_ref": "",
                "description": highlight["content"],
                "asset_refs": [],
                "effect_refs": [],
            }
            output_data["objects"].append(action_object)

    # Process annotations
    for annotation in input_data["annotations"]:
        if annotation["type"] == "attackAction":
            action_object = {
                "type": "attack-action",
                "id": id_to_technique_id.get(annotation["id"], annotation["id"]),
                "technique_id": annotation["technique_id"],
                "name": annotation["action_name"],
                "technique_ref": annotation["technique_ref"],
                "description": annotation["action_description"],
                "asset_refs": [annotation["asset_refs"]],
                "effect_refs": [annotation["effect_refs"]],
            }
            output_data["objects"].append(action_object)
        elif annotation["type"] == "attackAsset":
            asset_object = {
                "type": "attack-asset",
                "id": annotation["id"],
                "name": annotation["asset_name"],
                "description": annotation["asset_description"],
                "object_ref": annotation["object_ref"],
            }
            output_data["objects"].append(asset_object)

    return output_data


def confidence_num_to_label(num):
    """Map value integer 'confidence' to pre-defined string."""
    for low, high, label in _CONFIDENCE_NUM_TO_LABEL:
        if low <= num <= high:
            return label
    raise ValueError("Confidence number must be between 0 and 100 inclusive.")


def get_flow_object(flow_bundle):
    """Given an Attack Flow STIX bundle, extract the ``attack-flow`` object.

    :param flow_bundle stix.Bundle:
    :rtype: AttackFlow
    """
    for obj in flow_bundle.objects:
        if obj["type"] == "attack-flow":
            return obj


def get_viz_ignored_ids(flow_bundle):
    """Process a flow bundle and return a set of IDs that the visualizer should ignore,
    e.g. the extension object, the extension creator identity, etc.
    """
    ignored = set()

    # Ignore flow creator identity:
    flow = get_flow_object(flow_bundle)
    if flow_creator := flow.get("created_by_ref", None):
        ignored.add(flow_creator)

    # Ignore by SDO type:
    for obj in flow_bundle.objects:
        if isinstance(obj, dict):
            # this could happen if the SDO type is unknown
            ignored.add(obj["id"])
            continue

        if obj.type in VIZ_IGNORE_SDOS:
            ignored.add(obj.id)

        # Ignore extension creator identity:
        if obj.type == "extension-definition" and (
            ext_creator := obj.get("created_by_ref", None)
        ):
            ignored.add(ext_creator)

    return ignored


class MermaidGraph:
    """Helper class for building up a Mermaid graph."""

    def __init__(self):
        """Initialise Mermaid graph."""
        self.classes = dict()
        self.nodes = list()
        self.edges = list()

    def add_class(self, class_, shape, style):
        """Add class for object-oriented modeling."""
        self.classes[class_] = (shape, style)

    def add_node(self, node_id, node_class, label):
        """Add node (geometric shapes) in Mermaid graph."""
        self.nodes.append((node_id, node_class, label))

    def add_edge(self, src_id, target_id, text):
        """Add edge (arrows or lines) in Mermaid graph."""
        self.edges.append((src_id, target_id, text))

    def render(self):
        """Add Mermaid directives required by a renderer."""

        # Mermaid can't handle IDs with hyphens in them:
        def convert_id(id_):
            return id_.replace("-", "_")

        lines = ["graph TB"]

        for class_, (_, style) in self.classes.items():
            lines.append(f"    classDef {class_} {style}")

        lines.append("")

        for node_id, node_class, label in self.nodes:
            node_id = convert_id(node_id)
            label = label.replace('"', "%22")
            if self.classes[node_class][0] == "circle":
                shape_start = "(("
                shape_end = "))"
            else:
                shape_start = "["
                shape_end = "]"
            lines.append(f'    {node_id}{shape_start}"{label}"{shape_end}')
            lines.append(f"    class {node_id} {node_class}")

        lines.append("")

        for src_id, target_id, text in self.edges:
            src_id = convert_id(src_id)
            target_id = convert_id(target_id)
            lines.append(f"    {src_id} -->|{text}| {target_id}")

        lines.append("")

        return "\n".join(lines)


def convert_to_mermaid(bundle):
    """Convert an Attack Flow STIX bundle into Mermaid format."""
    bundle = parse(bundle, allow_custom=True)

    graph = MermaidGraph()
    graph.add_class("action", "rect", "fill:none")
    graph.add_class("operator", "circle", "fill:#a66b12")
    graph.add_class("condition", "rect", "fill:#336833")
    graph.add_class("builtin", "rect", "fill:none")
    ignored_ids = get_viz_ignored_ids(bundle)

    for o in bundle.objects:
        if o["type"] == "attack-action":
            lw = 60  # line-width
            tid = o.get("technique_id", None)
            tid = f"<span class=heading>ID</span><p>{tid}</p>" if tid else ""
            name = "\n".join(textwrap.wrap(o["name"], width=(lw - 20)))
            description = "\n".join(textwrap.wrap(o.get("description", ""), width=lw))
            confidence = confidence_num_to_label(o.get("confidence", 95))
            label_lines = (
                "<div class='node-head'>"
                "<span class=heading>Action</span>"
                f"<span class='node-title'>{name}</span>"
                "</div><div class=node-body>"
                f"{tid}"
                f"<span class=heading>Description</span><p>{description}</p>"
                f"<span class=heading>Confidence</span><p>{confidence}</p>"
                "</div>"
            )

            graph.add_node(o["id"], "action", label_lines)
            for ref in o.get("effect_refs", []):
                graph.add_edge(o["id"], ref, "effect")
        elif o["type"] == "attack-condition":
            graph.add_node(
                o["id"], "condition", f"<b>Condition:</b> {o['description']}"
            )
            for ref in o.get("on_true_refs", []):
                graph.add_edge(o["id"], ref, "true")
            for ref in o.get("on_false_refs", []):
                graph.add_edge(o["id"], ref, "false")
        elif o["type"] == "attack-operator":
            graph.add_node(o["id"], "operator", o["operator"])
            for ref in o.get("effect_refs", []):
                graph.add_edge(o["id"], ref, "effect")
        elif o["type"] == "relationship":
            graph.add_edge(o["source_ref"], o["target_ref"], o["relationship_type"])
        elif o["id"] not in ignored_ids:
            type_ = (
                "<span class='node-title'>"
                + o["type"].replace("-", " ").title()
                + "<span>"
            )
            label_lines = []
            for key, value in o.items():
                if key in VIZ_IGNORE_COMMON_PROPERTIES:
                    continue
                key = key.replace("_", " ").title()
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value)
                label_lines.append(f"<span class=heading>{key}</span><p>{value}</p>")

            node_head = f"<div class='node-head other'>{type_}</div>"
            node_body = "\n".join(textwrap.wrap("\n".join(label_lines), width=80))
            graph.add_node(
                o["id"],
                "builtin",
                node_head + f"<div class='node-body'>{node_body}<div>",
            )

    return graph.render()

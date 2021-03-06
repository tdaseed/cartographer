import json
import pkg_resources
import numpy as np
from scipy.stats import mode


def json_graph(model, categories=None, scales=None):
    json_dict = {}

    # build links json representation
    json_dict["links"] = []
    for s_node, t_node, n_common in model.links_:
        link_dict = {"source": str(s_node),
                     "target": str(t_node),
                     "n_common": n_common}
        json_dict["links"].append(link_dict)

    # node json representation
    json_dict["nodes"] = []
    for (p_n, p) in enumerate(model.nodes_):
        for (c_n, c) in enumerate(p):
            node_dict = {"id": str((p_n, c_n)),
                         "int_id": model.nodes_to_int_[(p_n, c_n)],
                         "color": 1,
                         "n_members": c.shape[0]}
            if categories is not None:
                for name, arr in categories.items():
                    node_dict[name] = int(mode(arr[c], axis=None)[0])
            if scales is not None:
                for name, arr in scales.items():
                    node_dict[name] = np.mean(arr[c], axis=None)
            json_dict["nodes"].append(node_dict)

    # list of categories and scales
    e_name = "categories_and_scales"
    json_dict[e_name] = []
    for c in (["int_id"] + (list(categories.keys()) if categories
                            is not None else [])):
        json_dict[e_name].append({"name": c, "type": "category"})
    for s in (list(scales.keys()) if scales is not None else []):
        json_dict[e_name].append({"name": s, "type": "scale"})

    return json.dumps(json_dict, indent=4)


def html_graph(model, categories=None, scales=None):

    resource_package = __name__
    resource_path = '/'.join(['graph_template.html'])
    template = pkg_resources.resource_string(resource_package, resource_path)
    json_graph_str = json_graph(model, categories, scales)
    template_pars = {"json_graph": json_graph_str}
    return template.decode('utf-8').format(**template_pars)

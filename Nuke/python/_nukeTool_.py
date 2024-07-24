import nuke

def close_all_animation():
    selected_nodes = nuke.selectedNodes()
    for node in selected_nodes:
        knobs = node.knobs()
        for knob_name in knobs:
            knob = node[knob_name]
            knob.clearAnimated()


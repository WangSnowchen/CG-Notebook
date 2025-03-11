import GafferUI
import Gaffer
import GafferDispatch
import functools
import imath
import IECore
import os
import sys
import subprocess




def registerAnnotation( menu):
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    mainWindow = GafferUI.ScriptWindow.acquire( script )

    selected = script.selection()
    if selected.size():
        current_annotation = Gaffer.Metadata.value(selected[0], "annotation:greeting:text")
        initial_text = current_annotation if current_annotation else ""
        d = GafferUI.TextInputDialogue( initialText=initial_text, title="Annotation", confirmLabel="Set" )
        c = GafferUI.ColorChooserDialogue( title="Select Color",color=imath.Color3f(1),cancelLabel="Cancel",confirmLabel="OK")
        text = d.waitForText( parentWindow =  mainWindow )
        color = c.waitForColor( parentWindow = mainWindow )
        for node in selected:
            if text:
                Gaffer.Metadata.registerValue(node, "annotation:greeting:text", text)
                Gaffer.Metadata.registerValue(node, "annotation:greeting:color", color)
            else:
                Gaffer.Metadata.deregisterValue(node, "annotation:greeting:text")
                Gaffer.Metadata.registerValue(node, "annotation:greeting:color", color)

def OpenThisFileGRF(menu):
    """
    Open the directory of the current Gaffer script in the file explorer.
    """
    # Get the current script window and script
    script_window = menu.ancestor(GafferUI.ScriptWindow)
    script = script_window.scriptNode()
    
    # Get the current file path and its directory
    current_file = script['fileName'].getValue()

    current_directory = os.path.dirname(current_file)
    
    # Determine the command to open the directory based on the OS
    if sys.platform == 'win32':  # Windows
        # Use raw string for Windows path
        current_directory = current_directory.replace('/', '\\')
        subprocess.Popen(['explorer' , current_directory])
    elif sys.platform in ['linux', 'linux2']:  # Linux
        subprocess.Popen(['xdg-open', current_directory])
    elif sys.platform == 'darwin':  # macOS
        subprocess.Popen(['open', current_directory])
    else:
        print(f"Unsupported platform: {sys.platform}")

def ChangeNodeColor(menu):
    """
    Change the color of the selected nodes in the Gaffer script.
    """
    # Get the current script window and script
    script_window = menu.ancestor(GafferUI.ScriptWindow)
    script = script_window.scriptNode()
    main_window = GafferUI.ScriptWindow.acquire(script)

    # Get the selected nodes
    selected_nodes = script.selection()
    if not selected_nodes.size():
        print("No nodes selected.")
        return

    # Open the color chooser dialogue
    initial_color = imath.Color3f(1)  # Default color
    color_chooser = GafferUI.ColorChooserDialogue(
        title="Select Color",
        color=initial_color,
        cancelLabel="Cancel",
        confirmLabel="OK"
    )
    chosen_color = color_chooser.waitForColor(parentWindow=main_window)

    # If a color was chosen, apply it to the selected nodes
    if chosen_color:
        for node in selected_nodes:
            Gaffer.Metadata.registerValue(node, "nodeGadget:color", chosen_color)
    else:
        print("Color selection was cancelled.")
def resetVisualiserScale(menu):
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    mainWindow = GafferUI.ScriptWindow.acquire( script )
    scene_viewer = mainWindow.getLayout().editor(GafferUI.Viewer)
    scene_view = scene_viewer.view()
    scene_view["drawingMode"]["visualiser"]["scale"].setValue(1.0)
def changeToolOrientation(menu):
    #change view orientation
    scriptWindow = menu.ancestor( GafferUI.ScriptWindow )
    script = scriptWindow.scriptNode()
    mainWindow = GafferUI.ScriptWindow.acquire( script )
    scene_viewer = mainWindow.getLayout().editor(GafferUI.Viewer)
    scene_view = scene_viewer.view()
    scene_view["tools"]["TranslateTool"]["orientation"].setValue(0)
    scene_view["tools"]["RotateTool"]["orientation"].setValue(0)

def change_purposes_mode(menu):
    """
    Toggle the purposes mode in the scene viewer between 'render' and 'proxy'.
    """
    # Get the current scene viewer and its drawing mode
    script_window = menu.ancestor(GafferUI.ScriptWindow)
    script = script_window.scriptNode()
    main_window = GafferUI.ScriptWindow.acquire(script)
    scene_viewer = main_window.getLayout().editor(GafferUI.Viewer)
    scene_view = scene_viewer.view()
    drawing_mode = scene_view["drawingMode"]["includedPurposes"]["value"]

    # Get the current mode
    current_mode = drawing_mode.getValue()

    # Define the modes to toggle between
    render_mode = IECore.StringVectorData(['default', 'render'])
    proxy_mode = IECore.StringVectorData(['default', 'proxy'])

    # Toggle the mode
    if 'render' in current_mode:
        drawing_mode.setValue(proxy_mode)
    else:
        drawing_mode.setValue(render_mode)




def add_menu_item(menu_definition, path, command, label):
    """
    Helper function to add a menu item to the menu definition.
    
    :param menu_definition: The menu definition to append to.
    :param path: The path of the menu item.
    :param command: The command to be executed when the menu item is clicked.
    :param label: The label of the menu item.
    """
    menu_definition.append(
        path,
        {
            "command": functools.partial(command),
            "label": label
        }
    )

# Get the menu definition
menu_definition = GafferUI.ScriptWindow.menuDefinition(application)

# List of menu items to add
menu_items = [
    ("registerAnnotation", registerAnnotation, "registerAnnotation"),
    ("OpenThisFileGRF", OpenThisFileGRF, "OpenThisFileGRF"),
    ("ChangeNodeColor", ChangeNodeColor, "ChangeNodeColor"),
    ("resetVisualiserScale", resetVisualiserScale, "resetVisualiserScale"),
    ("changeToolOrientation", changeToolOrientation, "changeToolOrientation"),
    ("change_purposes_mode", change_purposes_mode, "change_purposes_mode")
]

# Add each menu item using the helper function
for item_name, command, label in menu_items:
    add_menu_item(
        menu_definition,
        "/Noise/tools/" + item_name,
        command,
        label
    )
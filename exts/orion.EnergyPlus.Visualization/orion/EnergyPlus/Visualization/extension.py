import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.usd
from pxr import Sdf, Usd
import omni.kit.viewport

from .determine_type_to_use import DetermType
from .useful_functions import Func
from .legend_overlay import LegendOverlay
from .legend_colors import BYR, FULLCOLOR, MONOCHROMATIC, PROTANOPIA, TRITANOPIA, AttributeColor
import random

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class MyExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.

    #---------------------------------------------------#
    # Class variables for data, legend colors, viewport #
    #---------------------------------------------------#
    dataList={"Simulation Data": "simulation_data",
            "Simulation Data 2": "simulation_data_2",
            "Simulation Data with None": "simulation_data_none",
            "Boolean Simulation Data": 'simulation_boolean_data'}
    legendColorList={"Blue to Yellow to Red": BYR,
                    "Full Color Spectrum" : FULLCOLOR,
                    "Monochromatic Blue": MONOCHROMATIC,
                    "Blue to Yellow (Protanopia, Deuteranopia)" : PROTANOPIA,
                    "Cyan to Red (Tritanopia)":  TRITANOPIA}
    viewport_window = omni.kit.viewport.utility.get_active_viewport_window() 

    def __init__(self) -> None:
            super().__init__()
            self.viewport_scene = None

    def on_startup(self, ext_id):
        print("[orion.EnergyPlus.Visualization] MyExtension startup")
        self._window = ui.Window("Visualize Energy Data", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                # ----------------------------------------------------------#
                # the main function on_click, visualizes energy simulations #
                # ----------------------------------------------------------#
                def on_click():
                    """Creates the colored volumes and legend for selected layer"""
                    print("clicked!")
                    # create AttributeColor object for the chosen legend color variable
                    curr_legColor = AttributeColor(LegendOverlay.findData(Func.getSelPaths(), 
                                                    Func.getComboValue(dataComboBox, MyExtension.dataList)), 
                                                    Func.getComboValue(paletteComboBox, MyExtension.legendColorList),
                                                    Func.getComboValue(legendDiviComboBox, divisions))
                    # # Testing
                    # print("TESTTESTTESTTESTTESTTESTTESTTEST")
                    # self.testing(directionComboBox, 0, 0)

                    # Remove Energy_Results xForm if it exists and recreate it to contain xForms for the colore volumes and the materials
                    omni.usd.get_context().get_stage().RemovePrim('/World/Energy_Results')
                    Func.defineXform('/World/Energy_Results/ColoredVolms')
                    Func.defineXform('/World/Energy_Results')
                    matFolder = Func.defineXform('/World/Energy_Results/Materials')
                    # assign the materials and create legend using determType class to create the right ones for the data type of the attribute you want to visualize
                    DetermType.assign(curr_legColor, matFolder, Func.getComboValue(dataComboBox, MyExtension.dataList))
                    DetermType.legend(Func.getComboValue(directionComboBox, directions), MyExtension.viewport_window)
               
                # ------------#
                # UI Elements #
                # ------------#
                ui.Label("Visualize Energy Simulation for Selected and Create Legend", 
                        style = {"alignment":ui.Alignment.CENTER, "font_size": 25}) 

                magicNumHeight = 30  # For things to look good
                with ui.HStack(height=0):
                    with ui.VStack():
                        dataComboBox = Func.makeComboAndLabel("Data", MyExtension.dataList)
                    
                    with ui.VStack():
                        paletteComboBox = Func.makeComboAndLabel("Legend Color Palette", MyExtension.legendColorList)
                    
                    with ui.VStack():
                        divisions = {"7 divisions": 7, "12 divisions": 12, '100 divisions':100}
                        legendDiviComboBox = Func.makeComboAndLabel("Legend Resolution", divisions)

                    with ui.VStack():                            
                        directions = {'top':'top', 'bottom':'bottom', 'left':'left', 'right':'right'}
                        directionComboBox = Func.makeComboAndLabel("Legend Placement", directions)
                        def dummy_legend():
                            """function to change position of legend, but not its color palette or resolution"""
                            DetermType.legend(Func.getComboValue(directionComboBox, directions), MyExtension.viewport_window)
                        directionComboBox.model.add_item_changed_fn(lambda m, i: dummy_legend())

                ui.Button("Visualize", clicked_fn=lambda: on_click(), style = {"font_size": 30})
                with ui.HStack():
                    with ui.VStack():
                        # Button for creating random data for testing purposes
                        ui.Label("Generate Random Data based on selected layer for testing", height = magicNumHeight, style = {"font_size":16})
                        ui.Button("Generate Data", clicked_fn=lambda: self.gen_all_rand_data("simulation_data"), style = {"font_size": 30})
                    
                    with ui.VStack():
                        # Button for clearing legend
                        ui.Label("Clear Legend from Screen", height = magicNumHeight, style = {"font_size":16})
                        ui.Button("Clear", clicked_fn=lambda: MyExtension.viewport_window.frame.clear(), style = {"font_size": 30})

    def on_shutdown(self):
        MyExtension.viewport_window.frame.clear()
        print("[orion.EnergyPlus.Visualization] MyExtension shutdown")
    
    # Testing function
    def testing(self, var1, var2, var3):
        # tmp = [True, False, True, False, True, False]
        # print(min(tmp))
        # print(max(tmp))
        curr_prim = Func.getPrimAtPath('/')
        for prim in Usd.PrimRange(curr_prim):
            print(Func.getPath(prim))

    # --------------------------------------------------#
    # Sub-functions to generate random data to simulate #
    # --------------------------------------------------#
    def gen_all_rand_data(self, dataName):
        """ Generate a random float from 0 to 100 for all selected prims and
        make a custom attribute for each prim to store the data in"""
        # get selected paths to generate data for
        selected_prims = Func.getSelPaths()
        for s in selected_prims:
            # Determine wheter s is a prim or a layer then act accordingly
            curr_prim = Func.getPrimAtPath(s)
            if len(curr_prim.GetChildren())==0:
                int = random.uniform(0,100)
                # boolean = 'True'
                # if int>50:
                #     boolean = 'False'
                # if int>75:
                #     boolean = 'None'
                omni.kit.commands.execute('CreateUsdAttributeCommand',
                                        prim=curr_prim,
                                        attr_name=dataName,
                                        attr_type=Sdf.ValueTypeNames.Float,
                                        custom=True,
                                        variability=Sdf.VariabilityVarying,
                                        attr_value=int)
            else:
                self.gen_one_layer_rand_data(curr_prim.GetChildren(), dataName)
    
    def gen_one_layer_rand_data(self, children, dataName):
        """recursive helper function to generate random data for one layer of prims"""
        # if children list is empty, don't need to do anything
        if len(children)==0:
            return []
        else:
            for c in children:
            # determine if first element of child is a prim or a layer then act accordingly
                if len(c.GetChildren())==0:
                    int = random.uniform(0,100)
                    # boolean = 'True'
                    # if int>50:
                    #     boolean = 'False'
                    # if int>75:
                    #     boolean = 'None'
                    omni.kit.commands.execute('CreateUsdAttributeCommand',
                                            prim=c,
                                            attr_name=dataName,
                                            attr_type=Sdf.ValueTypeNames.Float,
                                            custom=True,
                                            variability=Sdf.VariabilityVarying,
                                            attr_value=int)
                else:
                    self.gen_one_layer_rand_data(c.GetChildren(), dataName)
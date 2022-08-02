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
        print("[orion.Transparent.Material] MyExtension startup")
        # The extension Window
        self._window = ui.Window("Visualize Energy Data", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                # ----------------------------------------------------------#
                # the main function on_click, visualizes energy simulations #
                # ----------------------------------------------------------#
                def on_click():
                    """Creates the colored volumes and legend"""
                    print("clicked!")
                    # Get chosen legend color palette
                    curr_legColor = AttributeColor(LegendOverlay.findData(Func.getSelPaths(), 
                                                                Func.getComboValue(dataComboBox, MyExtension.dataList)), 
                                                                Func.getComboValue(paletteComboBox, MyExtension.legendColorList),
                                                                Func.getComboValue(legendDiviComboBox, divisions))
                    # Testing
                    print("TESTTESTTESTTESTTESTTESTTESTTEST")
                    self.testing(directionComboBox, 0, 0)
                    # Create Folders for the Colored Volumes for each zone
                    omni.usd.get_context().get_stage().RemovePrim('/World/Energy_Results')
                    Func.defineXform('/World/Energy_Results/ColoredVolms')
                    Func.defineXform('/World/Energy_Results')
                    matFolder = Func.defineXform('/World/Energy_Results/Materials')
                    # Create all the materials for the legend, then assign all meshes the appropriate mat based on data, then make the legend overlay
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
                            # If energy simulation not been visualized yet, prevent creating/changing legend
                            DetermType.legend(Func.getComboValue(directionComboBox, directions), MyExtension.viewport_window)
                        directionComboBox.model.add_item_changed_fn(lambda m, i: dummy_legend())

                ui.Button("Visualize", clicked_fn=lambda: on_click(), style = {"font_size": 30})
                with ui.HStack():
                    with ui.VStack():
                        # Button for creating random data for testing
                        ui.Label("Generate Random Data based on selected layer for testing", height = magicNumHeight, style = {"font_size":16})
                        ui.Button("Generate Data", clicked_fn=lambda: self.gen_all_rand_data("simulation_data"), style = {"font_size": 30})
                    
                    with ui.VStack():
                        # Button for clearing legend
                        ui.Label("Clear Legend from Screen", height = magicNumHeight, style = {"font_size":16})
                        def clearLegend():
                            MyExtension.viewport_window.frame.clear()
                        ui.Button("Clear", clicked_fn=lambda: clearLegend(), style = {"font_size": 30})

    def on_shutdown(self):
        MyExtension.viewport_window.frame.clear()
        print("[orion.Transparent.Material] MyExtension shutdown")
    
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
        """ Generate the random data for all selected prims and
        make a custom attribute for each prim to store the data in"""
        print('adjflaskfjsldfjasldkjsdalfkjsda')
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

# legendColors=[Gf.Vec3f(0.0, 0.0, 1),  
    #             Gf.Vec3f(0.0, 0.5, 1), 
    #             Gf.Vec3f(0, 1, 1), 
    #             Gf.Vec3f(0, 1, 0.5),
    #             Gf.Vec3f(0, 1, 0), 
    #             Gf.Vec3f(0.5, 1, 0), 
    #             Gf.Vec3f(1, 1, 0), 
    #             Gf.Vec3f(1, 0.5, 0), 
    #             Gf.Vec3f(1, 0, 0)]
    # legendColors2=[Gf.Vec3f(0.0, 0.0, 1), 
    #             Gf.Vec3f(0.0, 0.5, 1), 
    #             Gf.Vec3f(0.3, 0.5, 1), 
    #             Gf.Vec3f(0.7, 0.7, 0.2),
    #             Gf.Vec3f(1, 1, 0), 
    #             Gf.Vec3f(1, 0.7, 0), 
    #             Gf.Vec3f(1, 0.3, 0), 
    #             Gf.Vec3f(1, 0.15, 0.2), 
    #             Gf.Vec3f(1, 0, 0)]
    # legendColorsBlueYellow=[Gf.Vec3f(0.0, 51.0/255, 150.0/255), 
    #                         Gf.Vec3f(23.0/255, 80.0/255, 172.0/255), 
    #                         Gf.Vec3f(51.0/255, 115.0/255, 196.0/255), 
    #                         Gf.Vec3f(84.0/255, 148.0/255, 218.0/255),
    #                         Gf.Vec3f(115.0/255, 185.0/255, 238.0/255), 
    #                         Gf.Vec3f(134.0/255, 206.0/255, 250.0/255), 
    #                         Gf.Vec3f(165.0/255, 145.0/255, 61.0/255), 
    #                         Gf.Vec3f(176.0/255, 155.0/255, 18.0/255), 
    #                         Gf.Vec3f(196.0/255, 175.0/255, 24.0/255), 
    #                         Gf.Vec3f(217.0/255, 194.0/255, 29.0/255), 
    #                         Gf.Vec3f(237.0/255, 214.0/255, 34.0/255)]
    # legendColorsCyanRed=[Gf.Vec3f(21.0/255, 101.0/255, 109.0/255), 
    #                     Gf.Vec3f(68.0/255, 143.0/255, 154.0/255), 
    #                     Gf.Vec3f(0, 161.0/255, 172.0/255), 
    #                     Gf.Vec3f(84.0/255, 193.0/255, 207.0/255),
    #                     Gf.Vec3f(1, 190.0/255, 202.0/255),
    #                     Gf.Vec3f(240.0/255, 113.0/255, 120.0/255),  
    #                     Gf.Vec3f(1, 28.0/255, 0)]
    # oldLegendColorList={"Blue to Green to Red": legendColors, 
    #                     "Blue to Yellow to Red": legendColors2, 
    #                     "Blue to Yellow": legendColorsBlueYellow,
    #                     "Cyan to Red": legendColorsCyanRed}
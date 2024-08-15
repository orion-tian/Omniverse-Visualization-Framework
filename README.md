# Omniverse Visualization Framework
Omniverse extension to visualize EnergyPlus simulation data on Omniverse 3D models by dynamically altering their materials. The goal of this research is to work towards developing a digital twin in Omniverse so that architectural design decision can be quickly be made with a computer instead of with the physical building, which can be slow and costly. We also found the current tools and pipelin involving running EnergyPlus from Grasshopper with Ladybug tools using Rhino models to be especially tedious for early stage architectural design where quick iteration is emphasized. 

In addition, Grasshopper has limited capabilities to which simulations they can export and labels for the simulations they can export could not be imported into Omniverse. Thus, we wish to create Omniverse extensions to interface directly between Omniverse and energy simulations, thus streamlining the entire process with more control. My extension focuses upon visualzing the EnergyPlus data once it has been imported into Omniverse.

<img width="468" alt="Picture2" src="https://github.com/user-attachments/assets/7ac429cc-b7aa-44c8-8efe-eea855aa4444">

The extension assumes the model stores the result of an EnergyPlus simulation under custom attribute for each of its meshes. To use the extension, you first select the layers and meshes you want to visualize. You then use the drop down menus to specify the data to display, and various parameters of the resulting legend such as its color palette, resolution, and position on the viewport. 

After you click the Visualize button, a new folder called Energy_Results will be created containing a copy of the meshes you selected. They will have a new material on them that has the color of the legend its data corresponds to. The original layers of the model you selected are turned invisible to better view the visualization. In addition, the original hierarchy of the model is maintained in the Energy_Results folder so you can easily find the part of the model you are most interested in. 

<img width="468" alt="Picture3" src="https://github.com/user-attachments/assets/4d5447bc-8fc7-4249-a704-d38e5d63d840">


Current color palette options include the full color palette from red to magenta, red to yellow to blue, monochromatic blue, and color blind options for protanopia and tritanopia. The resolution of the legend controls how many legend pieces there are, whether there are 7, 12, or 100 pieces. Lower resolutions are better for categorical data or a general overview of results while higher resolutions are better for a greater level of detail and continuous data. 

_________________________________________________________________________________________________________

# Extension Project Template

This project was automatically generated.

- `app` - It is a folder link to the location of your *Omniverse Kit* based app.
- `exts` - It is a folder where you can add new extensions. It was automatically added to extension search path. (Extension Manager -> Gear Icon -> Extension Search Path).

Open this folder using Visual Studio Code. It will suggest you to install few extensions that will make python experience better.

Look for "orion.Transparent.Material" extension in extension manager and enable it. Try applying changes to any python files, it will hot-reload and you can observe results immediately.

Alternatively, you can launch your app from console with this folder added to search path and your extension enabled, e.g.:

```
> app\omni.code.bat --ext-folder exts --enable omni.hello.world
```

# App Link Setup

If `app` folder link doesn't exist or broken it can be created again. For better developer experience it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. Convenience script to use is included.

Run:

```
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```
> link_app.bat --app create
```

You can also just pass a path to create link to:

```
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```


# Sharing Your Extensions

This folder is ready to be pushed to any git repository. Once pushed direct link to a git repository can be added to *Omniverse Kit* extension search paths.

Link might look like this: `git://github.com/[user]/[your_repo].git?branch=main&dir=exts`

Notice `exts` is repo subfolder with extensions. More information can be found in "Git URL as Extension Search Paths" section of developers manual.

To add a link to your *Omniverse Kit* based app go into: Extension Manager -> Gear Icon -> Extension Search Path


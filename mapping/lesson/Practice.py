# Lesson 8 Answers.
# Luke Kaim
# Glob can be helpful. See: https://docs.python.org/2/library/glob.html.
# This exercise was compeleted without using glob.

# Import modules.
import arcpy
import os
import sys


def list_files(directory, blank_project):
    """
    recursively walk a file structure using os.listdir.
    This is very powerful.

    Recursion is a way of programming or coding a problem, in which a function
    calls itself one or more times in its body. Usually, it is returning the
    return value of this function call. If a function definition fulfils the
    condition of recursion, we call this function a recursive function.
    See: http://www.python-course.eu/recursive_functions.php

    """

    base_dir = directory
    # Create a list of subfolders. This will be used for recursion.
    subdirlist = []
    # iterate the root folder.
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        # Test if the path is a file.
        if os.path.isfile(path):
            split = os.path.splitext(item)
            if split[1] == ".mxd":
                out_path = os.path.join(directory, split[0] + ".aprx")
                # Update the mxd. Call this method only if the path is a file.
                create_project(path, out_path, blank_project)
        # Else the path is a folder.
        # Append the path to subdirlist.
        else:
            subdirlist.append(os.path.join(base_dir, item))
    # Iterate over the sub folder list.
    for subdir in subdirlist:
        # Call the list_files function.
        # This is why this method uses recursion.
        list_files(subdir, blank_project)

def create_project(mxd_path, out_path, blank_project):
    arc_proj = arcpy.mp.ArcGISProject(blank_project)
    arc_proj.importDocument(mxd_path)
    arc_proj.saveACopy(out_path)
    # Need to create project object for the copy. 
    out_project = arcpy.mp.ArcGISProject(out_path)
    return out_project
    
    
    
def bad_listdir_method(folder_loc, blank_project):
    """
    Search a folder structure.
    What are the limitations of this method? Is this a recessive search?
    """

    # List the folders in folder.
    folder_list = os.listdir(folder_loc)
    # Iterate over the folders.
    for folder in folder_list:
        child_folder = os.path.join(folder_loc, folder)
        new_folder = os.listdir(child_folder)
        # Iterate one deep subfolders. This will not search the sub sub folders.
        for i in new_folder:
            folder1 = os.path.join(child_folder, i)
            arcpy.env.workspace = folder1
            # List the files in the folder.
            files_list = arcpy.ListFiles()
            for w in files_list:
                
                split = os.path.splitext(w)
                if split[1] == ".mxd":
                    out_path = os.path.join(folder1, split[0] + ".aprx")
                    # Update the mxd. Call this method only if the path is a file.
                    mxd_path = os.path.join(folder1, w)
                    create_project(mxd_path, out_path, blank_project)


def os_walk_method(directory):
    """
    Use os.walk to walk a file structure.
    """
    # Use os.walk to walk a file structure.
    for dir_name, subdir_list, file_list in os.walk(directory):
        # Iterate over the file list. This will allow one to update all
        # mxds in that folder.
        for file_name in file_list:
            mxd = os.path.join(dir_name, file_name)
            print(mxd)


def arc_walk_method(directory):
    """
    Use arcpy.walk to walk a file structure.
    """
    # Iterate over the file structure using arcpy.da.Walk.
    for dir_name, subdir_list, file_list in arcpy.da.Walk(directory):
        # Iterate over the subfolders.
        for subdir in subdir_list:
            # Get the files from each subfolder.
            folder = os.path.join(dir_name, subdir)
            arcpy.env.workspace = folder
            files = arcpy.ListFiles()
            # Iterate over the files.
            for file_name in files:
                path = os.path.join(folder, file_name)
                # Need to test if the path is a folder or a file.
                # Only want to call update_mxd if the path is a mxd.
                # More logic could be added to ensure the file is an mxd.
                if os.path.isfile(path):
                    print(path)
                # else the path is a folder.
                else:
                    pass


def practice_2(project):
    """
    Some data you have been using comes from external sources, and at times
    there are data entries with incorrect values causing your maps to have
    blown extents. You have been tasked to check all layers in the
    Practice2/Colorado.mxd document and list their extents, so problem layers
    can be identified and corrected. "Blown" Means extent is None or undefined. 

    """
    
    for layout in project.listLayouts():
        for element in layout.listElements("MAPFRAME_ELEMENT"):
            for lyr in element.map.listLayers():
                layer_extent = element.getLayerExtent(lyr)
                print(lyr.name, layer_extent)     
    del project


def practice_3(project):
    """
    List all broken data sources in the Practice2/Colorado.mxd map document.

    """

    for map in project.listMaps():        
        for lyr in map.listLayers():
            if lyr.isBroken:
                print(lyr.name)
    del project

    
def practice_4(project, out_project):
    """
    Set all raster layers in the first data frame to be invisible.

    """
    for map in project.listMaps():
        if map.name == "Layers":
            for lyr in map.listLayers():
                if lyr.isRasterLayer == True:
                    print(lyr.name, lyr.visible)
                    lyr.visible = False
    project.saveACopy(out_project)
    del project

                    
def layer_replace_data(project, gdb_path):
    """
    Change shapefile to feature class in the mxd.
    This uses replaceDataSource. This is done layer by layer.
    This is more powerful becuase one could change the data source for each
    layer.
    """
    for map in project.listMaps():
        for lyr in map.listLayers():
            lyr_prop = lyr.connectionProperties
            lyr_prop['connection_info']["database"] = gdb_path
            lyr_prop["workspace_factory"] = "File Geodatabase"
            lyr.updateConnectionProperties(lyr.connectionProperties, lyr_prop) 
    project.save()
    del project 
    

def main():
    arcpy.env.overwriteOutput = True
    base_workspace = r"C:\Users\lucas\Documents\UNC\python 970\week8"
    lesson_folder = os.path.join(base_workspace, "lesson")
    lesson_data = os.path.join(lesson_folder, "lesson_data")
    practice_1 = os.path.join(lesson_data, "Practice1")
    problem_2_folder = os.path.join(lesson_data, "Practice2")
    blank_project = r"C:\Users\lucas\Documents\UNC\python 970\week8\blank\blank.aprx"
##    bad_listdir_method(practice_1, blank_project)
##    list_files(practice_1, blank_project)
##    os_walk_method(practice_1)
##    arc_walk_method(practice_1)

    ### problem 2
    # Create the project from mxd. 
##    colorado_mxd = os.path.join(problem_2_folder, "Colorado.mxd")
    out_path = os.path.join(problem_2_folder, "Colorado.aprx")
##    project = create_project(colorado_mxd, out_path, blank_project)
##    # get the list of layers.
##    practice_2(project)
##    practice_3(project)
    split = os.path.splitext(out_path)
    basename = os.path.basename(split[0])
##    practice_4(project, os.path.join(problem_2_folder, basename + "1.aprx"))
##    
    problem_5_folder = os.path.join(lesson_data, "Practice5")
    gdb = os.path.join(problem_5_folder, "Practice5.gdb")
    out_project = os.path.join(problem_5_folder, basename + "1.aprx")
    map_path = os.path.join(problem_5_folder, "Colorado.mxd")
    project = create_project(map_path, out_project, blank_project)
    layer_replace_data(project, gdb)

if __name__ == '__main__':
    main()

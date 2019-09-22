# Homework week 8. arcpy.mapping homework.
# Luke Kaim

# Import modules.
import os
import arcpy
# Add folder to sys.path.
sys.path.append(r"C:\Users\lucas\Documents\UNC\python 970\week7\lesson")
import useful_func


def create_project(mxd_path, out_path, blank_project):
    arc_proj = arcpy.mp.ArcGISProject(blank_project)
    arc_proj.importDocument(mxd_path)
    arc_proj.saveACopy(out_path)
    # Need to create project object for the copy. 
    out_project = arcpy.mp.ArcGISProject(out_path)
    return out_project

def save_pdf(pdf_doc, layout, pdf_path):
    """
    save a pdf and append to pdf master.
    Parameters:
        1. pdf_doc is the master pdf that all pages will be appended to.
        2. map_doc is the MapDocument object for the mxd.
        3. pdf_path is the path for each county pdf. If this is changed every
            time then the county pdf would be saved. If the pdf_path is not
            changed for each pdf then the pdf will be overwritten.
        4. df_export_width is the width of the pdf. A number that defines the
            width of the export image in pixels for a data frame export.
            df_export_width is only used when exporting a data frame.
            Exporting a page layout uses the map document page width instead
            of df_export_width.
        5.A number that defines the height of the export image in pixels for a
             data frame export. df_export_height is only used when exporting a
             data frame. Exporting a page layout uses the map document page
             height instead of df_export_height.
        6. frame is a flag to tell whether to export page_layout or frame.

    """
    try:
        layout.exportToPDF(pdf_path)

        # add dataframe page to pdf.
        pdf_doc.appendPages(pdf_path)

    except:
        useful_func.error_handling(error_code=4325)



def iterater_lyr_save_pdf(field, selection_type, project, map_frame,
                          layout, pdf_doc, workspace):
    """
    Iterate over every row of the layer. Need to fix title and export the pdf.

    Parameters:
        1. lyr is the layer object.
        2. field is the field name the selection will be based on.
        3. selection_type is the type of the selection that will be used.
        4. map_doc is the Map document object.
        4. frame is the dataframe object.
        5. pdf_doc is the master pdf that all pdf will be added to.
        6. workspace is the output folder or geodatabase location where the pdf
            will be saved.

    """
    try:
        # Iterate over the data in each map frame with a wildcard set
        #to counties.
        lyr = map_frame.map.listLayers("COUNTIES")[0]
    except:
        useful_func.error_handling(error_code=5)

    # Need to iterate over every county in the counties feature
    # class.
    try:
        with arcpy.da.SearchCursor(lyr.dataSource, field) as cursor:
            for row in cursor:
                # Need field delimiter to work on multiple input types.
                field_delimiter = arcpy.AddFieldDelimiters(lyr.dataSource,
                                                     field)
                # Strings must always be enclosed in single quotation
                # marks in queries.
                sql_expression = """ {0} = '{1}'"""
                # Create sql select statement.
                sql_select = sql_expression.format(field_delimiter,
                                                    row[0])

                # Need to select the layer by the sql_select statement.
                select = arcpy.SelectLayerByAttribute_management(lyr,
                                                    selection_type,
                                                    sql_select)
                
                map_frame.camera.setExtent(map_frame.getLayerExtent(lyr))
                
                # Zoom out farther. This is done by increasing the scale.
                map_frame.camera.scale *= 2.5
        
                try:
                    for text_element in layout.listElements("TEXT_ELEMENT"):
                        if text_element.name == "title":
                            text_element.text = row[0]
                        
                except:
                    useful_func.error_handling(error_code=11)
                    
                # need to save project with extents and titled changed. 
                try:
                    project.save()
                except:
                    useful_func.error_handling(error_code=12)

                # Save each frame as a PDF.
                frame_pdf_save = os.path.join(workspace,
                                            "{0}.pdf".format(layout.name))
                # Save PDF.
                save_pdf(pdf_doc, layout, frame_pdf_save)
    except:
        useful_func.error_handling(error_code=4)
   
    


def run_analysis():
    """
    Function runs the analysis.
    """
    
    try:
        arcpy.env.overwriteOutput = True
        base_workspace = r"C:\Users\lucas\Documents\UNC\python 970\week8"
        lesson_folder = os.path.join(base_workspace, "lesson")
        lesson_data = os.path.join(lesson_folder, "lesson_data")
        mxd = os.path.join(lesson_data, "Lesson8.mxd")
        homework_workspace = os.path.join(base_workspace, "homework")
        project_homework = os.path.join(homework_workspace, "week8_homework.aprx")
        blank_project_workspace = os.path.join(base_workspace, "blank")
        blank_project = os.path.join(blank_project_workspace, "blank.aprx")
        sr = os.path.join(lesson_data, "NAD83.prj")
    except:
        useful_func.error_handling(error_code=27)


    # Copy the mxd. This prevents updating the orginial mxd.
    project = create_project(mxd, project_homework, blank_project)

    # Creat a pdf to store all the pdf in. This is the master pdf. Pages will be
    # Added to this pdf.
    try:
        pdf_all = os.path.join(homework_workspace, "pdf_all.pdf")
        # Need to delete the pdf if it exists.
        if os.path.exists(pdf_all):
            os.remove(pdf_all)
        pdf_doc = arcpy.mp.PDFDocumentCreate(pdf_all)
        # List the data frames.
        layouts = project.listLayouts()
    except:
        useful_func.error_handling(error_code=133)

    # Iterate over the data frames.
    for layout in layouts:
        # Save each frame as a PDF.
        frame_pdf_save = os.path.join(homework_workspace,
                                        "{0}.pdf".format(layout.name))
        # Save PDF.
        save_pdf(pdf_doc, layout, frame_pdf_save)
        try:
            map_frames = layout.listElements("MAPFRAME_ELEMENT")
        except:
            useful_func.error_handling(error_code=10)
        
        for map_frame in map_frames:
            # Iterate every row in the layer.
            iterater_lyr_save_pdf("COUNTY", "NEW_SELECTION" , project, map_frame,
                                  layout, pdf_doc, homework_workspace)
            
            # Problem 2.
            try:
                map_frame.camera.spatialReference = sr
                project.save()
            except:
                 useful_func.error_handling(error_code=145)
            
            

    # Commit changes and delete variable reference
    pdf_doc.saveAndClose()
    del pdf_doc, project


def main():
    run_analysis()
    print("Finished")

if __name__ == '__main__':
    main()

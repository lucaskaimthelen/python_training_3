import arcpy
import os

def search_example(fc, fields):
    """
    demonstrated search cursor. 
    """
    count = 0
    # search cusor. find how many buglary crimes there are. 
    with arcpy.da.SearchCursor(fc, fields) as cursor:
        for row in cursor:
            if row[0] == "burglary":
                count += 1
        print("burglary", count)

def insert_example(text_file, fc, fields):
    """
    insert cursor example.
    """
    with open(text_file, "r") as data:
        for index, row in enumerate(data):
            if index > 0:
                split_string = row.split(",")
                x_loc = split_string[2] 
                y_loc = split_string[3]
                point = arcpy.Point(x_loc, y_loc)
                with arcpy.da.InsertCursor(fc, fields) as cursor:
                    cursor.insertRow((index, point))
        

        
def main():
    work_folder = r"F:\data"
    gdb_name = "python_training.gdb"
    gdb = os.path.join(work_folder, gdb_name)
    crime_fc = os.path.join(gdb, "crimeprj")
    crime_field = ["OFFENSE_CA"]
    text_file = r"F:\data\gps_track_multiple.txt"
    arcpy.env.overwriteOutput = True

    # Use search cursor to return number of burglaries.
    search_example(crime_fc, crime_field)

    #create feature class.
    seal = arcpy.CreateFeatureclass_management(gdb, "seal", "POINT", spatial_reference=4326)
    seal_fc = seal.getOutput(0)
    fields = ["OBJECTID", "SHAPE@"]
    
    # insert cursor example.
    insert_example(text_file, seal_fc, fields)
    
    print("finished")

if __name__ == "__main__":
    main()
    






    


        

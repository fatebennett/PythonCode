import arcpy
import pandas as pd
import matplotlib.pyplot as plt
import BF_lab4_functions as l4
import importlib



# Block 1:  set up github
#   1.  Get set up with an account on GitHub
#   2.  Associate your GitHub account with your GitHub Desktop
#   3.  Create a new repository for this class
#   4.  Clone the repository to your local computer
#   5.  Create a new branch for your work
#   6.  Create a new folder in the repository for this class


# Block 2:  Prep and point to your Arc project for this week
#   If you have not already, create a new ArcGIS Pro project for this class
#      that is parallel to the code folder you set up in the prior step. 
#   Ensure that you have copied the files noted in the Google Doc lab document
#      from the Data/Lab4_2025 folder. 
#          
#   
# Set the workspace to point to the geodatabase you are using for this lab

arcpy.env.workspace = r"R:\2025\Spring\GEOG562\Students\fateb\Lab4_2025\lab4_arcproject\lab4_arcproject.gdb" 

############################################################################
# Block 3:  We are going to work with the notion of extending raster objects
#   I will show you a simple example of adding functionality and then 
#   have you extend a bit further in the next block.  

#    First, reimport the lab4 functions. Remember why we need to do this? 
importlib.reload(l4)

#  Look at the code in the Lab4_functions.py file for the "SmartRaster"
#   object.  Note the method "_extract_metadata".  Test it out just to see how
#  it works.  Point to the Landsat_image_corv raster, and print out the 
#   coordinate bounds of the raster

import arcpy

# Define the input raster and the target geodatabase
input_raster = r"R:\2025\Spring\GEOG562\Students\fateb\Lab4_2025\lab4_arcproject\Landsat_image_corv.tif"
target_gdb = r"R:\2025\Spring\GEOG562\Students\fateb\Lab4_2025\lab4_arcproject\lab4_arcproject.gdb"
output_raster = f"{target_gdb}\\Landsat_image_corv"

# Copy the raster into the geodatabase
arcpy.management.CopyRaster(input_raster, output_raster)

print("Raster copied successfully!")

r = l4.SmartRaster("Landsat_image_corv")
r._extract_metadata()
print(r.metadata["bounds"])


# Question 1
#  Why do we need to use the "super()" function in the definition of the SmartRaster?

# Your answer: The super function calls the parent class. This is important in extending a class because
# we want to make sure its properly initialized and its methods are available to the child class.
#In the context of SmartRaster, if it is a subclass of another class (e.g., arcpy.sa.Raster), 
# using super() ensures that the parent class's initialization logic is executed.






# Block 4:  Add a method to the SmartRaster class to calculate the NDVI
#
#    First, UNCOMMENT MY CODE FOR CALCULATE_NDVI
#     IN THE SMARTRASTER CLASS-- THE SKELETON IS THERE
#
#
#      Go back to Lab 3 to see how we calculated the NDVI.  Use that code
#       as your basis for adding a new method to the SmartRaster class. 
#       Let's call that method "calculate_ndvi".  It should take two arguments:
#        def calculate_ndvi(self,  band4_index = 4, band3_index = 3):

#       The method should return a tuple with the okay, NDVI_object

#  Again, you'll need to add code to the calculate_ndvi function
importlib.reload(l4)
okay, ndvi = r.calculate_ndvi()
NDVI_corv = ndvi

# Assuming this is okay, write it to a new raster that we can use later
out_ndvi_file = "NDVI_corv"
if okay: 
    print("NDVI calculation successful.")
    #Check first if the file already exists
    if arcpy.Exists(out_ndvi_file):
        print(f"{out_ndvi_file} already exists. ")
    # Write the NDVI raster to a new file
    try:
        ndvi.save(out_ndvi_file)
        print(f"{out_ndvi_file}written successfully.")
    except Exception as e:
        print(f"Error writing NDVI raster: {e}")    
else:
    print("NDVI calculation failed.")

# Question 4.1 
#  In the "calculate_ndvi", the method accepts 
#    two arguments to define which band indices
#    are relevant -- band 4 and 3.  But we didn't
#    set them here -- why did it work?

#  Your answer:
#In the method definition band4 is set to 4 and band3 is set to 3. If you want to change 
# the default values, you can do so when calling the method. However in this case when you
# call the method without any arguments, it will use the default values of 4 and 3.



##########################################################
# Block 5:  Now, let's look at setting up an equivalent type of
#  vector object.  This is going to be different because there
#  really isn't one in Arc the same way there is for Rasters.
#  However, when we work with feature classes, we create
#  feature layers that exist temporarily during a session, which
#  is kind of like an object.   

#  Go to lab4_functions and find the class
#   for SmartVectorLayer. 

#  UNCOMMENT THE ENTIRE CLASS (use shift /)

#  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#  Following my comment prompts in that file, 
#   fill out the code to make the 
#   "zonal_stats_to_field" method work.  

#   Then uncomment the next few lines, run them to summarize
#     the NDVI image we just created into a new
#     field called mean_ndvi


importlib.reload(l4)
fc = "Corvallis_parcels" # remember you should have copied this into your workspace in Block 2.

#Load the fc as a smart vector layer
smart_vector = l4.SmartVectorLayer(fc)

# then get the zonal stats using the mean value
smart_vector.zonal_stats_to_field(out_ndvi_file, output_field = "NDVI_mean")

# then save it as a new feature class!
smart_vector.save_as("Corvallis_parcels_plusNDVI")


# Question 5.1

#  Re-load the file in your Arc session, and the NDVI
#    file as well.  
#    Does it look like the zonal stats for NDVI worked
#     reasonably?  Any observations or oddities? 
# 

#
#When i changed around the symbology I could see that the NDVI values were assigned differentially to 
# different parcels. There is also a MEAN field that is null for everyone. I dont know if I messed up
# on removing that. Besides that I dont have any huge observations as I dont know what exactly I expected
# the NDVI to be for corvallis since I havent worked with it much before.But the large parks tend to have 
# higher numbers which is good. 





# Block 6: 
#  Now we'll add functionality to pull this information 
#   into a Pandas data frame


# Go to the Lab4_functions.py, uncomment all of the code
#  in the "extract_to_pandas_df" chunk of smart vector, 
#  and add the small chunk of code I have asked you
#  to do.  Most of the functionality is already there

importlib.reload(l4)
okay, df = smart_vector.extract_to_pandas_df()


# Question 6.1. 
#  In the extract_to_pandas_df, what does it mean
#   that I define the "fields=None" in the original
#   call to the method, and how do I use it in the
#   code?  

# Your answer
# I think it means that the default is that if the user does not input fields than the default for the fields
# value is none. This means if they dont filter the fields than all of them will be returned. If
# they want less fields then they can input that list and filter out a smaller amount of fields. It 
# seems like a good way to set it up. It gives good multifunctionality for the user.





#################################################
# Block 7: 
#  Now we're going to take advantage of the Pandas
#   link with matplotlib to make a graph

# First, uncomment the code for the "smartPanda" 
#  class in the lab4_functions.py, and run this code
#  below.  You can just run this -- no need to 
#  fix or add anything. 

importlib.reload(l4)

x_field = "YEAR_BUILT"
y_field = "NDVI_mean" 

sp = l4.smartPanda(df)  # create the new smartPanda type

sp.scatterplot(x_field, y_field, x_min=1901, x_max = 2030)


# question 7.1
#  in the scatterplot function, I have this piece of code:
#  if x_min is not None:
#           df_to_plot = df_to_plot[df_to_plot[x_field] >= x_min]
#  You'll note that I use the same test for x_min not being "None". 
# But what about the second line -- what is df_to_plot, 
#    and what does this line achieve? 
#  


# Your answer:
# The df_to_plot is a Pandas DataFrame containing the data used for the scatterplot.
# The second line filters the DataFrame to include only rows where the x_field values are greater than or equal to x_min. 
# This ensures that only data within the specified range (x_min and potentially x_max) is used for plotting.




###############################################################
#  Block 8

#  For our final show, we'll read the parameters we want to make
#   the plot from an external file, and then use those to create
#   the plot and write it to a PNG graphic file.  
#  The control file with the parameters is a comma-delimted 
#   format -- .csv -- that can be easily read and written 
#   from a spreadsheet program like excel (or even just a 
#      text editor)

#  First, go into the smartPanda class and examine
#     the "plot_from_file" method. 
#  Then, copy the .csv file into your local directory.
#   Source .csv:  in the R: drive Data\Lab4_2025\params_1.csv
#   destination:  put this in your student folder in the 
#     lab4\PythonCode folder. 
#    Why?  This is where your Python interpreter is considering
#      the working directory for it (not the arcpy workspace, but
#      the python working directory to read and write files, load
#      functions,etc.)
#      Thus, you can point to the file itself without  the full
#      path if you want. 

# You have the SmartPanda as "sp" from above, right?
#   Here, and you have the name of the file for the control file
#  Below, simply call the "plot_from_file" method to run the .csv fil

param_file = 'params_1.csv'  #  this assumes you've placed in the 
                            # python code directory you're working in here. 
# Your code:



#  My code

ok = sp.plot_from_file(param_file)
if ok:
    print("Done plotting")


# Now check the output graphic and make sure it worked. 

# Now, save the .csv file under a different name, 
#   change the inputs -- either add in some 
#   x or y min, max values, or change
#    the fields. 
#   note the name of the .csv in your journal, 
#    and then save the .png file along with that in the 
#    journal. 
#   Try a couple different variants of fields and ranges


# Load the original CSV file

param_file = 'params_1.csv' 


ok = sp.plot_from_file(param_file)
if ok:
    print("Done plotting")



param_file = 'params_1.csv' 


ok = sp.plot_from_file(param_file)
if ok:
    print("Done plotting")



param_file = 'params_1.csv' 


ok = sp.plot_from_file(param_file)
if ok:
    print("Done plotting")


# Generate the scatterplot (assuming you have a function to do this)


# Question 8.1
#  What will happen if you give it a field that is not
#    numeric?   How might you make this work better?

# Your answer
# If you give it a field that is not numeric, it will throw an error. This would work 
# better if you added a check to see if the field is numeric before trying to plot it. 
#This could save time and effort by preventing the error from occurring in the first place.



# Question 8.2
#  In your lab document, paste in a couple of the
#    examples of the output .png files. 
#DONE


# Question 8.3
#   I don't like having to type the name of the 
#   output file because I usually just want to 
#   document the x and y variables in the filename
#   Can you describe (in words, no need for code)
#   how you might achieve that?

# Your answer:
# I would use the x and y variables to create a string that contains the names of the variables. Then
# I would just make the file name concatenate the x and y variables into a string that is the file name
#that would be in the filename section. This I would just do manually in Excel.




"""! @file csv_reader.py
  
  This file is responsible for reading the thermal camera temperature csv file and returns
  the summation of each collumn.

  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  
  """

import csv

class CSV:
    
    def __init__ (self, data_input):
        
        """! 
        This function initializes the data for the CSV reader. 
        @param data_input The data to be interpreted by the CSV reader. 
        """
        
        self.data = data_input

    def readdata(self):
        """! 
        This function loops through all of the rows and cols of 
        """
    
        self.cols = [0]*32
        snap = csv.reader(self.data, delimiter=' ', quotechar='|')
        for row in snap:
            row = row[0].split(',')
            for lines in range(len(row)):
                self.cols[lines] += int(row[lines])
            
        return(self.cols)

    def col_largest(self):
        max = 0
        idx = 0
        for n in range(32):
            if self.cols[n] > max:
                idx = n
                max = self.cols[n]
        
        return(idx,max)

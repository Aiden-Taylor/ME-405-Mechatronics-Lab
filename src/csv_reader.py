"""! @file csv_reader.py
  
  This file is responsible for reading the thermal camera temperature csv file and returns
  the summation of each collumn.

  @author Aiden Taylor, Julia Fay, Jack Foxcroft
  
  """

class CSV:
    
    def __init__ (self, data_input):
        
        """! 
        This function initializes the data for the CSV reader. 
        
        @param data_input The data to be interpreted by the CSV reader. 
        """
        
        self.data = data_input

    def readdata(self):
        """! 
        This function loops through all of the rows and cols of the csv data 
        adding up all of the numbers in each column and storing the result 
        in an array called cols. 
        
        @returns This function returns the array that holds all of the column 
                summation values. 
        """

        self.cols = [0]*32
        
        for row in self.data:
            row = row.split(',')
            #print(row)
            for lines in range(len(row)):
                self.cols[lines] += int(row[lines])
                
        return(self.cols)

    def col_largest(self):
        """! 
        This function loops through all of column summation values 
        and returns the column number and value for the column with 
        the largest total summation. 

        @returns This function returns the column index and value for
            the column with the highest total summation. 
        
        """
        max = 0
        idx = 0
        for n in range(32):
            if self.cols[n] > max:
                idx = n
                max = self.cols[n]
        
        return(idx,max)

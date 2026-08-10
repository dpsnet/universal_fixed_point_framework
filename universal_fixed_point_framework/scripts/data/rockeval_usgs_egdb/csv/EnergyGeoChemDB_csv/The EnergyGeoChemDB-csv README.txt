The EnergyGeoChemDB-csv files include all records from the EnergyGeoChem.accdb Microsoft Access database.  The Samples.csv file contains sample information records from the EnergyGeoChem.accdb Samples table. The EnergyGeoChem.accdb Analysis table contains more than 3.6 million records which exceeds the maximum amount of data for some applications. To resolve this issue the Analysis table was divided into several csv files based on the Order ID field.  The file name provides the range of order ids that each file contains. The Analysis_00003-99043.csv file contains records for OrderIDs 0003 through 99043. The Analysis_AA-BJ.csv file contains records with OrderIDs beginning with AA and continues through BJ99.  The Analysis_BK-ERP-00063.csv file contains records with OrderIDs beginning with BK and continues through ERP-00063. The Analysis_ERP-00064.csv file contains records with OrderIDs beginning with ERP-00064 and continues through X1812, which is the last OrderID in the EnergyGeoChem.accdb Analysis table. The OrderID and SampleNumber columns are Primary fields to link sample and analysis records.

When opening the csv files in Microsoft Excel, the following message will be displayed. 

-----------------------------------------------------------------------------
"By default, Excel will perform the following data conversions in this file:
- Convert large numbers into scientific notation
- Convert digits surrounding the letter "E" into scientific notation
- Remove leading zeros
- Convert continuous letters and numbers into dates

Do you want to Permanently keep these conversions?

Button: Convert   Button: Don't Convert    Button: Help"
-----------------------------------------------------------------------------

Select Don't Convert button.
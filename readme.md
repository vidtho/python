# Python scripts
Repository for python scripts. These scripts include modules performed for etl, visualisation and excel output.

### ETL

Contents of ETL folder

| **Script name**		                 |  **Descripton**
---------------------------------------- |--------------------------------------------------------------------
| csvtodb.py | Script to read csv/pipe separated file , to data frame , and finally load it to oracle db.
| config/2.txt | Config files : config.txt and config2.txt
| dbtocsv.py | Script to read config file *[config.txt]*, load a query to dataframe and , create a csv file from dataframe. <br /> **Output file : etl/csvfiles/users.csv** 
| writetofile.py | Script to write "hello world" to file <br /> and then replace the words "hello" and "world" with "Welcome" , "vidya" respectively in file.
| dbtoxlsx.py | Script to read config file *[config2.txt]*, load a queries to 3 dataframes and , <br /> add those dataframes as excel sheet with corresponding charts.<br /> **Output file : etl/xls/emp_stats_2018_04_27_1.xlsx**

### Matpotlib
Contents of matpotlib folder

| **Script name**		                 |  **Descripton**  |   **Plot Diagrams**   |
---------------------------------------- |----------------- |-----------------------|
| basic_plots.py | Script to generate following charts <br /> - line chart <br /> - bar chart <br /> - histogram  <br /> - scatter plot  <br /> - stack plot <br /> - pie chart | <br /> [Figure_1.png] <br /> [Figure_2.png] <br /> [Figure_3.png], [Figure_4.png] <br /> [Figure_5.png] <br />  [Figure_6.png] <br /> [Figure_7.png]|
| example.txt | data in csv format| 
| file_plots.py | Script to get data from example.txt and plot chart | [fileplot_1.png]
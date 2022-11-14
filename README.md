<h1>Hugen</h1>

Hugen is a tool for generating data for PostgreSQL. This tool supports several modes:

<h5>- Generating by size</h5>

You can generate a script to create a database of the desired size by using the command `--size`   

For example: `--size=9.5GB`

<h5>- Generating by pattern</h5>
You can generate a script to create a database of the desired number of schemas, tables and rows by using the command:                                    
`--filepath={path_to_file}/generation_schema.txt`

                        
    ------------------------------------------------------------------------------------------------------------                                                                          
    generation_schema.txt                                                         
    ------------------------------------------------------------------------------------------------------------
    5:10:100      # Creating 5 schemas with 10 tables and 100 rows in every table     
                                                                                  
    Schema1:3:11  # Creating 1 schema with name `Schema1` with 3 tables and 11 rows in every table                                        
                                                                                  
    Schema2:                                                                      
        Table1:5,                      # Creating 1 schema `Schema2` with 1 table `Table1`, 5 rows    
        Table2(text, int, bigint):10,  # Creating the second table `Table2` in `Schema2` with 10 rows in format:     
                                       # field1:text, field2:int, field3:bigint   
        Table3(email:varchar(50)):10   # Creating `Table3` in `Schema2` with 10 rows in format: email:varchar(50)
    ------------------------------------------------------------------------------------------------------------
    
You can set up default schema for all tables without defined schema using `--fields`. The structure is the same 
for expressing in the generation file - types separated by commas and not mandatory field names before the field type.

For example:
`--fields="int, field2: varchar, varchar(50)"`
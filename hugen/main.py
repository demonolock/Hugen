import argparse
import os

from generator.postgres_generator import PostgresGenerator
from pattern_parser import SizeParser, FileParser
from loguru import logger


def main():
    namespace = init_namespace()
    if namespace.info:
        print_info()
        exit(0)
    if namespace.size and namespace.filepath:
        logger.error("Please, define only one parameter `--size` or `--filepath`")
        exit(1)
    if not namespace.size and not namespace.filepath:
        logger.error("Please, define one parameter `--size` or `--filepath`")
        exit(1)
    if namespace.size:
        num_part, unit_part = SizeParser.parse_size(namespace.size)
        PostgresGenerator(namespace.fileout, namespace.owner).generate_by_size(num_part, unit_part)
    if namespace.filepath:
        pattern = FileParser().parse_file(namespace.filepath)
        PostgresGenerator(namespace.fileout, namespace.owner, namespace.fields).generate_by_pattern(pattern)


def init_namespace():
    parser = argparse.ArgumentParser(description="Hugen is a tool for generating data for database. For more info "
                                                 "use --info")
    parser.add_argument('--info', action='store_const', const=True, help="Show extended information about the tool")
    parser.add_argument('-f', '--filepath', help="Path to file with generating pattern. For more info use --info")
    parser.add_argument('-s', '--size', help="Size of generating DB (i.e. --size=9GB). For more info use --info")
    parser.add_argument('-df', '--fields', help="Default fields list for generating. For more info use --info",
                        default=None)
    default_owner = "postgres"
    parser.add_argument('-o', '--owner', help="Set owner for schemas and tables. Default - postgres",
                        default=default_owner)
    default_fout = f"{os.path.dirname(__file__)}/temp/generation_result.sql"
    parser.add_argument('-fout', '--fileout', help="Path to file with generated instructions for creating data base.",
                        default=default_fout)

    return parser.parse_args()


def print_info():
    info_message = '''
    Hugen is a tool for generating data for database.
    
    You can generate a script to create a database of the desired size by using command '--size'   
    In example '--size=9.5GB'.
                                                        
    You can generate a script to create a database of the desired number of       
    schemas, tables and rows by using command:                                    
    '--filepath={path_to_file}/generation_schema.txt'                             
                        
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
    
    You can set up default schema for all tables without defined schema using '--fields'. The structure is the same 
    for expressing in the generation file - types separated by commas and not mandatory field names before 
    the field type.
    For example:
    --fields="int, field2: varchar, varchar(50)"
    '''
    print(info_message)


if __name__ == "__main__":
    main()

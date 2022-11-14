from hugen.generator.base_generator import BaseGenerator
from hugen.types_.custom_enum import SizeUnit
from hugen.utils import Utils


class PostgresGenerator(BaseGenerator):
    DEFAULT_TEXT_SIZE = 40
    DEFAULT_REL_SIZE = 30

    def __init__(self, filepath: str, owner: str, default_field_list=None):
        self.fout = open(filepath, 'w')
        self.owner = owner
        if default_field_list:
            self.default_field_list = default_field_list
        else:
            self.default_field_list = "id int, firstname varchar(30), lastname varchar, number int, email varchar(30)"

    def _add_rel_info(self, rel_name: str, rel_type: str, schema: str, owner: str):
        self.fout.write(f"""
--
-- Name: {rel_name}; Type: {rel_type}; Schema: {schema}; Owner: {owner}
--
""")

    def _create_schema(self, schema_name=None) -> str:
        if not schema_name:
            schema_name = Utils.get_random_text(self.DEFAULT_REL_SIZE)
        schema_name = schema_name.lower()
        self._add_rel_info(schema_name, 'SCHEMA', '-', self.owner)
        self.fout.write(f"CREATE SCHEMA {schema_name};\n")
        self.fout.write(f"ALTER SCHEMA {schema_name} OWNER TO {self.owner};\n")
        return schema_name

    @staticmethod
    def add_field_name(field_type_list: list) -> list:
        field_list = []
        for i, field_type in enumerate(field_type_list):
            if ' ' in field_type.strip(): # We already have field name - structure `fields_name field_type`
                field_list.append(field_type)
            else:
                field_list.append(f'field{i + 1} {field_type.strip()}')
        return field_list

    def _create_table(self, schema_name: str, table_name=None, field_list=None) -> str:
        """
        schema_name: Name of creating schema
        table_name: Name of creating table
        field_list: list of field types that can contain field name. If we didn't mark the name, we will put
        default field name "field{i}", where {i} is an index of the field.
        For field_list = "varchar, email varchar, int" we will get cur_field_list = "field1, email varchar, field3"
        :return: string with create command for PostgresSQL
        """
        if not table_name:
            table_name = Utils.get_random_text(self.DEFAULT_REL_SIZE)
        schema_name = schema_name.lower()
        table_name = table_name.lower()
        if not field_list:
            field_list = self.default_field_list.split(',')
        cur_field_list = self.add_field_name(field_list)
        self._add_rel_info(table_name, 'TABLE', schema_name, self.owner)
        self.fout.write(f"CREATE TABLE {schema_name}.{table_name}({', '.join(cur_field_list)});\n")
        self.fout.write(f"ALTER TABLE {schema_name}.{table_name} OWNER TO {self.owner};\n")
        return table_name

    def _start_copy_data(self, schema_name: str, table_name: str):
        """
        schema_name: Name of creating schema
        table_name: Name of creating table
        Also we expect that self.cur_field_list was filled on `create_table` step
        :return: string with the start of copy function
        """
        self.fout.write(f"COPY {schema_name}.{table_name} FROM stdin;\n")

    @staticmethod
    def _extract_field_type_list(field_list: list) -> list:
        type_sep = ' '
        field_type_list = []
        if type(field_list) == str:
            field_list = field_list.split(',')
        for field in field_list:
            field = field.strip()
            if type_sep in field:
                field_type = field.split(type_sep)[1]
            else:
                field_type = field
            field_type_list.append(field_type)
        return field_type_list

    def _add_data(self, field_list: list):
        self.cur_field_list = None
        field_type_list = self._extract_field_type_list(field_list)
        result_command = []
        for field_type in field_type_list:
            if field_type == 'int':
                result_command.append(str(Utils.get_random_int()))
            elif 'varchar' in field_type:
                size = self.DEFAULT_TEXT_SIZE
                if '(' in field_type and ')' in field_type:  # Extract size from varchar(size)
                    size = field_type.split(')')[0].split('(')[1]
                result_command.append(Utils.get_random_text(int(size)))
            elif 'text' in field_type:
                result_command.append(Utils.get_random_text(int(self.DEFAULT_TEXT_SIZE)))
        self.fout.write('\t'.join(result_command) + '\n')

    def _end_copy_data(self):
        self.fout.write("\.\n")

    def generate_by_size(self, num_part, unit_part):
        """
        Create a schema and a table with enough rows to occupy required amount of memory
        size	    table	    lines
        1 MB	    1 MB	    7341
        10 MB	    9.8 MB	    73404
        100 MB      98 MB	    734004
        1 GB        983 MB	    7340045
        10 GB	    9.8 GB	    73400445
        """
        required_bytes = num_part * 2 ** (10 * SizeUnit.find_by_name(unit_part).value)
        schema_name = Utils.get_random_text(self.DEFAULT_REL_SIZE)
        table_name = Utils.get_random_text(self.DEFAULT_REL_SIZE)
        field_list = self.default_field_list.split(',')
        self._create_schema(schema_name)
        self._create_table(schema_name, table_name, field_list)
        self._start_copy_data(schema_name, table_name)
        magic_number = 0.0072  # empirically found value
        for i in range(int(required_bytes * magic_number) + 1):
            self._add_data(field_list)
        self._end_copy_data()
        self.fout.close()

    def generate_by_pattern(self, pattern: dict):
        for schema_name in pattern.keys():
            tables = pattern[schema_name]
            for table in tables.keys():
                if '(' in table and table[-1] == ')':  # table has information about schema
                    table_name = table.split('(')[0]
                    field_list = table.split('(')[1][:-1].split(',')
                else:
                    table_name = table
                    field_list = self.default_field_list.split(',')
                row_number = int(tables[table])
                if schema_name.isnumeric():
                    schema_amount = int(schema_name)
                    for schema_ind in range(schema_amount):
                        schema_name = self._create_schema()
                        if table_name.isnumeric():
                            table_amount = int(table_name)
                            for table_ind in range(table_amount):
                                table_name = self._create_table(schema_name=schema_name, field_list=field_list)
                                self._start_copy_data(schema_name, table_name)
                                for i in range(row_number):
                                    self._add_data(field_list)
                                self._end_copy_data()
                        else:
                            self._create_table(schema_name, table_name, field_list)
                            self._start_copy_data(schema_name, table_name)
                            for i in range(row_number):
                                self._add_data(field_list)
                            self._end_copy_data()
                else:
                    self._create_schema(schema_name)
                    if table_name.isnumeric():
                        table_amount = int(table_name)
                        for table_ind in range(table_amount):
                            table_name = self._create_table(schema_name=schema_name, field_list=field_list)
                            self._start_copy_data(schema_name, table_name)
                            for i in range(row_number):
                                self._add_data(field_list)
                            self._end_copy_data()
                    else:
                        self._create_table(schema_name, table_name, field_list)
                        self._start_copy_data(schema_name, table_name)
                        for i in range(row_number):
                            self._add_data(field_list)
                        self._end_copy_data()

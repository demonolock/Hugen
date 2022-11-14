from loguru import logger

from types_.custom_enum import SizeUnit
import re


class SizeParser:

    @staticmethod
    def parse_size(size):
        num_part = size[:-2]
        unit_part = size[-2:]
        if not SizeUnit.is_valid_unit(unit_part):
            logger.error("You can specify size only with 'KB', `MB`, `GB` or `TB`, your unit is `{}`", unit_part)
            exit(1)
        if not num_part.isnumeric():
            logger.error("The size of a generating file should be numeric, your value is `{}`", num_part)
            exit(1)
        num_part = round(float(num_part), 1)
        return num_part, unit_part


class FileParser:

    def parse_file(self, filepath) -> dict:
        gen_schema = dict()
        words = self._read_words(filepath)
        i = 2
        length = len(words)
        while i < length:
            schema = words[i - 2]
            tables = dict()
            while i < length:
                table = words[i - 1]
                fields = words[i]
                if fields[-1] == ',':
                    tables[table] = fields[:-1]
                    i += 2
                else:
                    tables[table] = fields
                    i += 3
                    gen_schema[schema] = tables
                    break
        return gen_schema

    @staticmethod
    def read_all_from_one_line(parsing_list) -> [str, str, str]:
        schema_name = ''
        table_name = ''
        field_list = ''
        if parsing_list[0].strip() != '':
            schema_name = parsing_list[0].strip()
            if parsing_list[1].strip() != '':
                table_name = parsing_list[1].strip()
                if parsing_list[2].strip() != '':
                    field_list = parsing_list[2].strip()
        return [schema_name, table_name, field_list]

    @staticmethod
    def _read_words(filepath) -> list:
        words = []
        sep = ':'
        try:
            with open(filepath, 'r') as fin:
                pattern = fin.read()
                if pattern:
                    pattern = re.sub("#.*\n", "\n", pattern)  # clear comments
                    split = list(map(lambda word: word.strip(), re.split(f'{sep}|\n', pattern)))
                    words = list(filter(lambda word: word != '', split))  # Filter empty words
        except IOError:
            print(f"Couldn't open file: `{filepath}`")
        return words

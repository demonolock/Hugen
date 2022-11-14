class BaseGenerator:

    def _create_schema(self, schema_name) -> str:
        return f"CREATE SCHEMA {schema_name};"

    def _create_table(self, schema_name: str, table_name: str, field_list: list) -> str:
        pass

    def _add_data(self, field_list: list):
        pass

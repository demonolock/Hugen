import os
import subprocess

entrypoint = f'{os.path.dirname(__file__)}/main.py'


def test_run_with_both_params():
    result = subprocess.Popen(['python', f'{entrypoint}',
                               '--size=9GB',
                               '--filepath=./resources/generation_schema.txt"'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    stdout = result.communicate()
    assert "Please, define only one parameter `--size` or `--filepath`" in str(stdout)


def test_run_without_params():
    result = subprocess.Popen(['python', f'{entrypoint}'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    stdout = result.communicate()
    assert "Please, define one parameter `--size` or `--filepath`" in str(stdout)


def test_run_with_wrong_size_param_num_part():
    result = subprocess.Popen(['python', f'{entrypoint}',
                              '--size=9AGB'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    stdout = result.communicate()
    assert "The size of a generating file should be numeric, your value is `9A`" in str(stdout)


def test_run_with_wrong_size_param_unit_part():
    result = subprocess.Popen(['python', f'{entrypoint}',
                              '--size=9.5HB'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    stdout = result.communicate()
    assert "You can specify size only with 'KB', `MB`, `GB` or `TB`, your unit is `HB`" in str(stdout)


def test_run_with_option_help():
    result = subprocess.Popen(['python', f'{entrypoint}',
                              '--help'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    stdout = result.communicate()
    assert "Hugen is a tool for generating data for database. For more info use --info" in str(stdout)


def test_run_with_option_info():
    result = subprocess.Popen(['python', f'{entrypoint}',
                               '--info'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT)
    stdout = result.communicate()
    assert "Schema1:3:11  # Creating 1 schema with name `Schema1` with 3 tables and 11 rows in every table" \
           in str(stdout)

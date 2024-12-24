# Record any change to the project apart from private folder

---

1. Install `dnspython`
- run `pip install dnspython` in (.venv)
- add "dnspython" in `pyproject.toml`

2. Update paht in `default.yaml`
- add `parquet_store: '/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet'`

3. Add `data/parquet` to `gitignore`

4. Add `project_env.sh` for automation

5. Add `sysproduction/linux/my_crontab` for automation

6. Add `project.script` in `pyproject.toml` 

7. Setup `private-pysystemtrade` repo. 

Modified

1 . Change path in `sysdata/csv/csv_roll_parameters.py`
2 . Change path in `sysinit`

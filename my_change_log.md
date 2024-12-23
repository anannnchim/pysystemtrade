# Record any change to the project apart from private folder

---

1. Install `dnspython`
- run `pip install dnspython` in (.venv)
- add "dnspython" in `pyproject.toml`

2. Update paht in `default.yaml`
- add `parquet_store: '/Users/nanthawat/PycharmProjects/private-pysystemtrade/data/parquet'`

3. Add `data/parquet` to `gitignore`

4. Add `project_env.sh` for automation

5. Add `sysproduction/mac` for automation
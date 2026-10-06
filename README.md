# config-drift-detect

把多个来源的配置（`source,key,value` 的 CSV）合并起来，找出取值对不上的键，渲染成对齐表格。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m driftdetect report --csv conf.csv --source dev --source staging
python3 -m driftdetect demo --name onlyone
python3 -m driftdetect demo --name dup
python3 -m driftdetect demo --name emptymissing
python3 -m driftdetect demo --name space
python3 -m driftdetect demo --name work
```

## 口径

- **键集合**：所有来源里出现过的键都要参与比对，不只看某一个来源。
- **漂移**：一个键在各来源上的取值（缺失也算一种取值）不完全相同时算漂移。
- **来源内重复**：同一个来源里同一个键出现两行不同取值，按漂移处理。
- **取值比较**：比较前去掉两端空白；缺失与空串是两种不同取值。

## 不变量

- 每一行代表一个漂移的键，缺失的来源显示为 `<missing>`。
- 表格列按来源名排序，行按键排序，列宽对齐。
- `scanned` 不随键数平方级放大：两千个键的 `scanned` 不超过 6000。

## 输出契约

渲染成对齐表格：首行 `key | <来源...>`，次行分隔线，随后每个漂移键一行，
末行 `drift=<漂移键数>`。`--demo --name=work` 只打印 `{"keys": N, "scanned": N}`。

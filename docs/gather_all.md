## gather all命令

该命令用户收集集群的日志、observer所在主机的信息以及observer的堆栈信息

例子：
```shell script
 $ obdiag gather all -h
usage: obdiag gather all [-h] [--from datetime datetime] [--to datetime datetime] [--since 'n'<m|h|d>] [--store_dir store_dir] [-c config] [--scope scope]
                           [--encrypt encrypt] [--grep grep [grep ...]]

According to the input parameters, gather all reports

optional arguments:
  -h, --help            show this help message and exit
  --from datetime datetime
                        specify the start of the time range. format: yyyy-mm-dd hh:mm:ss.
  --to datetime datetime
                        specify the end of the time range. format: yyyy-mm-dd hh:mm:ss.
  --since 'n'<m|h|d>    Specify time range that from 'n' [d]ays, 'n' [h]ours or 'n' [m]inutes. before to now. format: <n> <m|h|d>. example: 1h.
  --store_dir store_dir
                        the dir to store gather result, current dir by default.
  -c config             obdiag custom config
  --scope scope         log type constrains, choices=[observer, election, rootservice, all], default=all
  --encrypt encrypt     Whether the returned results need to be encrypted, choices=[true, false], default=false
  --grep grep [grep ...]
                        specify keywords constrain for log

Example: obdiag gather all --from 2022-06-16 18:25:00 --to 2022-06-16 18:30:00
```

例子：
```shell script

 $ obdiag gather all --from 2022-07-28 16:25:00 --to 2022-07-28 18:30:00 --cluster_name test --encrypt true

...
ZipFileInfo:
+---------------+-----------+
| Node          | LogSize   |
+===============+===========+
| 192.168.2.11  | 29.874M   |
+---------------+-----------+
...

ZipFileInfo:
+----------------+-----------+
| Node           | LogSize   |
+================+===========+
| 192.168.2.12  | 143.229M  |
+----------------+-----------+
...


...
# 指定时间段内日志收集汇总
Summary:
+----------------+-----------+----------+------------------+--------+------------------------------------------------------------------------------------+
| Node           | Status    | Size     | Password         | Time   | PackPath                                                                           |
+================+===========+==========+==================+========+====================================================================================+
| 192.168.2.11   | Completed | 29.874M  | fB7FrrzTGl4EK5Hl | 20 s   | gather_pack_20220729170718/result_192.168.2.11_20220729222724_20220730003224.zip   |
+----------------+-----------+----------+------------------+--------+------------------------------------------------------------------------------------+
| 192.168.2.12   | Completed | 143.229M | SGRbXvMyA7lrnFW1 | 74 s   | gather_pack_20220729170718/result_192.168.2.12_20220729222724_20220730003224.zip   |
+----------------+-----------+----------+------------------+--------+------------------------------------------------------------------------------------+

...

# observer所在主机当前时间的主机信息收集汇总
Summary:
+----------------+-----------+---------+--------+----------------------------------------------------------------------+
| Node           | Status    | Size    | Time   | PackPath                                                             |
+================+===========+=========+========+======================================================================+
| 192.168.2.11   | Completed | 45.276K | 5 s    | gather_pack_20220729170856/sysstat_192.168.2.11_20220729170856.zip   |
+----------------+-----------+---------+--------+----------------------------------------------------------------------+
| 192.168.2.12   | Completed | 42.152K | 6 s    | gather_pack_20220729170856/sysstat_192.168.2.12_20220729170856.zip   |
+----------------+-----------+---------+--------+----------------------------------------------------------------------+

Gather Perf Summary:
+----------------+-----------+----------+--------+-------------------------------------------------------------------+
| Node           | Status    | Size     | Time   | PackPath                                                          |
+================+===========+==========+========+===================================================================+
| 192.168.2.11   | Completed | 368.178K | 90 s   | gather_pack_20230117140836/perf_192.168.2.11_20230117140836.zip   |
+----------------+-----------+----------+--------+-------------------------------------------------------------------+
| 192.168.2.12   | Completed | 368.178K | 90 s   | gather_pack_20230117140836/perf_192.168.2.12_20230117140836.zip   |
+----------------+-----------+----------+--------+-------------------------------------------------------------------+


```

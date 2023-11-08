************* Module run
run.py:99:38: C0303: Trailing whitespace (trailing-whitespace)
run.py:129:70: C0303: Trailing whitespace (trailing-whitespace)
run.py:137:0: C0301: Line too long (104/100) (line-too-long)
run.py:140:0: C0301: Line too long (110/100) (line-too-long
run.py:141:19: C0303: Trailing whitespace (trailing-whitespace)
run.py:185:0: C0303: Trailing whitespace (trailing-whitespace)
run.py:55:5: W0511: TODO: find alternative to global variable here (fixme)
run.py:247:1: W0511: TODO: find alternative way to display cart here (fixme)
run.py:56:4: W0603: Using the global statement (global-statement)
run.py:248:4: W0106: Expression "[print(*x) for x in CART_DISPLAY]" is assigned to nothing (expression-not-assigned)
run.py:290:8: W0106: Expression "[print(*x) for x in CART_DISPLAY]" is assigned to nothing (expression-not-assigned)


Report
======
176 statements analysed.

Statistics by type
------------------

+---------+-------+-----------+-----------+------------+---------+
|type     |number |old number |difference |%documented |%badname |
+=========+=======+===========+===========+============+=========+
|module   |1      |1          |=          |100.00      |0.00     |
+---------+-------+-----------+-----------+------------+---------+
|class    |1      |1          |=          |100.00      |0.00     |
+---------+-------+-----------+-----------+------------+---------+
|method   |1      |1          |=          |100.00      |0.00     |
+---------+-------+-----------+-----------+------------+---------+
|function |15     |15         |=          |100.00      |0.00     |
+---------+-------+-----------+-----------+------------+---------+



External dependencies
---------------------
::

    google 
      \-oauth2 
        \-service_account (run)
    gspread (run)
    pyfiglet (run)
    tabulate (run)
    termcolor (run)



361 lines have been analyzed

Raw metrics
-----------

+----------+-------+------+---------+-----------+
|type      |number |%     |previous |difference |
+==========+=======+======+=========+===========+
|code      |190    |52.63 |191      |-1.00      |
+----------+-------+------+---------+-----------+
|docstring |86     |23.82 |80       |+6.00      |
+----------+-------+------+---------+-----------+
|comment   |33     |9.14  |30       |+3.00      |
+----------+-------+------+---------+-----------+
|empty     |52     |14.40 |63       |-11.00     |
+----------+-------+------+---------+-----------+



Duplication
-----------

+-------------------------+------+---------+-----------+
|                         |now   |previous |difference |
+=========================+======+=========+===========+
|nb duplicated lines      |0     |0        |0          |
+-------------------------+------+---------+-----------+
|percent duplicated lines |0.000 |0.000    |=          |
+-------------------------+------+---------+-----------+



Messages by category
--------------------

+-----------+-------+---------+-----------+
|type       |number |previous |difference |
+===========+=======+=========+===========+
|convention |6      |19       |19         |
+-----------+-------+---------+-----------+
|refactor   |0      |3        |3          |
+-----------+-------+---------+-----------+
|warning    |5      |7        |7          |
+-----------+-------+---------+-----------+
|error      |0      |0        |0          |
+-----------+-------+---------+-----------+



Messages
--------

+------------------------+------------+
|message id              |occurrences |
+========================+============+
|trailing-whitespace     |4           |
+------------------------+------------+
|line-too-long           |2           |
+------------------------+------------+
|fixme                   |2           |
+------------------------+------------+
|expression-not-assigned |2           |
+------------------------+------------+
|global-statement        |1           |
+------------------------+------------+




------------------------------------------------------------------
Your code has been rated at 9.38/10 (previous run: 8.35/10, +1.02)


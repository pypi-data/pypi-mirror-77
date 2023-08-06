# ipython-kusto - Run Microsoft Kusto queries in IPython notebooks

This extension borrows extensively from Catherine Devlin's ipython-sql extension.
https://github.com/catherinedevlin/ipython-sql

It provides two magics:

- %kqlset - a line magic to set the default cluster and database
- %kql/%%kql - a line or cell magic to execute Kusto Query Language queries and return the results as a Pandas dataframe. The dataframe will be assigned to a variable 'kqlresult' (can be overridden with --set argument)

If you run either of these followed by a '?' you will get additional help.

When running a query, you may be redirected to a browser page to sign in if a token is needed.

See the example notebook in the examples/ directory for more details.

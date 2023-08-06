connectwrap

A Python package built on top of the sqlite3 module made specifically for SQLite database management & object relational mapping.

Make sure to have the latest version of Python 3 installed although this should work with previous versions.  

To install the package with pip enter command in terminal:
    pip install connectwrap

To uninstall the package with pip enter command in terminal:
    pip uninstall connectwrap

---------
Module db
---------

db_filepath: 	                        Attribute of the string type representing the database file path.
                                            The file must have a .db, .sqlite, or .sqlite3 extension.

db_table:                               Attribute of the string type representing a table within the database. 

connection: 	                        Attribute of the Connection type from the sqlite3 module representing the database connection. Used to commit changes to database.

connection_cursor: 	                    Attribute of the Cursor type from the sqlite3 module representing the database connection cursor. Used to execute queries.

connection_status: 	                    Attribute of the bool type representing whether the Database connection is opened or closed.
                                            Set to True upon the creation of a new Database object.
                                            Opened = True
                                            Closed = False

DatabaseOpenError: 	                    Custom exception to raise when the Database is open.

DatabaseNotOpenError: 	                Custom exception to raise when the Database is not open.

TableNotFoundError: 	                Custom exception to raise when an argument table doesn't exist in a database.

TableExistsError: 	                    Custom exception to raise when an argument table already exists in a database.

execute(query): 	                    Execute a custom query. The query argument must be a string.

commit(): 	                            Commit a query held in the connection cursor. 

close_db(): 	                        Close database connection.

open_db(): 	                            Open database connection. Reset the cursor.

set_db_filepath(db_filepath): 	        Change the db_filepath attribute value.
                                            The file must have a .db, .sqlite, or .sqlite3 extension.
                                            This allows you to switch between file databases while only creating one object.
                                            Works on open or closed databases. The result of this method will be an open Database using the db_filepath argument as the new Database file path.

set_db_table(db_table):                 Change the db_table attribute value.

get_connection_status(): 	            Return the connection_status attribute representing whether the Database connection is open or closed.
                                            Opened = True
                                            Closed = False

get_db_filepath(): 	                    Return the db_filepath attribute value representing the database file path.

get_db_table():                         Return the db_table attribute value.

get_tablenames(): 	                    Select and return the table names within a database as strings in a list.

get_keys(): 	                        Select and return the key names within the db_table attribute table as strings in a list. 

get_column(key): 	                    Select and return a list of the values in a column within the db_table attribute table based on the key from that column.

get_row(key, value): 	                Select and return a dictionary representing a row in the db_table attribute table where the key and value arguments match a row column key and value pair. 
                                            Only returns the first row with the occurance of the key/value argument pair.
                                            Returns None if there's no occurance of the key/value argument in any row in the table.
                                            The key argument must be a string and a key within the table.
                                            The value argument must be one of the following types - int, float, str, bytes, None.

get_table(): 	                        Select and return a list of dictionaries with each dictionary representing a row in the db_table attribute table.

rename_table(old_table_name, new_table_name): 	    Rename a table.

drop_table(table): 	                                Drop/delete table in the file database.

drop_row(key, value): 	                Drop/delete rows within the db_table attribute table with matching key & value. 
                                            The key argument must be a string and a key within the table.
                                            The value argument must be one of the following types - int, float, str, bytes, None.

create_table(table, **kwargs): 	        Create table within the file database.
                                            The key in each kwargs entry denotes the key name of a column.
                                            The value in each kwargs entry denotes the data type of a column.
                                            The value in each kwargs entry must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.

create_column(column, datatype): 	    Create a new column within the db_table attribute table. 
                                            The datatype argument must be one of the following strings - 'int', 'float', 'str', 'bytes', 'None'.

select_tablenames(): 	                Select and output to terminal the table names within a database.

select_table(): 	                    Select and output to terminal the rows from the db_table attribute table. 

select_column(*args): 	                Select and output to terminal the values from keys within the db_table attribute table. 
                                            Each arg in *args arguments must be strings containing key names within the table.

select_keys(): 	                        Select and output to terminal the key names within the db_table attribute table.

select_row(key, value): 	            Select and output to terminal a row in the db_table attribute table. 
                                            Only outputs the first row with the occurance of the key/value argument pair.
                                            Outputs None if there's no occurance of the key/value argument in any row in the table.
                                            The key argument must be a string and a key within the table.
                                            The value argument must be one of the following types - int, float, str, bytes, None.

insert_row(*args): 	                    Insert a row of data into the db_table attribute table.
                                            Each arg in *args must be one of the following types - int, float, str, bytes, None.

update_row(change_key, change_value, check_key, check_value): 	Update/change row column values within the db_table attribute table. 
                                                                    The key arguments must be strings and keys within the table.
                                                                    The value arguments must be one of the following types - int, float, str, bytes, None.

key_exists(key): 	                    Return True if the key argument exists in the db_table attribute table.

table_exists(table): 	                Return True if the table argument is a table name within the database. 

------------
Module utils
------------

drop_database(db_filepath): 	    Drop/delete .db, .sqlite, or .sqlite3 file database.

create_database(db_filepath): 	    Create .db, .sqlite, or .sqlite3 file database.

ishex(arg): 	                    Return True if all characters in arg string are hexadecimal.

isfloat(arg): 	                    Return True if arg string characters constitute a float.

isdb(db_filepath): 	                Return True if db_filepath argument has one of the follow extensions: .db, .sqlite, or .sqlite3 
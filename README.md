# Manage your emails with Python 
The `pydatamail` is a python module to apply data science principles to email processing. It stores the emails in an 
`SQL` database and generates `pandas.DataFrame` objects for futher processing and plotting.

# Installation 
Install the `pydatamail` package from github using `pip`:
```
pip install git+https://github.com/pyscioffice/pydatamail.git
```

# Python interface 
Import the `pygmailfiler` module 
```
from pydatamail DatabaseInterface, get_from_pie_plot, get_labels_pie_plot, get_number_of_email_plot, Message, email_date_converter
```

The individual components are briefly explained below: 

* `DatabaseInterface` - `SQLalchemy` based interface for `SQL` database to store emails
* `get_from_pie_plot` - plot a pie chart of the distribution of emails senders
* `get_labels_pie_plot` - plot a pie chart of the distribution of email labels
* `get_number_of_email_plot` - plot the number of incoming emails over time
* `Message` - abstract class to implement `pydatamail` compatible email adapters
* `email_date_converter` - convert the email date to python `datetime` dates. 

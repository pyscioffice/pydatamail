from pydatamail.database import get_email_database, DatabaseTemplate
from pydatamail.plots import (
    get_from_pie_plot,
    get_labels_pie_plot,
    get_number_of_email_plot,
)
from pydatamail.message import Message, email_date_converter
from pydatamail.machinelearning import (
    one_hot_encoding,
    get_machine_learning_database,
    gather_data_for_machine_learning,
    train_model,
    get_machine_learning_recommendations,
)

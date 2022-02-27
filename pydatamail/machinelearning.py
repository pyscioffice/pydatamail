import pandas
import pickle
from sklearn.ensemble import RandomForestRegressor
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydatamail.database import DatabaseTemplate


Base = declarative_base()


class MachineLearningLabels(Base):
    __tablename__ = "ml_labels"
    id = Column(Integer, primary_key=True)
    label_id = Column(String)
    random_forest = Column(String)
    user_id = Column(Integer)


class MachineLearningDatabase(DatabaseTemplate):
    def store_models(self, model_dict, user_id=1, commit=True):
        label_lst = (
            self._session.query(MachineLearningLabels.label_id)
            .filter(MachineLearningLabels.user_id == user_id)
            .all()
        )
        model_dict_new = {k: v for k, v in model_dict.items() if k not in label_lst}
        model_dict_update = {k: v for k, v in model_dict.items() if k in label_lst}
        model_delete_lst = [
            label for label in label_lst if label not in model_dict.keys()
        ]
        if len(model_dict_new) > 0:
            self._session.add_all(
                [
                    MachineLearningLabels(
                        label_id=k, random_forest=pickle.dumps(v), user_id=user_id
                    )
                ]
                for k, v in model_dict_new.items()
            )
        if len(model_dict_update) > 0:
            label_obj_lst = (
                self._session.query(MachineLearningLabels)
                .filter(MachineLearningLabels.user_id == user_id)
                .filter(
                    MachineLearningLabels.label_id.in_(list(model_dict_update.keys()))
                )
                .all()
            )
            for label_obj in label_obj_lst:
                label_obj.random_forest = pickle.dumps(
                    model_dict_update[label_obj.label_id]
                )
        if len(model_delete_lst) > 0:
            self._session.query(MachineLearningLabels).filter(
                MachineLearningLabels.user_id == user_id
            ).filter(MachineLearningLabels.label_id.in_(model_delete_lst)).delete()
        if commit:
            self._session.commit()

    def load_models(self, user_id=1):
        label_obj_lst = (
            self._session.query(MachineLearningLabels)
            .filter(MachineLearningLabels.user_id == user_id)
            .all()
        )
        return {
            label_obj.label_id: pickle.loads(label_obj.random_forest)
            for label_obj in label_obj_lst
        }


def _build_red_lst(df_column):
    collect_lst = []
    for lst in df_column:
        for entry in lst:
            collect_lst.append(entry)
    return list(set(collect_lst))


def _single_entry_df(df, red_lst, column):
    return [
        {
            column + "_" + red_entry: 1 if email == red_entry else 0
            for red_entry in red_lst
            if red_entry is not None
        }
        for email in df[column].values
    ]


def _list_entry_df(df, red_lst, column):
    return [
        {
            column + "_" + red_entry: 1 if red_entry in email else 0
            for red_entry in red_lst
        }
        for email in df[column].values
    ]


def _merge_dicts(email_id, label_dict, cc_dict, from_dict, threads_dict, to_dict):
    email_dict = {"email_id": email_id}
    email_dict.update(label_dict)
    email_dict.update(cc_dict)
    email_dict.update(from_dict)
    email_dict.update(threads_dict)
    email_dict.update(to_dict)
    return email_dict


def one_hot_encoding(df):
    dict_labels_lst = _list_entry_df(
        df=df, red_lst=_build_red_lst(df_column=df.labels.values), column="labels"
    )
    dict_cc_lst = _list_entry_df(
        df=df, red_lst=_build_red_lst(df_column=df.cc.values), column="cc"
    )
    dict_from_lst = _single_entry_df(df=df, red_lst=df["from"].unique(), column="from")
    dict_threads_lst = _single_entry_df(
        df=df, red_lst=df["threads"].unique(), column="threads"
    )
    dict_to_lst = _list_entry_df(
        df=df, red_lst=_build_red_lst(df_column=df.to.values), column="to"
    )
    return pandas.DataFrame(
        [
            _merge_dicts(
                email_id=email_id,
                label_dict=label_dict,
                cc_dict=cc_dict,
                from_dict=from_dict,
                threads_dict=threads_dict,
                to_dict=to_dict,
            )
            for email_id, label_dict, cc_dict, from_dict, threads_dict, to_dict in zip(
                df.id.values,
                dict_labels_lst,
                dict_cc_lst,
                dict_from_lst,
                dict_threads_lst,
                dict_to_lst,
            )
        ]
    )


def get_training_input(df):
    return df.drop(
        [c for c in df.columns.values if "labels_" in c] + ["email_id"], axis=1
    )


def train_randomforest(df_in, results, n_estimators=1000, random_state=42):
    return RandomForestRegressor(
        n_estimators=n_estimators, random_state=random_state
    ).fit(df_in, results)

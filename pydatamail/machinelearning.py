import pandas


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

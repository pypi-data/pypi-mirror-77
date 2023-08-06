# DLtorch Framework
# Author: Junbo Zhao <zhaojb17@mails.tsinghua.edu.cn>.

import DLtorch.datasets

def get_dataset_cls(_type):
    # Get a dataset from DLtorch framework without initialization.
    return getattr(DLtorch.datasets, _type)

def get_dataset(_type, **kwargs):
    # Get a dataset from DLtorch framework.
    return get_dataset_cls(_type)(**kwargs)

def get_dataset_attrs():
    # Get all the dataset types.
    # Used in "main.components".
    attrs = list(DLtorch.datasets.__dict__.keys())
    start_idx = attrs.index("base_dataset")
    return list(DLtorch.datasets.__dict__.keys())[start_idx + 1:]
# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains utility classes and functions for the package."""

import numpy as np
import pkg_resources
from skmultilearn.model_selection import iterative_train_test_split
from sklearn.model_selection import train_test_split
import torch
import os
from azureml.core.conda_dependencies import CondaDependencies
from azureml.automl.core.shared.exceptions import ClientException

from ..common.constants import PackageInfo


class _CondaUtils:

    @staticmethod
    def _all_dependencies():
        """Retrieve the packages from the site-packages folder by using pkg_resources.

        :return: A dict contains packages and their corresponding versions.
        """
        dependencies_versions = dict()
        for d in pkg_resources.working_set:
            dependencies_versions[d.key] = d.version
        return dependencies_versions

    @staticmethod
    def get_conda_dependencies():
        dependencies = _CondaUtils._all_dependencies()
        conda_packages = []
        pip_packages = []
        for package_name in PackageInfo.PIP_PACKAGE_NAMES:
            pip_packages.append('{}=={}'.format(package_name, dependencies[package_name]))

        for package_name in PackageInfo.CONDA_PACKAGE_NAMES:
            conda_packages.append('{}=={}'.format(package_name, dependencies[package_name]))

        cd = CondaDependencies.create(pip_packages=pip_packages, conda_packages=conda_packages,
                                      python_version=PackageInfo.PYTHON_VERSION)

        return cd


def _split_train_val(dataset_wrapper, test_size=0.2, multilabel=False):
    """Split dataset into training and validation.

    :param dataset_wrapper: input dataset wrapper
    :type dataset_wrapper: azureml.contrib.automl.dnn.vision.io.read.dataset_wrappers.BaseDatasetWrapper
    :param test_size: ratio of input data to be put in validation
    :type test_size: float
    :param multilabel: whether input is multilabel
    :type multilabel: bool
    :return: tuple of numpy arrays containing indices
    :rtype: tuple[numpy.array, numpy.array]
    """
    indices = np.arange(len(dataset_wrapper))
    if multilabel:
        y = np.zeros((len(dataset_wrapper), dataset_wrapper.num_classes))
        for i in indices:
            label_indices = [dataset_wrapper.label_to_index_map[l] for l in dataset_wrapper.label_at_index(i)]
            y[i, label_indices] = 1
        indices = indices.reshape(-1, 1)
        indices_train, _, indices_test, _ = iterative_train_test_split(indices, y, test_size=test_size)
        indices_train = indices_train.squeeze(1)
        indices_test = indices_test.squeeze(1)
    else:
        y = np.zeros(len(dataset_wrapper))
        for i in indices:
            y[i] = dataset_wrapper.label_to_index_map[dataset_wrapper.label_at_index(i)]
        # try to get a stratified split. If that fails, get a normal split
        try:
            indices_train, indices_test, _, _ = train_test_split(indices, y, test_size=test_size, stratify=y)
        except:
            indices_train, indices_test, _, _ = train_test_split(indices, y, test_size=test_size)

    return indices_train.astype(int), indices_test.astype(int)


def _gen_validfile_from_trainfile(train_file, val_size=0.2, output_dir=None):
    """Split dataset into training and validation.

    :param train_file: full path for train file
    :type train_file: str
    :param val_size: ratio of input data to be put in validation
    :type val_size: float
    :param output_dir: where to save train and val files
    :type output_dir: str
    :return: full path for train and validation
    :rtype: str
    """
    os.makedirs(output_dir, exist_ok=True)

    lines = []
    num_lines = 0
    with open(train_file, "r") as f:
        for line in f:
            lines.append(line.strip())
            num_lines += 1

    indices = np.arange(num_lines)
    x_train, x_test, _, _ = train_test_split(indices, lines, test_size=val_size)

    new_train_file = os.path.join(output_dir, 'train_sub.csv')
    new_valid_file = os.path.join(output_dir, 'val_sub.csv')

    newline = '\n'
    with open(new_train_file, "w") as f1:
        for idx in x_train:
            f1.write(lines[idx] + newline)

    with open(new_valid_file, "w") as f2:
        for idx in x_test:
            f2.write(lines[idx] + newline)

    return new_train_file, new_valid_file


def _get_model_params(model, model_name=None):
    """Separate learnable model params into three groups (the last, the rest (except batchnorm layers), and batchnorm)
    to apply different training configurations.

    :param model: model class
    :type model object
    :param model_name: current network name
    :type str
    :return: groups of model params
    :rtype: lists
    """
    if model_name is None:
        raise ClientException('model_name cannot be None', has_pii=False)

    inception_last_layers = ['AuxLogits.', 'fc.']
    seresnext_last_layers = ['last_linear']
    models_last_layers = ['fc.']

    model_to_layers = {'inception': inception_last_layers, 'seresnext': seresnext_last_layers}

    last_layer_names = model_to_layers.get(model_name, models_last_layers)

    rest_params = []
    last_layer_params = []
    batchnorm_params = []

    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if any(map(lambda x: name.startswith(x), last_layer_names)):
            last_layer_params.append(param)
        else:
            if 'bn' in name:
                batchnorm_params.append(param)
            else:
                rest_params.append(param)

    return last_layer_params, rest_params, batchnorm_params


def _get_default_device_name():
    return "cuda:0" if torch.cuda.is_available() else "cpu"

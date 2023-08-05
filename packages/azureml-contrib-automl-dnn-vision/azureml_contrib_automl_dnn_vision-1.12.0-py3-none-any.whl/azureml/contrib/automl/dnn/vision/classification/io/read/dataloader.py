# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains dataloader functions for the package."""
from azureml.automl.core.shared.exceptions import ClientException

try:
    import torch
    from torch.utils.data.dataloader import default_collate
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')

import collections
from ....common.dataloaders import RobustDataLoader


def _one_hot_encode(label_list, num_classes=None):
    if num_classes is None:
        raise ClientException('num classes needs to be passed', has_pii=False)
    one_hot_label = torch.zeros(num_classes)
    one_hot_label[label_list] = 1

    return one_hot_label


class _CollateFn:
    def __init__(self, f, multilabel=False, num_classes=None):
        """Collate function for the dataloader that performs transformations on dataset input. Since pytorch
        multiprocessing needs to pickle objects, we could not have nested functions.
        Therefore this ends up as a class.

        :param f: function that takes in a pillow image and returns a torch Tensor.
        :type f: function
        :param multilabel: whether this is a multilabel dataset
        :type multilabel: bool
        :param num_classes: number of classes
        :type num_classes: int
        :return: function that can take a batch of tuples of pillow images and labels and returns tensors of
        transformed
        images and the label.
        :rtype: function
        """
        if multilabel and num_classes is None:
            raise ClientException('num_classes needs to be set if multilabel is True', has_pii=False)
        self._multilabel = multilabel
        self._num_classes = num_classes
        self._func = f

    def __call__(self, x):
        batch = []
        for im, label in x:
            if self._multilabel:
                label = _one_hot_encode(label, num_classes=self._num_classes)
            batch.append((self._func(im), label))

        return default_collate(batch)


def _get_data_loader(dataset_wrapper, is_train=False, transform_fn=None, batch_size=None,
                     oversample=False, num_workers=None):
    """Get data loader for the torch dataset only loading the selected indices and transforming the input images using
    transform_fn.

    :param dataset_wrapper: dataset wrapper
    :type dataset_wrapper: azureml.contrib.automl.dnn.vision.io.read.dataset_wrapper.BaseDatasetWrapper
    :param is_train: is this data for training
    :type is_train: bool
    :param transform_fn: function that takes a pillow image and returns a torch Tensor
    :type transform_fn: function
    :param batch_size: batch size for dataloader
    :type batch_size: int
    :param oversample: enable oversampling
    :type oversample: bool
    :param num_workers: num workers for dataloader
    :type num_workers: int
    :return: dataloader
    :rtype: torch.utils.data.DataLoader
    """
    if transform_fn is None:
        transform_fn = _identity

    collate_fn = _CollateFn(transform_fn, multilabel=dataset_wrapper.multilabel,
                            num_classes=dataset_wrapper.num_classes)

    if oversample and is_train:
        # it should be either oversampling or CE w/ weights or Focal loss
        samples_weights = _make_weights_for_imbalanced_classes(dataset_wrapper)
        sampler = torch.utils.data.sampler.WeightedRandomSampler(samples_weights, len(samples_weights))
        return RobustDataLoader(dataset_wrapper, batch_size=batch_size, sampler=sampler,
                                collate_fn=collate_fn, num_workers=num_workers)
    else:
        return RobustDataLoader(dataset_wrapper, batch_size=batch_size, shuffle=is_train,
                                collate_fn=collate_fn, num_workers=num_workers)


def _identity(x):
    """
    :param x: any input
    :type x: any type
    :return: return the input
    :rtype: any type
    """
    return x


def _make_weights_for_imbalanced_classes(dataset_wrapper):
    """Allow get samples elements with given probabilities (samples_weights)

    :param dataset_wrapper: dataset wrapper
    :type dataset_wrapper: azureml.contrib.automl.dnn.vision.io.read.dataset_wrapper.BaseDatasetWrapper
    :return: weights for samples
    :rtype: list
    """
    images = dataset_wrapper._CommonImageDatasetWrapper__files_to_labels_dict
    class_counts = collections.defaultdict(int)
    data_targets = []
    for key in images:
        label = images[key]
        class_counts[label] += 1
        data_targets.append(label)

    samples_weights = [1.0 / class_counts[class_label] for class_label in data_targets]
    return samples_weights

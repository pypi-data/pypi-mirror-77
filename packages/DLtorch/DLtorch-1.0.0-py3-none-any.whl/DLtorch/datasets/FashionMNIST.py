# DLtorch Framework
# Author: Junbo Zhao <zhaojb17@mails.tsinghua.edu.cn>.

import torchvision.transforms as transforms
import torchvision.datasets as datasets

from DLtorch.datasets.base import base_dataset

class FashionMNIST(base_dataset):
    NAME = "FashionMNIST"

    def __init__(self, dir, train_transform=None, test_transform=None, whether_valid=False, portion=None):
        super(FashionMNIST, self).__init__(datatype="image", whether_valid=whether_valid, portion=portion)
        self.dir = dir
        self.train_transform = train_transform if train_transform is not None else \
            transforms.Compose([transforms.ToTensor()])
        self.test_transform = test_transform if test_transform is not None else \
            transforms.Compose([transforms.ToTensor()])
        self.datasets["train"] = datasets.FashionMNIST(root=self.dir, train=True, download=True, transform=self.train_transform)
        self.datasets["test"] = datasets.FashionMNIST(root=self.dir, train=False, download=True, transform=self.test_transform)
        self.datalength["train"] = len(self.datasets["train"])
        self.datalength["test"] = len(self.datasets["test"])
        if self.whether_valid:
            self.devide()
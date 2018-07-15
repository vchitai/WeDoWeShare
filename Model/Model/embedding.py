import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import time
import os
import copy
import pandas as pd


class EmbeddingWrapper():

    def __init__(self, data_path, mentor_path, n_cont=0, emb_drop=0,
                 out_sz=1, szs = [1024,512], drops = [0.3,0.2], use_bn = 0):

        self._batch_size = 64
        self._lr = 0.001
        self._num_epochs = 2

        self.load_data(data_path)
        self.load_mentors(mentor_path)
        self._model = self.EmbeddingNet(self._emb_szs, n_cont, emb_drop = emb_drop,
                                        out_sz=out_sz, szs = szs, drops=drops, use_bn=use_bn)
        self._optimizer = optim.RMSprop(self._model.parameters(), lr = self._lr)
        self._criterion = nn.MSELoss()

    def load_mentors(self, mentor_path):
        mentor = pd.read_csv('./data/mentor.csv', header=None)
        self._mentor = mentor.values

    def load_data(self, data_path):
        df = pd.read_csv(data_path, header=None)

        b = np.array([np.max(df.values[:, i]) for i in range(df.values.shape[1]-1)], dtype=int)
        self._emb_szs = [(len(set(df.values[:, i])) + int(b[i] + 1), 32)
                         for i in range(df.values.shape[1]-1)]

        self._train_data = np.array(df.values[:, :-1])
        self._label_data = np.array(df.values[:, -1]).reshape(-1,1)
        self._test_data = df.values[:500][:-1]

        self.numpy_to_loader()

    def numpy_to_loader(self):

        self._train_tensor = torch.from_numpy(self._train_data).long()

        self._label_tensor = torch.from_numpy(self._label_data).float()
        self._train_dataset = torch.utils.data.TensorDataset(self._train_tensor, self._label_tensor)
        self._label_dataset = torch.utils.data.TensorDataset(self._label_tensor)
        self._test_tensor = torch.from_numpy(self._test_data).long()
        self._test_dataset = torch.utils.data.TensorDataset(self._test_tensor)

        self._train_loader = torch.utils.data.DataLoader(
            dataset=self._train_dataset, batch_size=self._batch_size, shuffle=True)
        self._test_loader = torch.utils.data.DataLoader(
            dataset=self._test_dataset, batch_size=self._batch_size, shuffle=False)
        self._label_loader = torch.utils.data.DataLoader(
            dataset=self._label_dataset, batch_size=self._batch_size, shuffle=False)

    class EmbeddingNet(nn.Module):
        def emb_init(self, x):
            x = x.weight.data
            sc = 2 / (x.size(1) + 1)
            x.uniform_(-sc, sc)

        def __init__(self, emb_szs, n_cont, emb_drop, out_sz, szs,
                     drops, use_bn=0):
            super().__init__()

            self.embs = nn.ModuleList([nn.Embedding(c, s) for c, s in emb_szs])
            # for emb in self.embs: emb.weight.data.uniform_(-0.01,0.01)
            for emb in self.embs: self.emb_init(emb)

            n_emb = sum(e.embedding_dim for e in self.embs)

            szs = [n_emb + n_cont] + szs

            self.lins = nn.ModuleList([nn.Linear(szs[i], szs[i + 1])
                                       for i in range(len(szs) - 1)])
            self.bns = nn.ModuleList([nn.BatchNorm1d(sz) for sz in szs[1:]])
            self.outp = nn.Linear(szs[-1], out_sz)
            self.emb_drop = nn.Dropout(emb_drop)

            self.drops = nn.ModuleList([nn.Dropout(drop) for drop in drops])
            # self.bn_cont = nn.BatchNorm1d(n_cont)
            self.use_bn = use_bn


        def forward(self, x_cat):

            x = [e.weight.data[x_cat[:, i]] for i, e in enumerate(self.embs)]
            x = torch.cat(x, 1)
            # x2 = self.bn(x_cont)
            x = self.emb_drop(x)
            # x.torch.cat([x,x2], 1)

            for l, d, b in zip(self.lins, self.drops, self.bns):
                x = nn.functional.relu(l(x))
                if self.use_bn:
                    x = b(x)
                x = d(x)
            x = self.outp(x)
            return x

    def train_new_batch(self, new_batch, new_label):

        self._train_data = np.vstack((self._train_data, new_batch))
        self._label_data = np.vstack((self._label_data, new_label))

        new_label = torch.from_numpy(new_label).float().reshape(-1, 1)
        new_batch = torch.from_numpy(new_batch).long().reshape(-1, self._train_data.shape[1])

        self._model.train()
        out = self._model(new_batch)
        loss = self._criterion(out, new_label)
        self._optimizer.zero_grad()
        loss.backward()
        self._optimizer.step()
        print('loss_new_batch: ', loss)

    def suggest(self, data, n = 5):

        data = np.array([list(data) + list(self._mentor[i]) for i in range(len(self._mentor))])
        self._model.eval()
        data = np.array(data)
        out = self._model(data)

        temp = np.array(out.data.reshape(-1))

        return self._mentor[temp.argsort()[-n:][::-1]]

    def train_all(self, num_epochs = 1):
        loss_avg = 0
        total_step = len(self._train_loader)
        self._model.train()
        for i in range(num_epochs):
            k = self._batch_size

            for j, (data, label) in enumerate(self._train_loader):

                label = label.float().reshape(-1, 1)
                out = self._model(data).reshape(-1, 1)

                # print(out.shape, type(data), type(label))

                loss = self._criterion(out, label)
                loss_avg += loss
                self._optimizer.zero_grad()
                loss.backward()
                self._optimizer.step()
                k += self._batch_size

                if (j + 1) % 100 == 0:
                    print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'
                          .format(i + 1, num_epochs, j + 1, total_step, loss.item()))

        loss_avg = loss_avg / (total_step * num_epochs)
        print('loss_avg: ', loss_avg)


    def save_model(self, model_path):
        torch.save(self._model.state_dict(), model_path)

    def load_model(self, model_path):
        self._model.load_state_dict(torch.load(model_path))
    def update_loaders(self):
        self.numpy_to_loader()

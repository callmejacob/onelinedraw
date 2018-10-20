# -*- coding: utf-8 -*-
import os;
import sys;

from skimage import data, io, filters
from skimage.filters import rank
from skimage.morphology import disk
from skimage.transform import rescale
from skimage import img_as_float
import numpy as np

def genmap(img_path, gray_path):
        img = data.load(img_path, True)
        img_sub = data.load(gray_path, True)

        ratio = 0.25
        img_down = rescale(img, ratio)
        img_down_sub = rescale(img_sub, ratio)

        w_sub, h_sub = img_down_sub.shape
        w_img, h_img = img_down.shape

        block_sub = img_down_sub.astype(np.float)
        ignore_i = 0
        cout_i = 0
        min_i = w_img
        max_i = 0
        min_j = h_img
        max_j = 0
        max_row = 0
        max_col = 0
        for i in range(w_img - w_sub):
                if ignore_i > 0:
                        ignore_i -= 1
                        continue
                min_err = 10000
                ignore_j = 0
                cout_j = 0
                for j in range(h_img - h_sub):
                        if ignore_j > 0:
                                ignore_j -= 1
                                continue
                        block_img = img_down[i:i+w_sub, j:j+h_sub].astype(np.float)
                        err = np.sum(np.power(block_img - block_sub, 2))
                        if err < 0.1:
                                ignore_j = h_sub
                                cout_j += 1
                                if j < min_j:
                                        min_j = j
                                if j > min_j:
                                        max_j = j
                                #print i, j, err
                        if err < min_err:
                                min_err = err
                if min_err < 0.1:
                        ignore_i = w_sub
                        cout_i += 1
                        if i < min_i:
                                min_i = i
                        if i > max_i:
                                max_i = i
                        #print cout_i, cout_j
                if cout_i > max_row:
                        max_row = cout_i
                if cout_j > max_col:
                        max_col = cout_j


        #print max_row, max_col, min_i, max_i, min_j, max_j


        edge_row = np.zeros(max_row, dtype=np.int)
        edge_col = np.zeros(max_col, dtype=np.int)

        edge_row[0] = min_i
        edge_row[max_row-1] = max_i

        index_i = 0
        ignore_i = 0
        for i in range(min_i, max_i, 1):
                if ignore_i > 0:
                        ignore_i -= 1
                        continue
                has_sub = False
                for j in range(min_j, max_j, 1):
                        block_img = img_down[i:i+w_sub, j:j+h_sub].astype(np.float)
                        err = np.sum(np.power(block_img - block_sub, 2))
                        if err < 0.1:
                                has_sub = True
                                break
                if has_sub:
                        ignore_i += w_sub
                        edge_row[index_i] = i
                        index_i += 1


        index_j = 0
        ignore_j = 0
        for j in range(min_j, max_j, 1):
                if ignore_j > 0:
                        ignore_j -= 1
                        continue
                has_sub = False
                for i in range(min_i, max_i, 1):
                        block_img = img_down[i:i+w_sub, j:j+h_sub].astype(np.float)
                        err = np.sum(np.power(block_img - block_sub, 2))
                        if err < 0.1:
                                has_sub = True
                                break
                if has_sub:
                        ignore_j += h_sub
                        edge_col[index_j] = j
                        index_j += 1


        pos = np.zeros(max_row * max_col * 2, dtype=np.int).reshape((max_row, max_col, 2))

        for i in range(max_row):
                for j in range(max_col):
                        pos[i,j,1] = int((edge_row[i] + w_sub/2)/ratio)
                        pos[i,j,0] = int((edge_col[j] + h_sub/2)/ratio)

        value = np.zeros(max_row * max_col, dtype=np.float).reshape((max_row, max_col))
        mean = np.zeros(max_row * max_col, dtype=np.float).reshape((max_row, max_col))
        for i in range(max_row):
                for j in range(max_col):
                        x = edge_row[i]
                        y = edge_col[j]
                        block_img = img_down[x:x+w_sub, y:y+h_sub].astype(np.float)
                        err = np.sum(np.power(block_img - block_sub, 2))
                        value[i,j] = err
                        mean[i,j] = np.mean(block_img)
        
        #print mean
        
        cat_i = 0
        cat_j = 0
        for i in range(max_row):
                for j in range(max_col):
                        if mean[i,j] > 0.97 and mean[i,j] < 0.98:
                                continue
                        elif value[i,j] < 5:
                                continue
                        else:
                                cat_i = i
                                cat_j = j
                                break

        map = np.zeros(max_row * max_col, dtype=np.int).reshape((max_row, max_col))
        for i in range(max_row):
                for j in range(max_col):
                        val = value[i,j]
                        if val < 5:
                                map[i,j] = 1
	map[cat_i,cat_j] = 1
        return max_row, max_col, cat_i, cat_j, map, pos


# for test
#max_row, max_col, cat_i, cat_j, map, pos = genmap('/Users/jacob/Desktop/model.png', '/Users/jacob/Desktop/gray_block.png')
#print max_row, max_col, cat_i, cat_j
#print map

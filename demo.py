#!/usr/env/bin python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import sys
import subprocess
import time
import os
import yaml
import matplotlib.pyplot as plot
import cv2

import chainer
from chainercv.utils import read_image
from chainercv.visualizations import vis_image
from chainercv.visualizations import vis_semantic_segmentation
from icnet.data_util.cityscapes.cityscapes_utils import cityscapes_label_colors
from icnet.data_util.cityscapes.cityscapes_utils import cityscapes_label_names
from icnet.config_utils import *

chainer.cuda.set_max_workspace_size(1024 * 1024 * 1024)
os.environ["CHAINER_TYPE_CHECK"] = "0"

from collections import OrderedDict
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)))

from icnet.models import icnet_paper

def demo_icnet():
    """Demo ICNet."""
    chainer.config.train = False
    chainer.config.enable_backprop = False

    config, img_path = parse_args()
    test_data = load_dataset_test(config["dataset"])
    test_iter = create_iterator_test(test_data, config['iterator'])
    model = get_model(config["model"])
    devices = parse_devices(config['gpus'])

    if devices:
        model.to_gpu(devices['main'])

    img = read_image(img_path)
    # img = img.transpose(1, 2, 0)
    # img = cv2.resize(img, (512, 256)).transpose(2, 0, 1)

    for i in range(2):
        s = time.time()
        pred = model.predict(img)[0]
        print("time: {}".format(time.time() - s))
    # Save the result image
    ax = vis_image(img)
    _, legend_handles = vis_semantic_segmentation(
        pred,
        label_colors=cityscapes_label_colors,
        label_names=cityscapes_label_names,
        alpha=1.0,
        ax=ax)
    ax.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc=2,
              borderaxespad=0.)
    plot.show()
    # base = os.path.splitext(os.path.basename(args.img_fn))[0]
    # out_fn = os.path.join(args.out_dir, 'predict_{}.png'.format(base))
    # plot.savefig(out_fn, bbox_inches='tight', dpi=400)


def main():
    demo_icnet()

if __name__ == '__main__':
    main()

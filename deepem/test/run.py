from __future__ import print_function
import os

import torch

from deepem.test.forward import Forward
from deepem.test.option import Options
from deepem.test.utils import *


def test(opt):
    # Model
    model = load_model(opt)

    # Forward scan
    forward = Forward(opt)
    for dname in opt.data_names:
        print(dname)
        scanner = make_forward_scanner(dname, opt)
        output = forward(model, scanner)
        save_output(dname, output, opt)


if __name__ == "__main__":
    # Options
    opt = Options().parse()

    # GPUs
    os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpu_id

    # Make directories.
    if not os.path.isdir(opt.exp_dir):
        os.makedirs(opt.exp_dir)
    if not os.path.isdir(opt.model_dir):
        os.makedirs(opt.model_dir)
    if not os.path.isdir(opt.fwd_dir):
        os.makedirs(opt.fwd_dir)

    # cuDNN auto-tuning
    torch.backends.cudnn.benchmark = opt.autotune

    # Run inference.
    print("Running inference: {}".format(opt.exp_name))
    test(opt)
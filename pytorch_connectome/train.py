from __future__ import print_function
import os
import time

import torch

from tensorboardX import SummaryWriter

from pytorch_connectome.data import Data
from pytorch_connectome.options import TrainOptions


def train(opt):
    # TODO: Create a model.

    # Data loader
    train_data = Data(opt, 'train')
    # eval_data = Data(opt, 'eval')

    # Optimizer
    trainable = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = torch.optim.Adam(trainable, lr=opt.base_lr)

    # Create a summary writer.
    writer = SummaryWriter(opt.log_dir)

    # Training loop
    t0 = time.time()
    print("========== BEGIN TRAINING LOOP ==========")
    for i in range(opt.chkpt_num, opt.max_iter):

        # Load training samples.
        sample = train_data(opt.in_spec)

        # Optimizer step
        optimizer.zero_grad()
        # losses, nmasks, inputs, preds, labels = model(sample)
        # weights = [opt.loss_weight[k] for k in sorted(opt.loss_weight)]
        # loss = sum([w*l.mean() for w, l in zip(weights,losses)])
        loss.backward()
        optimizer.step()

        # Elapsed time
        elapsed = time.time() - t0

        # Averaging & displaying stats
        if (i+1) % opt.avgs_intv == 0 or i < opt.warm_up:
            raise NotImplementedError

        # Logging images
        if (i+1) % opt.imgs_intv == 0:
            raise NotImplementedError

        # Evaluation loop
        if (i+1) % opt.eval_intv == 0:
            pass

        # Model snapshot
        if (i+1) % opt.chkpt_intv == 0:
            raise NotImplementedError

        # Restart timer.
        t0 = time.time()

    # Close the summary writer.
    writer.close()


if __name__ == "__main__":
    # Options
    opt = TrainOptions().parse()

    # GPUs
    os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(opt.gpu_ids)

    # Make directories.
    if not os.path.isdir(opt.exp_dir):
        os.makedirs(opt.exp_dir)
    if not os.path.isdir(opt.log_dir):
        os.makedirs(opt.log_dir)
    if not os.path.isdir(opt.model_dir):
        os.makedirs(opt.model_dir)

    # cuDNN auto-tuning
    torch.backends.cudnn.benchmark = opt.autotune

    # Run experiment.
    print("Running experiment: {}".format(opt.exp_name))
    train(opt)
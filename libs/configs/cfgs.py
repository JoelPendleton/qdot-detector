# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
import os
import tensorflow as tf
import math

"""
FLOPs: 2265025702;    Trainable params: 72323263

single scale:
This is your result for task 1:

    mAP: 0.7621689030515238
    ap of each class:
    plane:0.8911299075888718,
    baseball-diamond:0.8319356150323267,
    bridge:0.532965628899156,
    ground-track-field:0.692229444940269,
    small-vehicle:0.7885344440845781,
    large-vehicle:0.8253443952966053,
    ship:0.8717523692116588,
    tennis-court:0.9036865664703386,
    basketball-court:0.8635620193886776,
    storage-tank:0.8658526534313077,
    soccer-ball-field:0.6689637165098199,
    roundabout:0.6450680681312201,
    harbor:0.6886764453856856,
    swimming-pool:0.6993915095320309,
    helicopter:0.6634407618703122

The submitted information is :

Description: RetinaNet_DOTA_R3Det_DCL_B_2x_20201026_183.6w
Username: yangxue
Institute: DetectionTeamUCAS
Emailadress: yangxue16@mails.ucas.ac.cn
TeamMembers: yangxue, yangjirui

multi-scale:
This is your result for task 1:

    mAP: 0.7670382656312196
    ap of each class:
    plane:0.8912587225241578,
    baseball-diamond:0.8295350063178848,
    bridge:0.5354391578943396,
    ground-track-field:0.7226694690814012,
    small-vehicle:0.7828926735591332,
    large-vehicle:0.8219394631377006,
    ship:0.8679072689260785,
    tennis-court:0.9067367273506963,
    basketball-court:0.8658560298103354,
    storage-tank:0.8678816823772975,
    soccer-ball-field:0.6748765620510818,
    roundabout:0.6687503362282022,
    harbor:0.7019636971279444,
    swimming-pool:0.6940805604576306,
    helicopter:0.673786627624411

The submitted information is :

Description: RetinaNet_DOTA_R3Det_DCL_B_4x_20201026_162w_ms
Username: yangxue
Institute: DetectionTeamUCAS
Emailadress: yangxue16@mails.ucas.ac.cn
TeamMembers: yangxue, yangjirui

This is your result for task 1:

    mAP: 0.7697170603172414
    ap of each class:
    plane:0.8926232861407345,
    baseball-diamond:0.8359568124943043,
    bridge:0.5305427879227442,
    ground-track-field:0.7275505523517319,
    small-vehicle:0.7813035809001221,
    large-vehicle:0.8196570061078225,
    ship:0.8694352114813823,
    tennis-court:0.9036266911006428,
    basketball-court:0.8597687568319556,
    storage-tank:0.8693901181479016,
    soccer-ball-field:0.6619147551751572,
    roundabout:0.6556220897240033,
    harbor:0.732884993776407,
    swimming-pool:0.7056251744598303,
    helicopter:0.699854088143882

The submitted information is :

Description: RetinaNet_DOTA_R3Det_DCL_B_4x_20201026_162w_ms_flip
Username: SJTU-Det
Institute: SJTU
Emailadress: yangxue-2019-sjtu@sjtu.edu.cn
TeamMembers: yangxue
"""

# ------------------------------------------------
VERSION = 'RetinaNet_DOTA_R3Det_DCL_B_4x_20201026'
NET_NAME = 'resnet152_v1d'  # 'MobilenetV2'

# ---------------------------------------- System
ROOT_PATH = os.path.abspath('../../')
print(20*"++--")
print(ROOT_PATH)
GPU_GROUP = "0,1,2,3"
NUM_GPU = len(GPU_GROUP.strip().split(','))
SHOW_TRAIN_INFO_INTE = 20
SMRY_ITER = 200
SAVE_WEIGHTS_INTE = 27000 * 4

SUMMARY_PATH = ROOT_PATH + '/output/summary'
TEST_SAVE_PATH = ROOT_PATH + '/tools/test_result'

if NET_NAME.startswith("resnet"):
    weights_name = NET_NAME
elif NET_NAME.startswith("MobilenetV2"):
    weights_name = "mobilenet/mobilenet_v2_1.0_224"
else:
    raise Exception('net name must in [resnet_v1_101, resnet_v1_50, MobilenetV2]')

PRETRAINED_CKPT = ROOT_PATH + '/dataloader/pretrained_weights/' + weights_name + '.ckpt'
TRAINED_CKPT = os.path.join(ROOT_PATH, 'output/trained_weights')
EVALUATE_DIR = ROOT_PATH + '/output/evaluate_result_pickle/'

# ------------------------------------------ Train and test
RESTORE_FROM_RPN = False
FIXED_BLOCKS = 1  # allow 0~3
FREEZE_BLOCKS = [True, False, False, False, False]  # for gluoncv backbone
USE_07_METRIC = True
ADD_BOX_IN_TENSORBOARD = True

MUTILPY_BIAS_GRADIENT = 2.0  # if None, will not multipy
GRADIENT_CLIPPING_BY_NORM = 10.0  # if None, will not clip

CLS_WEIGHT = 1.0
REG_WEIGHT = 1.0
ANGLE_WEIGHT = 0.5
USE_IOU_FACTOR = True
REG_LOSS_MODE = None
ALPHA = 1.0
BETA = 1.0

BATCH_SIZE = 1
EPSILON = 1e-5
MOMENTUM = 0.9
LR = 5e-4
DECAY_STEP = [SAVE_WEIGHTS_INTE*12, SAVE_WEIGHTS_INTE*16, SAVE_WEIGHTS_INTE*20]
MAX_ITERATION = SAVE_WEIGHTS_INTE*20
WARM_SETP = int(1.0 / 4.0 * SAVE_WEIGHTS_INTE)

# -------------------------------------------- Dataset
DATASET_NAME = 'DOTA'  # 'pascal', 'coco'
PIXEL_MEAN = [123.68, 116.779, 103.939]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
PIXEL_MEAN_ = [0.485, 0.456, 0.406]
PIXEL_STD = [0.229, 0.224, 0.225]  # R, G, B. In tf, channel is RGB. In openCV, channel is BGR
IMG_SHORT_SIDE_LEN = [800, 400, 600, 1000, 1200]
IMG_MAX_LENGTH = 1200
CLASS_NUM = 15
OMEGA = 180 / 256.
ANGLE_MODE = 0

IMG_ROTATE = True
RGB2GRAY = True
VERTICAL_FLIP = True
HORIZONTAL_FLIP = True
IMAGE_PYRAMID = True

# --------------------------------------------- Network
SUBNETS_WEIGHTS_INITIALIZER = tf.random_normal_initializer(mean=0.0, stddev=0.01, seed=None)
SUBNETS_BIAS_INITIALIZER = tf.constant_initializer(value=0.0)
PROBABILITY = 0.01
FINAL_CONV_BIAS_INITIALIZER = tf.constant_initializer(value=-math.log((1.0 - PROBABILITY) / PROBABILITY))
WEIGHT_DECAY = 1e-4
USE_GN = False
FPN_CHANNEL = 256
NUM_SUBNET_CONV = 4
FPN_MODE = 'fpn'

# --------------------------------------------- Anchor
LEVEL = ['P3', 'P4', 'P5', 'P6', 'P7']
BASE_ANCHOR_SIZE_LIST = [32, 64, 128, 256, 512]
ANCHOR_STRIDE = [8, 16, 32, 64, 128]
ANCHOR_SCALES = [2 ** 0, 2 ** (1.0 / 3.0), 2 ** (2.0 / 3.0)]
ANCHOR_RATIOS = [1, 1 / 2, 2., 1 / 3., 3., 5., 1 / 5.]
ANCHOR_ANGLES = [-90, -75, -60, -45, -30, -15]
ANCHOR_SCALE_FACTORS = None
USE_CENTER_OFFSET = True
METHOD = 'H'
USE_ANGLE_COND = False
ANGLE_RANGE = 180  # 90 or 180

# -------------------------------------------- Head
SHARE_NET = True
USE_P5 = True
IOU_POSITIVE_THRESHOLD = 0.5
IOU_NEGATIVE_THRESHOLD = 0.4
REFINE_IOU_POSITIVE_THRESHOLD = [0.6, 0.7]
REFINE_IOU_NEGATIVE_THRESHOLD = [0.5, 0.6]

NMS = True
NMS_IOU_THRESHOLD = 0.1
MAXIMUM_DETECTIONS = 100
FILTERED_SCORE = 0.05
VIS_SCORE = 0.4



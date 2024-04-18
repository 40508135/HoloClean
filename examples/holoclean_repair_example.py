import sys

sys.path.append('../')
import holoclean
from detect import NullDetector, ViolationDetector
from repair.featurize import *

variable = [1]

for i in range(len(variable)):
    # 1. Set up a HoloClean session.
    hc = holoclean.HoloClean(
        db_name='holo',
        domain_thresh_1=0,
        domain_thresh_2=0,
        weak_label_thresh=0.99,
        max_domain=10000,
        cor_strength=0.6,
        nb_cor_strength=0.8,
        epochs=10,
        weight_decay=0.01,
        learning_rate=0.001,
        momentum=0.9,
        threads=1,
        batch_size=1,
        verbose=False,
        timeout=3 * 60000,
        feature_norm=False,
        weight_norm=False,
        seed=45,
        print_fw=True
    ).session

    # 2. Load training data and denial constraints.
    hc.load_data('hospital', '../testdata/adult_dirty0.1.csv')
    hc.load_dcs('../testdata/adult_constraints.txt')
    hc.ds.set_constraints(hc.get_dcs())

    # 3. Detect erroneous cells using these two detectors.
    detectors = [NullDetector(), ViolationDetector()]
    hc.detect_errors(detectors)

    # 4. Repair errors utilizing the defined features.
    hc.setup_domain()
    featurizers = [
        InitAttrFeaturizer(),
        OccurAttrFeaturizer(),
        FreqFeaturizer(),
        ConstraintFeaturizer(),
    ]

    hc.repair_errors(featurizers)

    # 5. Evaluate the correctness of the results.
    hc.evaluate(fpath='../testdata/adult_clean.csv',
                tid_col='tid',
                attr_col='attribute',
                val_col='correct_val')
    print("variable is:", variable[i], "run:", i + 1)

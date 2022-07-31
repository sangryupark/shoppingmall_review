import os
import pandas as pd
import re

from hanspell import spell_checker
from tqdm import tqdm


def preprocess(data_path, file_name):
    if os.path.exists(os.path.join(data_path, file_name + "_fix")):
        print("Preprocess file already exist!")
        return pd.read_csv(os.path.join(data_path, file_name + "_fix"))

    else:
        before = pd.read_csv(os.path.join(data_path, file_name))
        after_id, after_review, after_target = [], [], []
        print("---- START PREPROCESSING ----")
        for idx in tqdm(range(len(before))):
            review = before["reviews"].iloc[idx]
            pattern = re.compile("[^ 가-힣0-9+]")
            pattern_check = pattern.sub("", review)
            spell_checked = spell_checker.check(pattern_check)

            if len(spell_checked) != 0:
                after_id.append(before["reviews"].iloc[idx])
                after_review.append(spell_checked.checked)
                after_target.append(before["target"].iloc[idx])

        after = pd.DataFrame(
            {
                "id": after_id,
                "reviews": after_review,
                "target": after_target,
            }
        )
        print("---- FINISH PREPROCESSING ----")
        return after

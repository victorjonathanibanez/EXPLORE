import os
import glob
import random
import math
import shutil

class TrainingDataCreator:
    def __init__(self):
        pass

    def create_training_data(self, source_dir, target_dir, objects, training_percentage=80, validation_percentage=20):
        def collect_candidates(folder_path):
            candidates = []
            for filename in glob.iglob(folder_path + '/**/*.jpg', recursive=True):
                candidates.append(filename)
            return candidates

        def create_images(candidates, img_save_path, file_prefix):
            cnt = 0
            for filename in candidates:
                cnt += 1
                new_filename = os.path.join(img_save_path, f'{file_prefix}_{cnt}.jpg')
                shutil.copy(filename, new_filename)

        def process(source_dir, target_dir, dist_training, dist_validation):
            objects.append('no')
            distributions = {'training': dist_training, 'validation': dist_validation}

            for cls in objects:
                candidates = collect_candidates(os.path.join(source_dir, cls))
                random.shuffle(candidates)

                offset = 0
                for key, percentage in distributions.items():
                    share = math.floor(len(candidates) / 100 * percentage)

                    class_path = os.path.join(target_dir, key, cls)
                    if not os.path.isdir(class_path):
                        os.makedirs(class_path)

                    create_images(candidates[offset:offset + share], class_path, cls)
                    offset += share

        process(source_dir, target_dir, training_percentage, validation_percentage)


# Example Usage:
# training_data_creator = TrainingDataCreator()
# training_data_creator.create_training_data('source_directory', 'target_directory', ['Object1', 'Object2', ...], 80, 20)

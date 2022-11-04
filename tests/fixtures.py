import pandas as pd
import glob
import random
import os
import sys
import librosa


def setup_fixtures(count=5):
    test_list = []
    current_folder = os.path.dirname(__file__)
    test_folder = current_folder + "/" + "resample_test_audio"
    port = f"123{sys.version_info.minor}"
    audio_paths = glob.glob(test_folder + "/*")
    for i in range(count):
        item = random.randint(0, len(audio_paths) - 1)
        test_list.append(
            (f"caption {i}" if i != 0 else "", audio_paths[item].replace(
                test_folder, f"http://localhost:{port}"))
        )
    test_list = test_list[:count]

    return test_list


def generate_url_list_txt(output_file, test_list):
    with open(output_file, "w") as f:
        for _, url in test_list:
            f.write(url + "\n")


def generate_csv(output_file, test_list):
    df = pd.DataFrame(test_list, columns=["caption", "url"])
    df.to_csv(output_file)


def generate_tsv(output_file, test_list):
    df = pd.DataFrame(test_list, columns=["caption", "url"])
    df.to_csv(output_file, sep="\t")


def generate_tsv_gz(output_file, test_list):
    df = pd.DataFrame(test_list, columns=["caption", "url"])
    df.to_csv(output_file, sep="\t", compression="gzip")


def generate_json(output_file, test_list):
    df = pd.DataFrame(test_list, columns=["caption", "url"])
    df.to_json(output_file)


def generate_parquet(output_file, test_list):
    df = pd.DataFrame(test_list, columns=["caption", "url"])
    df.to_parquet(output_file)


def check_one_audio_sr(audio_sr, target_sr):
    if audio_sr != target_sr:
        raise Exception(
            f"Audio sample rate is not right. Expected: {target_sr}, got: {audio_sr}")


def check_audio_sr(file_list_resampled, target_sr):
    for file_resampled in file_list_resampled:
        # y, sr = librosa.load(file)
        y_r, audio_sr = librosa.load(file_resampled)
        check_one_audio_sr(audio_sr, target_sr)

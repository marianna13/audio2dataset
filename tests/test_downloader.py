from fixtures import setup_fixtures
from audio2dataset.writer import FilesSampleWriter
from audio2dataset.downloader import Downloader

import pandas as pd
import os


def test_downloader():
    tmp_path = 'tmp'
    test_folder = str(tmp_path)
    test_list = setup_fixtures(count=5)
    audio_folder_name = os.path.join(test_folder, "audio")

    os.mkdir(audio_folder_name)
    writer = FilesSampleWriter

    downloader = Downloader(
        writer,
        sample_rate=16000,
        thread_count=32,
        save_caption=True,
        extract_exif=True,
        output_folder=audio_folder_name,
        column_list=["caption", "url"],
        timeout=10,
        number_sample_per_shard=10,
        oom_shard_count=5,
        compute_md5=True,
        encode_format="mp3",
        retries=0,
    )

    tmp_file = os.path.join(test_folder, "test_list.feather")
    df = pd.DataFrame(test_list, columns=["caption", "url"])
    df.to_feather(tmp_file)

    downloader((0, tmp_file))

    assert len(os.listdir(audio_folder_name + "/00000")) == 3 * len(test_list)

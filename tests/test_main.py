import pytest
from audio2dataset import download
from audio2dataset.downloader import Downloader
from audio2dataset.writer import FilesSampleWriter
from fixtures import (
    get_all_files,
    check_audio_sr,
    generate_input_file,
    setup_fixtures,
)

import os


@pytest.mark.parametrize("sample_rate", [16000])
def test_download_resample(sample_rate, tmp_path):
    test_folder = str(tmp_path)
    test_list = setup_fixtures()
    url_list_name = os.path.join(test_folder, "url_list")
    audio_folder_name = os.path.join(test_folder, "audio")
    unresampled_folder = os.path.join(test_folder, "unresampled_audio")

    download(
        url_list_name,
        sample_rate=sample_rate,
        output_folder=unresampled_folder,
        thread_count=32
    )

    l = get_all_files(audio_folder_name, "mp3")
    j = [a for a in get_all_files(
        audio_folder_name, "json") if "stats" not in a]
    assert len(j) == len(test_list)
    p = get_all_files(audio_folder_name, "parquet")
    assert len(p) == 1
    assert len(l) == len(test_list)
    check_audio_sr(j, sample_rate)

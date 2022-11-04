from audio2dataset.writer import (
    FilesSampleWriter,
    WebDatasetSampleWriter,
    ParquetSampleWriter,
    DummySampleWriter
)

import os
import glob
import pytest
import tarfile
import pandas as pd
import pyarrow as pa


@pytest.mark.parametrize("writer_type", ["files", "webdataset", "parquet", "dummy"])
def test_writer(writer_type, tmp_path):
    current_folder = os.path.dirname(__file__)
    test_folder = str(tmp_path)
    input_folder = current_folder + "/" + "resample_test_audio"
    output_folder = test_folder + "/" + "test_write"
    os.mkdir(output_folder)
    audio_paths = glob.glob(input_folder + "/*")
    schema = pa.schema(
        [
            pa.field("key", pa.string()),
            pa.field("caption", pa.string()),
            pa.field("status", pa.string()),
            pa.field("error_message", pa.string()),
            pa.field("sample_rate", pa.int32()),
            pa.field("original_sample_rate", pa.int32()),
            pa.field("duration", pa.int32()),
            pa.field("original_duration", pa.int32())
        ]
    )
    if writer_type == "files":
        writer_class = FilesSampleWriter
    elif writer_type == "webdataset":
        writer_class = WebDatasetSampleWriter
    elif writer_type == "parquet":
        writer_class = ParquetSampleWriter
    elif writer_type == "dummy":
        writer_class = DummySampleWriter

    writer = writer_class(0, output_folder, True, 5, schema, "mp3")

    for i, image_path in enumerate(audio_paths):
        with open(image_path, "rb") as f:
            audio_str = f.read()
            writer.write(
                audio_str=audio_str,
                key=str(i),
                caption=str(i),
                meta={
                    "key": str(i),
                    "caption": str(i),
                    "status": "ok",
                    "error_message": "",
                    "sample_rate": 16000,
                    "duration": 16000,
                    "original_sample_rate": 16000,
                    "original_duration": 16000
                },
            )
    writer.close()

    if writer_type != "dummy":

        df = pd.read_parquet(output_folder + "/00000.parquet")

        expected_columns = [
            "key",
            "caption",
            "status",
            "error_message",
            "sample_rate",
            "duration",
            "original_sample_rate",
            "original_duration"
        ]

        if writer_type == "parquet":
            expected_columns.append("mp3")

        assert df.columns.tolist() == expected_columns

        assert df["key"].iloc[0] == "0"
        assert df["caption"].iloc[0] == "0"
        assert df["status"].iloc[0] == "ok"
        assert df["error_message"].iloc[0] == ""
        assert df["sample_rate"].iloc[0] == 16000
        assert df["duration"].iloc[0] == 16000
        assert df["original_sample_rate"].iloc[0] == 16000
        assert df["original_duration"].iloc[0] == 16000

    if writer_type == "files":
        saved_files = list(glob.glob(output_folder + "/00000/*"))
        assert len(saved_files) == 3 * len(audio_paths)
    elif writer_type == "webdataset":
        l = glob.glob(output_folder + "/*.tar")
        assert len(l) == 1
        if l[0] != output_folder + "/00000.tar":
            raise Exception(l[0] + " is not 00000.tar")

        assert len(tarfile.open(output_folder +
                   "/00000.tar").getnames()) == len(audio_paths) * 3
    elif writer_type == "parquet":
        l = glob.glob(output_folder + "/*.parquet")
        assert len(l) == 1
        if l[0] != output_folder + "/00000.parquet":
            raise Exception(l[0] + " is not 00000.parquet")

        assert len(df.index) == len(audio_paths)
    elif writer_type == "dummy":
        l = glob.glob(output_folder + "/*")
        assert len(l) == 0

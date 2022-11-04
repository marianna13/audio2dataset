import pandas as pd
from audio2dataset import download

data = {
    'URL': [
        'https://mixkit.co/free-sound-effects/download/166/?filename=mixkit-fast-small-sweep-transition-166.wav',
        'https://demo.pro.radio/wp1/wp-content/uploads/2020/06/wpcast-podcast-samples-3.mp3'
    ],
    'CAPTION': [
        'Fast small sweep transition',
        'Fast rocket whoosh'
    ]
}


pd.DataFrame(data).to_csv('test.csv', index=False)
if __name__ == '__main__':
    download(
        'test.csv',
        input_format='csv',
        url_col='URL',
        caption_col='CAPTION',
        sample_rate=16000
    )

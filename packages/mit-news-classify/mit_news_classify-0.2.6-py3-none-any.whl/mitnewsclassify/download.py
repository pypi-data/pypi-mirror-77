import os
from urllib.request import urlretrieve
from tqdm import tqdm

# This is used to show progress when downloading.
# see here: https://github.com/tqdm/tqdm#hooks-and-callbacks
class TqdmUpTo(tqdm):
    """Provides `update_to(n)` which uses `tqdm.update(delta_n)`."""
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        b  : int, optional
            Number of blocks transferred so far [default: 1].
        bsize  : int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize  : int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)  # will also set self.n = b * bsize

def download(model=None):
    # downloading from dropbox
    # maybe in the future allow for downloading only some models?
    urls = {
        # tfidf model
        "/data/tfidf/model_2500_500_50.h5":"https://www.dropbox.com/s/cf37niebcuj6i8i/model_2500_500_50.h5?dl=1",
        "/data/tfidf/small_vocab_20.csv":"https://www.dropbox.com/s/v8ytgdeumwpw4g7/small_vocab_20.csv?dl=1",
        "/data/tfidf/tfmer_20.p":"https://www.dropbox.com/s/y46i525tzmf0hqx/tfmer_20.p?dl=1",
        '/data/tfidf/labelsdict_20.p':"https://www.dropbox.com/s/8c64ogjl82hz536/labelsdict_20.p?dl=1",
        '/data/tfidf/nyt-theme-tags.csv':"https://www.dropbox.com/s/kvf34v0ecnc7lgc/nyt-theme-tags.csv?dl=1",
        # tfidf_bi model
        "/data/tfidf_bi/model_2000_500_50.h5":"https://www.dropbox.com/s/8j7dwpl8k1trcol/model_2000_500_50.h5?dl=1",
        "/data/tfidf_bi/small_vocab_bi_20.csv":"https://www.dropbox.com/s/r9q5fmds0n5ujh2/small_vocab_bi_20.csv?dl=1",
        "/data/tfidf_bi/tfmer_bi_20.p":"https://www.dropbox.com/s/tbdji109vtvdotm/tfmer_bi_20.p?dl=1",
        '/data/tfidf_bi/labelsdict_bi_20.p':"https://www.dropbox.com/s/20hx0oav37wf1ly/labelsdict_bi_20.p?dl=1",
        '/data/tfidf_bi/nyt-theme-tags.csv':"https://www.dropbox.com/s/4b1d8ej25af8j6q/nyt-theme-tags.csv?dl=1",
        # doc2vec model
        "/data/doc2vec/model_1200_800_40.h5":"https://www.dropbox.com/s/ooqavntcjia3ery/model_1200_800_40.h5?dl=1",
        "/data/doc2vec/doc2vec_model":"https://www.dropbox.com/s/hk4snqw43adxcog/doc2vec_model?dl=1",
        "/data/doc2vec/doc2vec_model.trainables.syn1neg.npy":"https://www.dropbox.com/s/7w9sv4bc7vuv30b/doc2vec_model.trainables.syn1neg.npy?dl=1",
        # gpt2 model
        "/data/gpt2/gpt_0.5.pth":"https://www.dropbox.com/s/r1icj5ytplfhuj0/gpt_0.5.pth?dl=1",
        "/data/gpt2/labelsdict.p":"https://www.dropbox.com/s/d59odrsmawmhgt8/labelsdict.p?dl=1",
        "/data/gpt2/nyt-theme-tags.csv":"https://www.dropbox.com/s/c1wts9knu3htzch/nyt-theme-tags.csv?dl=1",
    }

    # get package directory
    pwd = os.path.dirname(os.path.abspath(__file__))
    print("Package directory: " + pwd)

    # make directories as needed
    try:
        os.mkdir(pwd + "/data")
    except FileExistsError:
        print(pwd + "/data" + " directory already exists, some other models downloaded. Continuing...")
    
    dirs = [
        "/data/tfidf",
        "/data/tfidf_bi",
        "/data/doc2vec",
        "/data/gpt2",
    ]
    for dir in dirs:
        if (model is None or model in dir):
            try:
                os.mkdir(pwd + dir)
            except FileExistsError:
                print(pwd + dir + " directory already exists... perhaps you already downloaded the data? Overwriting...")

    # download the files
    for sink, source in urls.items():
        if (model is None or model in sink):
            print("Downloading " + sink + " from " + source)
            try:
                with TqdmUpTo(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:  # all optional kwargs
                    urlretrieve(source, filename=pwd+sink, reporthook=t.update_to, data=None)
                    t.total = t.n
            except urllib.error.ContentTooShortError:
                print("Download incomplete?")
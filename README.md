# AUDIO AND LYRICS BASED EMOTION RECOGNITION USING MULTIMODAL DEEP LEARNING

## Installation Guide for Program Dependencies

1. Install the Python development environment on your system.
    Note: For easy installation and management of program dependencies, it is recommended to install python with pip and virtualenv.

    - Check if your Python environment is already configured:
        ```
        python3 --version
        pip3 --version
        virtualenv --version
        ```
    - If the packages are already installed, skip to the next step. Otherwise install using the following:
        ```
        sudo apt update
        sudo apt install python3-dev python3-pip
        sudo pip3 install -U virtualenv  # system-wide install
        ```

2. Create a virtual environment (recommended)
    ```
    virtualenv --system-site-packages -p python3 ./venv
    source ./venv/bin/activate  # sh, bash, ksh, or zsh
    pip install --upgrade pip
    pip list  # show packages installed within the virtual environment
    ```

3. Install the Tensorflow pip package.
    ```
    pip install --upgrade tensorflow
    ```
    Note: To specify version, use `pip install tensorflow@X.X`

4. Install NLTK using `pip install nltk`

5. Install WNAffect
    Clone files (emotion.py and wnaffect.py) from https://github.com/clemtoy/WNAffect

    To obtain Wordnet 1.6, download file from https://wordnet.princeton.edu/download/old-versions

    To obtain Wordnet-Domains 3.2, request to download file from http://wndomains.fbk.eu/download.html

6. Install spotipy using `pip install spotipy`

7. Install Jupyter Notebook using `pip install jupyter`

8. Install sklearn using `pip install sklearn`

9. Install imblearn using `pip install imblearn`

10. Install numpy using `pip install numpy`

11. Install pandas using `pip install pandas`


If you successfully installed all program dependencies, you are now set and ready to run this project!

## Other Files Needed
1. Obtain a copy of the following files from the Million Song Dataset (MSD):
    - Last.fm Dataset (TAG SQLite)
    - musiXmatch Dataset (SQLite format)
    - unique_tracks.txt

2. Obtain a copy of the Million Song Dataset Echonest mapping from https://labs.acousticbrainz.org/million-song-dataset-echonest-archive/ 

## Instructions

1. To obtain the desired dataset for this special problem, run the following programs in this order:
    - dataset_processing.py
    - map_tracks_to_spotify.py
    - get_audio_features.py
    - build_lyrics_vocab.py

2. Run jupyter notebook.

3. Open either model_audio.ipynb, model_lyrics.ipynb, or model_audio_lyrics.ipynb to run and test out the models.
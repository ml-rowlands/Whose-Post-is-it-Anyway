
# Whose Post Is It Anyway? - Strava Post Author Prediction

## Overview

This project aims to predict the author of a Strava post based on various features collected by GPS watches, as well as additional metadata collected by Strava. The model is trained on data from multiple athletes and can predict the most likely author of a new, unseen post.

## Features

- **Data Collection**: Automated script for pulling data.
- **Machine Learning Model**: Automatically hyperparameter tunes and selects the best performing machine learning pipeline for predictions and dumps the model for use in a web app.
- **Web App**: A Streamlit web app that allows users to input feature values and see prediction probabilities. See an example [here](https://strava-post-classifier.streamlit.app/)

## Requirements

- Python 3.x
- Scikit-learn
- Streamlit
- Pandas
- [More in `requirements.txt`](requirements.txt)

## Getting Started

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/ml-rowlands/Whose-Post-is-it-Anyway.git
    ```
   
2. Navigate to the project directory and install the requirements:
    ```bash
    cd your-repo
    pip install -r requirements.txt
    ```
3. Update the Strava API pull in ['Data_Pull.py'](Scripts/Data_Pull.py) to collect your own data.

### Usage

#### Running the Web App

```bash
streamlit run Strava_Post_Author_Predictor.py
```

Open the displayed URL in your web browser.

#### Running the Automated Model Update

This project includes a script for automated monthly updates to the machine learning model. To run the script, execute:

```bash
python sp_model_selection.py
```

## Contributing

Feel free to fork the project, open a pull request, or submit issues and feature requests.

## License

[MIT](LICENSE)

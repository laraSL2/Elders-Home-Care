# Elders-Home-Care Application
## About

The Elders-Home-Care Application is designed to enhance the efficiency in the elder care facilities. By leveraging technology, this application streamlines care notes and generates personalized care plans for each individual.

## How to Run the App
We have a deployed version of our application available at this link. [Deployed_App](https://elders-home-care-5furev6mdrbiygkteb9utt.streamlit.app)

If you need to run the app locally, please follow these steps. Additionally, we have pushed synthetic data samples to the [synthetic_data](https://github.com/laraSL2/Elders-Home-Care/tree/main/synthetic_data) folder. You can use this data for testing purposes. It’s important to note that all the data in this folder does not belong to real individuals.

### Step 1

1. Clone the GitHub repository:
   ```bash
   git clone git@github.com:laraSL2/Elders-Home-Care.git
   cd Elders-Home-Care
   ```
### Step 2

2. Create a Virtual environment & install the necessary packages by running the following command:
   ```bash
   pip install -r requirements.txt
   ```
### Step 3

3. Update the config.json file by adding the Gemini and Graph database to the App.

### Step 4

4. Run the Flask API .
   ```bash
   python run.py
   ```
   

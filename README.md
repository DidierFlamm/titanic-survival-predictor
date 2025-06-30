# 🚢 Titanic Survival Predictor

A Streamlit application presenting a complete Machine Learning case study.  
The goal: predict the probability of survival for each Titanic passenger based on features like age, sex, class, and family aboard.

🔗 **Live demo available here:** [didstitanic.streamlit.app](https://didstitanic.streamlit.app/)

---

## 📁 Project Structure
[root](https://github.com/DidierFlamm/titanic-survival-predictor)  
├── main.py          # Streamlit app launcher  
├── streamlit_app.py # Main Streamlit app (entry point)  
├── utils.py         # Utility functions  
├── /pages/          # Additional Streamlit pages  
└── README.md        # This file

  
## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/your-username/titanic-survival-predictor.git
cd titanic-survival-predictor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Google Cloud Credentials for Translation API
To use the Google Cloud Translation API, you need to configure a service account key:

1. **Create a Google Cloud project** and enable the Cloud Translation API.

2. **Create a Service Account Key** in JSON format.

3. **Locally:**
   - Copy `.env.example` to `.env` at the root of the project.
   - Fill in the variable `GOOGLE_APPLICATION_CREDENTIALS` with the path to your JSON key file.

   Example `.env`:

   ```env
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-key.json
   ```

**Note:** The free tier of the Google Cloud Translation API allows up to **500,000 characters** translated per month.  
See [Google Cloud Translation Pricing](https://cloud.google.com/translate/pricing) for details.

### 4. Launch the Streamlit app
You can launch the app either by running main.py or with streamlit run streamlit_app.py :  
```bash
python main.py
```
or
```bash
streamlit run streamlit_app.py
```
  
## 🔍 Features
Visualisations  
Models training and evaluation  
Optimisation  
Individual survival prediction  
  
## 🛠 Built With
Python  
Streamlit  
Scikit-learn  
Pandas / NumPy  
Matplotlib / Seaborn / Plotly  
  
## 📊 Example
Predict the survival of a 28-year-old woman in 1st class with no family aboard.

## 🌐 Live App  
No setup needed — try it instantly online:  
👉 [https://didstitanic.streamlit.app](https://didstitanic.streamlit.app)
  
## 📄 License  
MIT License – feel free to reuse and adapt.
  
## 🙌 Acknowledgements  
Inspired by the famous Titanic survival classification challenge from [Kaggle](https://www.kaggle.com/competitions/titanic/overview).

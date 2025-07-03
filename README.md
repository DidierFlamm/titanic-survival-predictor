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
   - Create a `.streamlit/secrets.toml` file at the root of your project (same level as streamlit_app.py).
   - Add your service account credentials in TOML format under a [google_credentials] section.  
   
   Example:

   ```toml
   [google_credentials]
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-private-key-id"
   private_key = """
   -----BEGIN PRIVATE KEY-----
   YOUR_PRIVATE_KEY_CONTENT_HERE
   -----END PRIVATE KEY-----
   """
   client_email = "your-service-account-email"
   client_id = "your-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email"
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
Plotly-express  
  
## 📊 Example
Predict the survival of a 28-year-old woman in 1st class with no family aboard.

## 🌐 Live App  
No setup needed — try it instantly online:  
👉 [https://didstitanic.streamlit.app](https://didstitanic.streamlit.app)
  
## 📄 License  
MIT License – feel free to reuse and adapt.
  
## 🙌 Acknowledgements  
Inspired by the famous Titanic survival classification challenge from [Kaggle](https://www.kaggle.com/competitions/titanic/overview).

## ℹ️ About
Author : Didier Flamm  
✉️ did_padman@hotmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/didier-flamm)  
Date : June 2025

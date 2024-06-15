# Smart ATS

Smart ATS is a Streamlit application that evaluates resumes based on a given job description. It uses Google Generative AI to analyze and provide feedback on resumes, helping users to improve their applications.

## Features

- Upload multiple resumes (PDF) at once.
- Evaluate and compare each resume individually.
- Showcase top N applications among the uploaded files.
- Display the results in a stacked format for better readability.

### Setup

1. **Clone the repository**

   ```sh
   git clone https://github.com/yourusername/smart-ats.git
   cd smart-ats

2. **Create and activate a new Conda environment**

   ```sh
   conda create -p smart-ats python=3.10
   conda activate smart-at

3. **Install the required packages**

   ```sh
   pip install -r requirements.txt

4. **Set up environment variables**

   ```sh
   GOOGLE_API_KEY=your_google_gemini_api_key

### Usage

1. **Run the Streamlit application**

   ```sh
   streamlit run app.py

2. **Open your browser and navigate to**

  ```sh
  http://localhost:8501



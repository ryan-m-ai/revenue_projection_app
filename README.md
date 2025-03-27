# Revenue Projection App

A Streamlit application for projecting revenue growth over time.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Features

- Input starting revenue
- Set annual growth rate
- Choose projection period
- View revenue projection chart
- See summary statistics

## GitHub Setup

1. Initialise git repository:
```bash
git init
```

2. Create .gitignore file:
```bash
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

3. Add and commit files:
```bash
git add .
git commit -m "Initial commit"
```

4. Create a new repository on GitHub and follow the instructions to push your code. 
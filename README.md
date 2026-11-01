# SmartPick AI: Personalized Mobile Phone Recommender System

## Project Overview
SmartPick AI is an AI-driven mobile phone recommendation system built for the
Samsung Innovation Campus Generative AI Mini Project (PJ1). It evaluates
smartphones using multi-criteria weighted scoring tailored to user personas,
rather than simple hard filters.

## Folder Structure
    StudentName_SmartPickAI/   (rename to YourName_SmartPickAI, no spaces)
    ├── assets/        # Logo (logo.png) and favicon
    ├── notebooks/     # SmartPickAI_PJ1.ipynb + scripts (data_cleaning.py, recommendation.py, build_frontend.py,
    │                #   frontend_template.html, smartpick_ai.html, app.py)
    ├── prompts/       # Persona prompts, scoring template, explanation template
    ├── datasets/      # Input dataset (sic_mobile_spec_PJ1.xlsx)
    ├── outputs/       # sample_recommendations.md, evaluation_log.md
    ├── requirements.txt
    └── README.md

## Customer Personas & Weights
1. Student: Price 40%, Battery 25%, RAM 15%, Storage 10%, Processor 10%
2. Gamer: Processor 35%, RAM 30%, Battery 20%, Storage 10%, Price 5%
3. Content Creator: Camera 40%, Storage 20%, RAM 15%, Processor 15%, Battery 5%, Price 5%
4. Business Professional: Battery 30%, Processor 30%, RAM 20%, Price 10%, Storage 10%
5. Senior Citizen: Price 40%, Battery 30%, RAM 15%, Storage 10%, Processor 5%

## Technologies Used
- Python, Pandas, NumPy — data processing
- Scikit-learn — Min-Max normalization
- HTML + Tailwind CSS + Chart.js — web frontend; Streamlit — optional second UI
- Matplotlib — visual analytics
- Pillow — loads the SmartPick AI logo and favicon

## Images
Phone cards use free Pexels stock photos (direct image URLs, no API key needed).
The SmartPick AI logo lives in assets/logo.png and appears in the page header,
sidebar and browser tab.

## Dataset
datasets/sic_mobile_spec_PJ1.xlsx - 413 phones, 11 columns (name, rating, price, camera,
display_type, display_size, battery, storage, ram, weight, processor).
Cleaning handles mixed price formats, storage in GB/TB, and 276 missing processors.

## Dependencies
See requirements.txt. Install with: pip install -r requirements.txt

## How to Run
1. Install dependencies:  pip install -r requirements.txt
2. Enter the code folder:  cd notebooks
3. Web frontend (recommended): open notebooks/smartpick_ai.html in any browser (double-click).
   It is a single file with the 413 phones, personas and logo built in. It loads Tailwind CSS and
   Chart.js from a CDN, so an internet connection is needed. To rebuild it after changing the dataset,
   weights or logo:  python build_frontend.py
4. Notebook:               jupyter notebook SmartPickAI_PJ1.ipynb   (Run All, top to bottom)
5. Streamlit app (optional): streamlit run app.py

## Frontend Features (smartpick_ai.html)
- Persona chips: Student, Gamer, Content Creator, Business Pro, Senior Citizen, Custom Sliders
- Budget slider, minimum RAM, display type and brand filters
- Criteria weight sliders (price, RAM, camera, battery, storage, processor) that load each persona's weights
- Plain-English search box, e.g. "Best camera phone under $350 with AMOLED"
- Top 5 / 10 / 20 cards with score, spec badges and a "why this phone" explanation
- Side-by-side compare (up to 4 phones) with radar chart, and a "Similar Phones" finder
- Scores match recommendation.py exactly (Min-Max scaling, inverted price, weighted sum x 100)

## APIs Used
None. No API keys are needed. Code was developed with Gemini/Claude assistance.

## Evaluation / Outputs
Sample generated recommendations are in outputs/. The app ranks the top 5 phones
per persona and provides an AI explanation for each match.

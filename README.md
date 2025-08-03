# ⚡ EV Routing Optimizer with Discharge Stations

A Streamlit web app that solves Electric Vehicle Routing Problems (EVRP) with support for **discharge stations**, **custom vehicle capacity**, and **multiple test cases or uploads**.

---

## 🚀 Features

- Select from preloaded test case CSV files or upload your own.
- Toggle **discharge mode** to allow optional visits to discharge stations for profit.
- View optimized delivery routes for a fleet of EVs.
- Automatically labels **Depot**, **Customer**, and **Discharge Station**.
- Clean and interactive interface built with Streamlit.
- Supports flexible number of vehicles and capacity settings.

---

## 📁 Folder Structure

EV-Routing/
├── streamlit_app.py
├── Test_Case_CSV_Files/
│ ├── testcase1.csv
│ ├── testcase2.csv
│ ├── testcase3.csv
│ └── testcase4.csv
├── requirements.txt
├── README.md
├── .gitignore
└── venv/


    ## 📄 Test Case Format

Uploaded or default CSVs must contain the following columns:

| ID | X | Y | Demand | NodeType |
|----|----|----|--------|----------|
| 0  | 10 | 20 |  0     | Depot    |
| 1  | 25 | 30 | 20     | Customer |
| 2  | 50 | 15 |  0     | DischargeStation |

> ⚠️ **Column headers are case-sensitive**.

---

## Hosted App:
Visit the live app here:
https://your-hosted-streamlit-link

---

## Team Credits
Developed by Team-Mind_Mesh

Developers: Amrutha D, Vishnu V

College: REVA University, Bangalore

Contact: vishnuv2309@gmail.com

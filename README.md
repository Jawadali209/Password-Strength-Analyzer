# 🔐 Password Strength Analyzer and Cracking Simulation Tool

An educational cybersecurity tool that **analyzes password strength** and runs a
**controlled, ethical simulation** of common password-guessing strategies to
show *why* weak passwords are easy to guess. Built as a Master's dissertation
project and deployed as an interactive Streamlit dashboard.

> ⚠️ **Ethical scope:** This tool never attacks real systems, accounts, or
> leaked password lists. All demonstrations use user-supplied input or synthetic
> sample data, and the word *"cracking"* refers only to a controlled,
> classroom-style simulation (Kelley et al., 2012).

---

## 📌 Overview

Password-based authentication is still the first line of defence for most digital
services, yet users routinely choose weak, predictable passwords. Simple
character-count rules are not enough because they miss common words, keyboard
walks and repeated structures (Wheeler, 2016). This project turns that research
into a practical, easy-to-understand tool that:

1. scores a password and explains its weaknesses in plain language, and
2. simulates dictionary and brute-force guessing to illustrate real risk.

## ✨ Features

- Password strength score (0–100) and strength band (Very Weak → Excellent)
- Theoretical **entropy** and **effective entropy** (entropy adjusted for patterns)
- Dictionary-word, keyboard-pattern, sequential-number and repeated-character detection
- Plain-language weaknesses and improvement recommendations
- **Controlled cracking simulation:** dictionary attack (word + mutations) and brute-force estimate
- Attack-type prediction and estimated crack time
- Analytics dashboard over a 215-password synthetic dataset (Plotly charts)
- Interactive Streamlit web app

## 🛠 Technologies

Python · Streamlit · Pandas · NumPy · Plotly

## 📂 Project Structure

```
Password-Strength-Analyzer/
├── analyzer.py           # Core analysis engine (scoring, entropy, checks)
├── simulator.py          # Controlled dictionary + brute-force simulation
├── app.py                # Streamlit dashboard
├── config.py             # Central configuration (weights, thresholds)
├── generate_dataset.py   # Reproducible dataset builder (seeded)
├── dictionary.txt        # Common-word list for detection
├── sample_passwords.csv  # Synthetic dataset (215 sample passwords)
├── requirements.txt      # Python dependencies
├── README.md
├── LICENSE               # MIT
└── .gitignore
```

## 🚀 Run Locally

```bash
git clone https://github.com/<your-username>/Password-Strength-Analyzer.git
cd Password-Strength-Analyzer
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **New app**, select your repository, branch `main`, and main file `app.py`.
4. Click **Deploy** — Streamlit installs `requirements.txt` automatically.

## 📊 Dataset

`sample_passwords.csv` contains 215 synthetic sample passwords spanning common,
dictionary, pattern, moderate, strong and excellent-random categories. It is
produced by `generate_dataset.py` with a fixed random seed, so results are fully
reproducible. No real, leaked or personal passwords are used.

## 📚 Selected References

- Bonneau, J. (2012) *The science of guessing.* IEEE S&P.
- Kelley, P.G. et al. (2012) *Guess again: measuring password strength by simulating cracking algorithms.* IEEE S&P.
- Wheeler, D.L. (2016) *zxcvbn: low-budget password strength estimation.* USENIX Security.
- Shay, R. et al. (2016) *Designing password policies for strength and usability.* ACM TISSEC.
- NIST (2020) *Digital Identity Guidelines (SP 800-63B).*

## 📄 License

Released under the MIT License — see [LICENSE](LICENSE).

## 👤 Author

MS Data Science — Dissertation Project (2026)

# 💰 Expenses — Python Expense Management & Statement Parser

A Python-based automation project for managing and parsing expense data from receipts, bank statements, and other financial sources.  
It extracts, normalizes, and exports structured expense data for better tracking and analysis.

---

## 📁 Project Structure

```bash
.
├── exporter.py
├── extractor.py
├── normalizer.py
├── parsing.py
├── project.py
├── sorter.py
├── test_project.py
├── requirements.txt
└── README.md
```

| File | Description |
|------|--------------|
| **extractor.py** | Extracts raw data from files (images, PDFs, CSVs). |
| **parsing.py** | Parses raw text into structured fields like date, vendor, and amount. |
| **normalizer.py** | Cleans and standardizes data formats (dates, currency, etc.). |
| **sorter.py** | Sorts or organizes entries by date, category, or vendor. |
| **exporter.py** | Exports processed data into CSV, Excel, or JSON format. |
| **project.py** | Coordinates all modules into a complete ETL (Extract → Transform → Load) pipeline. |
| **test_project.py** | Contains pytest-based tests for validating functionality. |

---

## ⚙️ Setup & Installation

1. **Clone the repository**

   ```bash
   git clone <https://github.com/cjawale-QABA/expenses.git>
   cd expenses
   ```

2. **Create and activate a virtual environment**

   ``` bash
   python3 -m venv venv
   source venv/bin/activate     # On macOS/Linux # or
   venv\Scripts\activate        # On Windows
   ```

3. **Install dependencies**

   ``` bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Use

### Option 1 — Run the entire pipeline python

```python
import project

# This will trigger the end-to-end pipeline 
# 1. Extract → 2. Parse → 3. Normalize → 4. Sort → 5. Export

project.main()

```

### Option 2 — Use individual modules

```python
from extractor import extract
from parsing import parse
from normalizer import normalize
from sorter import sort
from exporter import export

raw_data = extract("input/bank_statement.pdf")
parsed_data = parse(raw_data)
clean_data = normalize(parsed_data)
sorted_data = sort(clean_data)
export(sorted_data, "output/expenses.csv")
```

---

## 🧪 Running Tests

Use `pytest` to run all unit and integration tests:

```bash
pytest
```

You can also check coverage (if installed):

```bash
pytest --cov=.
```

---

## ✨ Features

- 🔍 Extracts data from multiple file formats (PDF, image(images should be clear), email(to be exhanced))
- 🧹 Normalizes dates, vendors, and amounts
- 🧾 Exports clean data to CSV/Excel for reporting
- ⚙️ Modular design — easily extend or replace components
- ✅ Simple pytest test suite for validation

---

## 🛣️ Roadmap

- [ ] OCR integration for image-based bills  
- [ ] Vendor categorization using keyword mapping  
- [ ] Add CLI support for quick command-line execution  
- [ ] Export to Excel and Google Sheets  
- [ ] Add logging and configuration management  

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository  
2. Create a new branch (`feature/my-feature`)  
3. Add your feature or fix and update tests  
4. Submit a Pull Request  

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

Thanks to open-source Python libraries and community contributors who inspired this project’s modular ETL-style architecture.

---

**Author:** [Chaitali Jawale](https://github.com/cjawale-QABA)  
**Project:** [Expenses](https://github.com/cjawale-QABA/expenses)

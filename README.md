# E-Commerce Analytics Dashboard

This dashboard is a Streamlit application designed to analyze e-commerce data from a `main_data.csv` file. It provides interactive visualizations to understand sales performance, top-selling products, customer locations, and delivery status.

## Features

* **Product Analysis**: Displays the top 10 and bottom 10 products ranked by order volume and revenue.
* **Geographic Analysis**: Shows the top 10 cities and states ranked by order volume and revenue.
* **Delivery Analysis**: Visualizes the distribution of delivery status (on-time vs. late).
* **Date Filtering**: Allows users to filter data by date range.
* **Interactive Sidebar**: Provides date filters and copyright information.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/bachtiarashidiqy/EcommerceDashboard.git
    cd EcommerceDashboard
    ```

2.  **Create a virtual environment (optional):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For macOS and Linux
    venv\Scripts\activate  # For Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, you can create one with:

    ```bash
    pip freeze > requirements.txt
    ```

4.  **Run the application:**

    ```bash
    streamlit run dashboard.py
    ```

5.  **Open in browser:**

    Open the URL displayed in the terminal in your web browser.

## File Structure
<pre>
EcommerceDashboard/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── data_1.csv
│   └── data_2.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
</pre>

## Dependencies

* streamlit
* pandas
* matplotlib
* seaborn

## Usage

1.  **Filter Data**: Use the date input widgets in the sidebar to filter data by date range.
2.  **Visualize**: View the visualizations on the main page to understand sales, products, locations, and delivery performance.
3.  **Interact**: Hover over visualizations to see more details.

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.
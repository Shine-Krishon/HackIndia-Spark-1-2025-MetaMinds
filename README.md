# Crop Forecasting Application

This is a web-based application for forecasting crop yields and providing recommendations based on various factors such as district and crop type.

## Project Structure

## Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```sh
   cd <project-directory>
   ```
3. Create a virtual environment:
   ```sh
   python -m venv virt
   ```
4. Activate the virtual environment:
   - On Windows:
     ```sh
     .\virt\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source virt/bin/activate
     ```
5. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```sh
   python app.py
   ```
2. Open your web browser and navigate to `http://127.0.0.1:5000`.

## File Descriptions

- [app.py](http://_vscodecontentref_/6): The main application file that contains the Flask server code.
- [crop_data.csv](http://_vscodecontentref_/7): The dataset containing crop information.
- [static](http://_vscodecontentref_/8): Directory containing static files such as CSS stylesheets.
  - [forecast.css](http://_vscodecontentref_/9): Styles specific to the forecast page.
  - [styles.css](http://_vscodecontentref_/10): General styles for the application.
- [templates](http://_vscodecontentref_/11): Directory containing HTML templates.
  - `error.html`: Template for error pages.
  - `forecast.html`: Template for the forecast page.
  - `index.html`: Template for the home page.
  - `markets.html`: Template for the markets page.
  - `recommend.html`: Template for the recommendation page.
- [virt](http://_vscodecontentref_/12): Directory containing the virtual environment files.

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```sh
   git push origin feature-branch
   ```
5. Create a pull request.

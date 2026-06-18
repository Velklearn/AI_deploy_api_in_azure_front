from streamlit.testing.v1 import AppTest
from pathlib import Path


APP_FILE = Path(__file__).resolve().parents[1] / "yourwineui" / "app.py"

def test_markdown_texts():
    """Check the Text Content when user visits the main page"""
    at = AppTest.from_file(str(APP_FILE)).run()
    assert at.markdown[0].value == "# Wine Quality Prediction App 🍷🍇"
    assert at.markdown[2].value == "### **Select Mode:**"

def test_selectbox_options():
    """Check the Main Options of the select box"""
    at = AppTest.from_file(str(APP_FILE)).run()
    assert at.selectbox[0].options == ['Choose', 'Input version', 'Slider version']

def test_slider_version():
    """Check the slider labels in slider version"""
    at = AppTest.from_file(str(APP_FILE)).run()
    at.selectbox[0].set_value("Slider version").run()
    assert at.slider[0].label == "Volatile Acidity"
    assert at.slider[1].label == "Alcohol"

def test_input_version():
    """Check the input labels in input version"""
    at = AppTest.from_file(str(APP_FILE)).run()
    at.selectbox[0].set_value("Input version").run()
    assert at.number_input[0].label == "Volatile Acidity"
    assert at.number_input[1].label == "Alcohol"

def test_predict_button():
    """Test the predict button initial status"""
    at = AppTest.from_file(str(APP_FILE)).run()
    at.selectbox[0].set_value("Input version").run()
    assert at.button[0].value == False
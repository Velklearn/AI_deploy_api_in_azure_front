## Challenge 2: Build and Deploy a Web App in Azure

## Overview

🎯 **Exercise objectives**:

* Build a Streamlit Web App that consumes the API you deployed in Challenge 1.
* Deploy the Web App to Azure **on your existing App Service Plan**, with the Azure CLI.
* Perform code tests with pytest.
* **(Bonus)** Automate the deployment with CI/CD using GitHub Actions.

🔧 **Tools**:

* **VS Code** for interactive coding
* **Streamlit** to build Web Apps
* **Azure CLI (`az`)** to deploy
* **GitHub** to host the code of your Apps

---
## 📃 Instructions

In this challenge, you will build a Web App with Streamlit to predict wine quality using your deployed API. Then, you will deploy it to Azure App Services. By the end, you will understand how to deploy user interfaces that consume APIs with predictive models.

First, you will create a simple **Front-End** (website) to let anyone predict the quality of red wine 📈📉🍷🤔 using an API.

For now, we used notebooks for data exploration and model training, then exposed the model with an API. But an API is not meant to be used directly by end users. We create a separate project for the website to keep things organised.

🤔 Why split our code into different projects?

👉 Separating exploration + preprocessing + training from the website keeps the website package very light.

👉 Separate projects also ease the deployment of the interface and the API independently.

The website package doesn't need any model-training code, since the trained model is exposed by our FastAPI application.

Splitting training, prediction and website has several benefits:

- We can deploy our small package on light hosting solutions.
- Other teams (e.g. web developers) can work with us without any Data Science knowledge.
- It follows the web pattern of separating the `Front-End` (the website) from the `Back-End` (the service). Typically, we use an API to make predictions and display them in the website.

For these reasons, we'll create a new repository for our website and plug it into our API.

⚠️ In this Challenge, **Sections 1, 2 and 3 are mandatory**. You can come back to do Sections 4-9 if you finish Challenges 3, 4 and 5.

---
### 1. Build and test your first Web App locally

> 🎈 **What is Streamlit?** Streamlit is a Python library that turns a plain script into an interactive web app — no HTML, CSS or JavaScript needed. You write Python top to bottom, and each Streamlit call (`st.title`, `st.slider`, `st.button`...) renders a UI element in the browser. The mental model is simple: **your script re-runs from top to bottom on every interaction**, and the current widget values drive what's displayed. That's why you don't write callbacks like in classic front-end frameworks — you just read a widget's value where you need it.
>
> A few building blocks you'll use here:
> - **Text**: `st.title`, `st.markdown`, `st.text` — display text and headings.
> - **Inputs**: `st.number_input`, `st.slider`, `st.selectbox` — get values from the user.
> - **Actions**: `st.button` — returns `True` on the run where it was clicked.
>
> 📚 Keep these two open in a tab — they're all you need:
> - the [Streamlit cheatsheet](https://cheat-sheet.streamlit.app/) (every widget at a glance),
> - the [API reference](https://docs.streamlit.io/develop/api-reference) (details and examples for each one).

- Create a new project directory for the website, at `/Documents/GitHub/`. Use a unique name without spaces — your first name works well, e.g. `frederic-wineui`.

- Open `Anaconda Prompt` using the `streamlit-env` environment you created during the setup:

<figure style="width: 90%">
  <img alt="Anaconda-Navigator-environment-6-activate.png" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNjk0Qmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--17c1ad93ffc67fd6aaacdc90682e5c205ece9ecf/Anaconda-Navigator-environment-6-activate.png?disposition=attachment" />
</figure>

- Once the terminal is open, type:

```bash
cd Documents/GitHub
```

<figure style="width: 80%">
  <img alt="streamlit-env-4.png" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBK2w0Qmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--76adb1aa94aabc3857ba7e64c956edeb4bd248c0/streamlit-env-4.png" />
</figure>

This changes the current directory to the GitHub folder where we keep our projects.

- Create a new directory with `mkdir`:

```bash
mkdir yourwineui
```

- Change into it:

```bash
cd yourwineui
```

- Create a new Python file `app.py`:

```bash
touch app.py
```

- Open `app.py` in VS Code with the `streamlit-env`.

- Copy this code into `app.py` and save:

```python
import streamlit as st

# this is the main function in which we define our webpage
def main():
    st.markdown("# Wine Quality Prediction App 🍷🍇")
    st.markdown("### This app is meant to predict red wine quality " +
            "according to different chemical")

# Init code
if __name__=='__main__':
    main()
```

- Back in the terminal:

```bash
streamlit run app.py
```

The app opens automatically in your browser. If not, go to the localhost address shown in your terminal, typically http://localhost:8501.

- You should see a website with the two titles. If so, close the Web App and go back to VS Code.

---
### 2. Use your Web App to get predictions

Create the input fields for each feature required by the model. Use widgets such as `st.number_input` or `st.slider` to get values for each feature: volatile acidity, citric acid, residual sugar, etc. In our case, we'll use only volatile acidity and alcohol.

Example:

```python
# input number version
volatile_acidity = st.number_input("Volatile Acidity", min_value=0.0, max_value=2.0, value=0.7)
alcohol = st.number_input("Alcohol", min_value=0.0, max_value=20.0, value=9.4)


# slider version
volatile_acidity = st.slider('Volatile Acidity', 0.0, 2.0, 0.319, 0.001)
alcohol = st.slider('Alcohol', 0.0, 16.0, 11.634, 0.01)
```

- Run your application and check it displays the values from the widgets:

```python
st.text(volatile_acidity)
st.text(alcohol)
```

- At the beginning of `app.py`, define the URL of the API you deployed in the last challenge. Then create a button that, when clicked, calls the API to predict the wine quality using the widget data and displays the prediction. Use the [Streamlit cheatsheet](https://cheat-sheet.streamlit.app/). Feel free to try other components.

> 🧠 **The key idea — the front-end talks to the back-end over HTTP.** Your Streamlit app doesn't load the model; it sends the feature values to your API and displays whatever comes back. Concretely, with the `requests` library:
> ```python
> import requests
> url = "https://your-api.azurewebsites.net/predict"   # your API from Challenge 1
> response = requests.post(url, json={"alcohol": alcohol, "volatile_acidity": volatile_acidity})
> prediction = response.json()
> st.write(prediction)
> ```
> This is exactly the Front-End ↔ Back-End split from the intro: the UI is "dumb" (it just collects inputs and shows results), the API holds the intelligence (the model). Each can be developed, tested and deployed on its own.

---
### 3. Build your local Python package

- First, download the <a download="app.py" href="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNUtIQmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--0c5782dcdf895583a1fa680ab9744ad5c5536907/app.py?disposition=attachment">final version of app.py</a> and replace the one you created in `yourwineui` (keep a copy of yours if you want).

- Copy the `img/wine6.png` found in the challenge repository into the `yourwineui` project.

- Change the URL in `app.py` to your API URL. Check you can get predictions with your Web App as in the Figures:

<figure style="width: 70%">
  <img alt="Capture d'écran 2024-09-22 222823.png" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNU9IQmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--60ef7c2bf42b9eef6856227fcb9baa9adf405c5c/Capture%20d'%C3%A9cran%202024-09-22%20222823.png?disposition=attachment" />
</figure>

<figure style="width: 70%">
  <img alt="Capture d'écran 2024-09-22 222839.png" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNVNIQmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--219b730298417bad9e8c7231819b846407065cb9/Capture%20d'%C3%A9cran%202024-09-22%20222839.png?disposition=attachment" />
</figure>

<figure style="width: 70%">
  <img alt="Capture d'écran 2024-09-22 222902.png" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNVdIQmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--744d480b11e694ef877e6f6e2c352c725750bf18/Capture%20d'%C3%A9cran%202024-09-22%20222902.png?disposition=attachment" />
</figure>

- Use GitHub Desktop to initialize your local repository with Git: `Create new repository`, select your folder location, give it the same name as your folder (as for the API repository).

<figure style="width: 70%">
  <img alt="Capture d'écran 2024-09-22 183118.png"  src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBM2lIQmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--94d3217bf9f08e3bd9520f686723620c6709446e/Capture%20d'%C3%A9cran%202024-09-22%20183118.png" />
</figure>

- Copy the `.gitignore` from your API project into the Web App project, and check you have `app.py` too. Then commit your changes in GitHub Desktop with a message (e.g. `First commit`).

- Create a `requirements.txt` with the libraries needed to run the Web App:

```text
pip>=9
setuptools>=26
wheel>=0.29
pandas
numpy
requests
streamlit
```

> 💡 Compare with the API's `requirements.txt`: no scikit-learn, no joblib, no FastAPI here — the Web App loads no model, it only *talks* to the API (that's what `requests` is for). This is what "keeping the front-end light" means concretely.

> 💡 And as for the API: no `setup.py`, no `setup.sh` — Azure installs this `requirements.txt`, and we'll give it the start command directly in the Web App configuration.

- Your local repository `Documents/GitHub/yourwineui` should contain:

```
yourwineui
│   .gitignore
│   app.py
│   requirements.txt
│
└───img
│   │   wine6.png
```

- Save and commit this checkpoint with GitHub Desktop.

------
## **Bonus Sections**

Go to the next Challenge 3. You can come back to do Sections 4-9 if you finish Challenges 3, 4 and 5.

------
### 4. Build and test your code with pytest

As before, testing code enables test automation for CI/CD. We'll evaluate locally with `pytest` first, then activate CI/CD later. See how to test Streamlit in the [documentation](https://docs.streamlit.io/develop/concepts/app-testing/cheat-sheet).

- Create a folder `tests` with an empty `__init__.py` and a file `test_app.py`.

- In `test_app.py`, add:

```python
from streamlit.testing.v1 import AppTest

def test_markdown_texts():
    """Check the Text Content when user visits the main page"""
    at = AppTest.from_file("app.py").run()
    assert at.markdown[0].value == "# Wine Quality Prediction App 🍷🍇"
    assert at.markdown[2].value == "### **Select Mode:**"

def test_selectbox_options():
    """Check the Main Options of the select box"""
    at = AppTest.from_file("app.py").run()
    assert at.selectbox[0].options == ['Choose', 'Input version', 'Slider version']

def test_slider_version():
    """Check the slider labels in slider version"""
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value("Slider version").run()
    assert at.slider[0].label == "Volatile Acidity"
    assert at.slider[1].label == "Alcohol"

def test_input_version():
    """Check the input labels in input version"""
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value("Input version").run()
    assert at.number_input[0].label == "Volatile Acidity"
    assert at.number_input[1].label == "Alcohol"

def test_predict_button():
    """Test the predict button initial status"""
    at = AppTest.from_file("app.py").run()
    at.selectbox[0].set_value("Input version").run()
    assert at.button[0].value == False
```

This simulates the Streamlit app and tests its elements with a unit-testing approach.

🧠 Note these tests check the **UI structure and behaviour** (titles, widgets, button state), not predictions. The model is the API's responsibility, tested in its own repository: each project tests *its* job.

- Open an Anaconda Prompt with the `streamlit-env`. From the **project root**:

```bash
cd # Gets back to the $HOME directory
cd Documents/GitHub/yourwineui
pytest tests/test_app.py
```

You should get **5 passed**. If pytest is not found:

```bash
pip install pytest
pytest tests/test_app.py
```

<figure style="width: 90%">
  <img alt="Capture d'écran 2024-09-23 003032.png" src="https://learn.lewagon.com/rails/active_storage/blobs/redirect/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNWFIQmc9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--3167a07af271712031ae61d0525f0abd3b566415/Capture%20d'%C3%A9cran%202024-09-23%20003032.png?disposition=attachment" />
</figure>

If you do not obtain this result, ask a TA for help.

- Your local repository should contain:

```
yourwineui
│   app.py
│   requirements.txt
│   .gitignore
│
└───tests
│   │   __init__.py
│   │   test_app.py
│
└───img
│   │   wine6.png
```

---
### 5. Create a GitHub repository and link it to your local project

- In GitHub Desktop, from `Documents/GitHub/yourwineui`, use **Publish repository** to push to GitHub. Follow the instructions.

- Open your GitHub account and check the remote repository has all your files. If not, ask a TA.

---
### 6. Deploy your Web App on the SAME App Service Plan

⚠️ **Do NOT create a new App Service Plan.** You already have one from Challenge 1 — we'll deploy this second app on it. Remember: the **plan is the machine you pay for**, and a **Web App is just an application running on it**. Putting two apps on one plan means your bill doesn't change — API and UI share the same machine. (In production, teams sometimes separate them to scale independently, but for us one B1 is plenty.)

Set your variables again (only the first line to edit), reusing the **same plan name** as Challenge 1:

```bash
# macOS / Linux / Git Bash
FIRSTNAME=kevin            # ← the ONLY line to edit
RG=$FIRSTNAME
PLAN=${FIRSTNAME}plan         # the SAME plan you created in Challenge 1
UI_NAME=${FIRSTNAME}wineui    # the new Web App for the front-end
```

```powershell
# Windows (PowerShell)
$FIRSTNAME="frederic"         # ← the ONLY line to edit
$RG=$FIRSTNAME
$PLAN="${FIRSTNAME}plan"
$UI_NAME="${FIRSTNAME}wineui"
```

#### 6.1 Create the Web App — on your existing plan

```bash
az webapp create \
    -n $UI_NAME \
    -g $RG \
    -p $PLAN \
    --runtime "PYTHON:3.11"
```

🧠 **What does `create` do?** Same as for the API: it creates an **empty** Web App attached to your existing plan (`-p $PLAN`) — no new compute, no new cost. The app slot exists but has no code yet.

👀 **Go check in the portal**: open your App Service Plan → *Apps*. You should now see **two** Web Apps on it: your API and your UI. One machine, two applications.

#### 6.2 Configure how Azure starts Streamlit

```bash
# 1. Install requirements.txt when you deploy code
az webapp config appsettings set \
    -g $RG \
    -n $UI_NAME \
    --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true

# 2. The command that launches Streamlit
az webapp config set \
    -g $RG \
    -n $UI_NAME \
    --startup-file "python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0"
```

🧠 **What does this do?** Same logic as the API, different server. Locally, `streamlit run app.py` listens on port 8501 on your machine only. On Azure, the container expects the app on **port 8000** and reachable from outside the process (`--server.address 0.0.0.0`) — without these two flags the app would start but Azure could never reach it, giving endless "Application Error" pages. Compare with the API: gunicorn for FastAPI, streamlit for the front-end — the startup command is where each app declares how it runs.

#### 6.3 Deploy your code

```bash
cd # Gets back to the $HOME directory
cd Documents/GitHub/yourwineui

az webapp up \
    -n $UI_NAME \
    -g $RG \
    -p $PLAN \
    --runtime "PYTHON:3.11"
```

🧠 **What does `up` do?** Where `create` made an empty app, `up` **packages the current folder** (mind the `cd`!) and uploads it: Azure installs your `requirements.txt` and (re)starts the app with your Startup Command. **`create` builds the house, `up` moves your furniture in.** First deployment takes a few minutes. ☕

👀 While it builds: portal → your Web App → *Deployment Center → Logs* and *Log stream*.

---
### 7. (Bonus) Finish the Continuous Integration with the tests

- Connect your UI Web App to GitHub from the portal, exactly as for the API: open your **UI Web App → Deployment Center** → Source: **GitHub** → authorize → select your organization, the `yourwineui` repository and the `master` branch → **Save**. Azure commits the workflow file and stores the deployment secret.

- In GitHub Desktop, `git pull` to get the generated `.yml` file.

- Open the `.yml` in VS Code and add the test step after the dependencies install — ⚠️ note the file name is `test_app.py` here, not `test_fast.py`:

```yaml
      - name: Install dependencies
        run: pip install -r requirements.txt

      # Optional: Add step to run tests here (PyTest, Django test suites, etc.)
      - name: Test with pytest
        run: pytest tests/test_app.py
```

- Save, commit, push, and watch the **Actions** tab: build → tests → deploy.

---
### 8. Test your Streamlit Web App

- Open your UI Web App's **Default domain** in a new tab. You should see the main page, as locally.

- Try different feature values and compare the predictions. 🍷 You now have a complete deployed product: a browser front-end on one Web App, calling your model API on another — both on the same machine.

🛠️🆘 **Troubleshooting**: blank page or "Application Error"? Check the **Log stream** first (is Streamlit starting? on which port?), verify your Startup Command, then restart:

```bash
az webapp restart -n $UI_NAME -g $RG
```

And if the page loads but predictions fail: the problem is probably the **API URL** in `app.py` — test it directly in your browser (`/docs`).

---
### 9. **Bonus**: Rebuild a new model with more features

- Try to recreate the whole process for the API and the Streamlit Web App with a model using more features. Remember you only need to modify the source code; if you set up CI/CD, the deployments happen automatically after the tests pass.

Well done! You have deployed your Web App to Azure with an MLOps approach. 🎉

---

### Don't forget to save your work!

Save your files: File > Save. Then close all the tabs in your browser and VS Code windows. You can safely close the Anaconda Prompt.

💡 Don't forget to **push your code to GitHub**

1. Open GitHub Desktop.
2. It should automatically detect any file with modifications. If not, ask a TA.
3. Make sure these files are ticked, and write a _commit message_ in the bottom left form.
4. Click on the "Commit to `master`" button at the bottom of the form.
5. Click on the "Push `origin`" button at the top of the window.

---
## 🥇 Key learning points
By the end of this exercise, you will have:
* Deployed a second Web App on your **existing App Service Plan**, understanding the App Service cost model (you pay for compute, not per app).
* Built a Streamlit front-end that consumes your model through its API.
* (Bonus) Automated tests and deployment with GitHub Actions.

That's it! Take a small break before diving into the next exercise.
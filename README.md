# AI-Autonomous-Surveillance-System

**Date:** 11/29/2024

## Available Material

This repository contains the project carried out for the Training Unit "Modeling of Multi-Agent Systems with Computer Graphics", which is part of the second course evidence. Below is an overview of the available materials and their locations:

### Unity
The graphics and simulation section project with Unity can be found in the following OneDrive link to a compressed folder:

[Unity Project Preview - OneDrive](https://tecmx-my.sharepoint.com/:u:/g/personal/a01637405_tec_mx/EYM0AAal919Oou-auaHc_5gB4rXpkf3mjAO46vPfBtEdyw?e=87H8Qu)

### Omniverse
An import from Unity and Demo look at the implementation of the project in conjunction with Nvidia Omniverse can be found at the following OneDrive link to a compressed folder:

[Omniverse Project Preview - OneDrive](https://tecmx-my.sharepoint.com/:u:/g/personal/a01068505_tec_mx/EeCkjnGrlytJhm7z5zn7U7wBMsA5pjX_fyZUAW6pdd4-hw?e=iuQkb9)

### Agents’ Code & Computer Vision’s Code
The final codes for these services can be found directly in the project repository (previously attached). Likewise, the link can be found here again:

- `Agents`
- `Computer Vision`

### Documentation
Detailed documentation and workflow can be found at the following link to a Google Drive document:

[Documentation & Workflow - Google Drive](https://docs.google.com/document/d/1CG0gDy-nMS0_nWzAFrbZyQxMkf7I-CueW6UiskvcWE8/edit?usp=sharing)

## Demonstration

A demonstration video showcasing the functionality of the simulation is available on YouTube: 

[YouTube - Simulation Demonstration](https://youtu.be/7nxhV7HlYU4)

## Environment Setup

To configure the development and execution environment for the project, follow the steps below:

### 1\. Unity

1.  **Download and Install Unity HUB:**

    -   Visit the [official Unity website](https://unity.com/download) and download the Unity Hub installer.
    -   Run the downloaded installer and follow the instructions to install the app, which facilitates managing different Unity versions.
    
2.  **Install the Required Unity Version:**

    -   Open Unity Hub.
    -   Go to the **Installs** tab.
    -   Click on **Add** and select the specific version required for the project `Unity 2022.3.52f1`
    -   Follow the instructions to complete the installation.

### 2\. Python

1.  **Download Python:**

    -   Visit the [official Python website](https://www.python.org/downloads/) and download the latest version available for Python.
  
2.  **Install Python:**

    -   Run the downloaded installer.
    -   During installation, ensure that the **"Add Python to PATH"** option is checked.
    -   Follow the instructions to complete the installation.
  
3.  **Verify the Installation:**

    -   Open a terminal or command prompt.
    -   Run `python --version` to confirm that Python is installed correctly.

### 3\. Installing Libraries from `requirements.txt`

1.  **Clone the Repository:**

    -   If you haven't already, clone this repository to your local machine. Using:
      
        ```
        git clone https://github.com/alexeiddg/AI-Autonomous-Surveillance-System.git
        ```
        ... in the rute of your preference.
    
2.  **Create a Virtual Environment (Optional but Recommended):**

    -   Navigate to the project directory.
    -   Run `python -m venv env` to create a virtual environment named `env`.
    -   Activate the virtual environment:
        -   On Windows: `env\Scripts\activate`
        -   On macOS/Linux: `source env/bin/activate`
    
3.  **Install Dependencies:**

    -   Ensure you are in the main directory of the cloned repository, where the `requirements.txt` file is located.
    -   Run the following command to install all necessary libraries:

        ```        
        pip install -r requirements.txt`
        ```
4.  **Verify the Installation:**

    -   After installation, you can verify that all libraries have been installed correctly by running `pip list`.

### 4\. Optional Setup: Nvidia Omniverse and Localhost Application

1\.  **Download and Install Nvidia Omniverse:**

    -   Visit the [Nvidia Omniverse website](https://www.nvidia.com/en-us/omniverse/) and download the Omniverse Launcher.

    -   Run the installer and follow the instructions to set up the Omniverse platform.

2\.  **Install Omniverse Kit:**

    -   Open the Omniverse Launcher.

    -   Navigate to the **Exchange** section.

    -   Search for the "Omniverse Kit" and install it. This is a toolkit for building advanced applications which is going to be used as our environment to vizualize the Omniverse Import Project.

-   **Set Up the Nucleus Server:**

    -   Open the Omniverse Launcher and go to the **Nucleus** tab.

    -   In the file explorer type interface, navigate to **Omniverse**.

    -   Click on **Create Local Server**.

    -   Follow the on-screen instructions to finish configuring the localhost server.

    -   This directory is where you will import the project.

## Run the Project

### Instructions

1.  **Download the Unity Project:**

    -   Download the compressed Unity project folder from the OneDrive link provided in the **Available Materials** section of this README.

2.  **Add the Project to Unity Hub:**

    -   Extract the downloaded folder to your preferred location.

    -   Open Unity Hub.

    -   Click on the **Add** button.

    -   Navigate to the extracted folder and select it to add the project to Unity Hub.

3.  **Start Python Servers:**

    -   Open a terminal in the root directory of the cloned repository.

    -   Run the following commands to start the Python servers for the Agent and Computer Vision:

        ```
        python "Computer Vision/cv_server.py"
        python Agents/agents.py
        ```

4.  **Run the Unity Simulation:**

    -   Ensure both servers are running.

    -   In Unity Hub, open the project and press the **Play** button to start the simulation.

5.  **Simulation Controls:**

    -   **Switch Camera/View:** Press the `Space` key.

    -   **Drone Controls:**

        -   Press `R` to switch to manual mode.

            -   Use `W`, `A`, `S`, `D` keys to move.

            -   Use `Shift` + `Space` to ascend or descend.

        -   Press `L` to return to automatic mode.

### NVIDIA Omniverse Demo

1.  **Download the Omniverse Demo Project:**

    -   Download the compressed Omniverse project folder from the OneDrive link provided in the **Available Materials** section of this README.

2.  **Extract and Set Up the Project:**

    -   Extract the downloaded folder to your preferred location.

    -   Follow the Omniverse installation guide provided in the project folder to set up the environment.

3.  **Run the Omniverse Demo:**

    -   Launch the Omniverse application.

    -   Open the extracted project folder within the application.

4.  **Explore the Demo:**

    -   Use the provided controls or features to interact with the simulation and explore its functionalities.

--------
Feel free to explore and provide feedback!

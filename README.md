# Phishing Email Detector

Defense security tool combining Python script and LLM driven analysis to identify and explain phishing threats.

## Overview
This is a defender tool designed to analyze emails to look for social engineering cues, suspicious headers, and other anomalies. This project is designed to provide a brief reasoning with a reasoning layer to try to understand why an email is malicious or suspicious, providing a risk score and recommendations, while also providing a simple GUI for easy to use educational purposes.

## Scope and Target
* **Target:** The target for this tool is educational environments, as the tool is designed for learning purposes only and not real world automation services.
* **Scope:** The scope of our tool is within the analysis of raw emails with a focus on identifying suspicious texts and actions. 
* **Out of Scope:** In accordance with our authorized target, any email not from a public data set, instructor provided, or generated (if permitted) is considered to be out of scope.

## Setup Plan
* ### Environment Initialization
  * Clone repositories and setup Python 3.x environment.
  * Install any and all required dependencies for text parsing and GUI rendering.

* ### Configurations
  * Configure connection to a reasoning engine. This may involve setting an environment variable for an API key or to a local model endpoint, if hosting it internally.

* ### Execution
  * Launch application via the main python script to startup the GUI.
  * Load our email samples for analysis and scoring.

## Tools
* **Language:** Python 3.x
* **Reasoning Engine:** An integrated large language model (LLM) tasked with handling analysis and social engineering cues.
* **Interface:** Python GUI framework for simple user interaction and visualization.

---

## Project Direction

* ### 1st Phase
  * Establish a python environment and building a prefilter to determine "hard flags".

* ### 2nd Phase
  * Connect prefilter results with a reasoning engine, and focus on synthesising our information to create a risk score for a possible phishing email.

* ### 3rd Phase
  * Test our program against datasets and aim for approximately 80 percent accuracy, and create a report and presentation based on our findings.
* ### 3rd Phase
  * Test our program against datasets and aim for approximately 80 percent accuracy, and create a report and presentation based on our findings.

# Image-to-Table Converter

## Overview

The **Image-to-Table Converter** is a Python3-based application that processes images of tables and converts them into a structured CSV file format. This tool is designed to help users quickly and accurately extract tabular data from images, improving productivity and reducing manual effort. The application also includes a web interface, making it easy to upload images and download the corresponding CSV files. The project is built using Python, Flask, and deployed on Vercel.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Web Interface](#web-interface)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Image to CSV Conversion**: Converts images of tables into CSV format with accurate extraction of rows and columns.
- **Web Interface**: Simple and intuitive web interface for uploading images and downloading CSV files.
- **CSV Management**: Stores generated CSV files for download, ensuring easy access and retrieval.
- **Modular Codebase**: The code is structured for easy maintenance and further expansion.
- **Python & Flask**: Built using Flask for the backend and deployed on Vercel for easy access and scalability.

## Project Structure

The project is organized as follows:

```bash
Image-to-Table Converter/
├── generated_csv/               # Directory for storing generated CSV files
│   ├── Screenshot_from_2024-07-11_23-21-13.csv
│   ├── a21b07f9-9b8a-4dfe-8857-de8349fd9aca.csv
│   └── text_model.csv
├── static/                      # Static files for the web interface
│   ├── homepage.css             # CSS file for the homepage design
│   └── script.js                # JavaScript file for interactivity
├── templates/                   # HTML templates
│   └── homepage.html            # Homepage HTML template
├── app.py                       # Main application file (Flask app)
├── modularise.py                # Contains the core image-to-CSV logic
├── requirements.txt             # Python dependencies
├── vercel.json                  # Configuration for Vercel deployment
└── README.md                    # Project documentation
```

## Requirements
To run the project locally, ensure tat you have the following installed:

- **Python 3.x**
- **Flask**: as a web framework
- **OpenCV**: for image processing
- **NumPy**: for matrix operations
- **Pandas**: for CSV manipulation

All dependencies are listed in the requirements.txt file

## Installation

- **Clone the repository**:
```bash
git clone https://github.com/PcNerd9/Alx-portfolio-project.git
cd Alx-portfolio-project
```

- **Install dependencies**:
```bash
pip install -r requirements.txt
```

- **Run the application**:
```bash
python3 app.py
```

- **Access the application**: Open your web browser and navigate to: *http://0.0.0.0:5000*


## Usage
### Web Interface
- **Upload Image**: Navigate to the homepage, where you can upload an image of a table that you want to convert into a CSV file.

- **Conversion Process**: Once uploaded, the image will be processed by the backend, and the table's data will be extracted and saved in CSV format.

- **Download CSV**: After conversion, you will be provided with a link to download the generated CSV file.

## Web Interface
The web interface is simple and user-friendly:

- **Homepage**: Upload an image of a table using the provided form.
- **Download**: After successful processing, the converted CSV file can be downloaded directly from the interface.
The design is managed using the static/homepage.css file, and the logic is handled by script.js.

## Deployment
This application is deployed on Vercel. The configuration for deployment is provided in the vercel.json file.

To deploy it yourself:

- Install the Vercel CLI:

```bash
Copy code
npm i -g vercel
```
- Run the deployment:

```bash
vercel
```
Follow the prompts to deploy the application.

## Contributing
Contributions are welcome! If you have any ideas, features, or bugs to report, feel free to open an issue or submit a pull request.

Here’s how you can contribute:

1.  Fork the repository.
2.  Create a new branch (git checkout -b feature-branch).
3.  Make your changes.
4.  Commit your changes (git commit -m 'Add some feature').
5.  Push to the branch (git push origin feature-branch).
6.  Open a pull request

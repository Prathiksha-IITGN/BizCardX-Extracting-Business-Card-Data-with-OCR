Business Card OCR
This is a Streamlit app for extracting information from business card images using OCR. The app allows users to upload an image of a business card and extract information such as the person's name, designation, company, mobile number, email, website URL, area, city, state, and pin code. The extracted information is displayed in a table and can be saved to a SQLite database.

Requirements:
The requirements for running the Business Card OCR application are as follows:

Python 3.6 or higher
Streamlit
Numpy
OpenCV (cv2)
EasyOCR
SQLite3

Installation:
To run the app locally, follow these steps:

1.Clone the repository
2.Install the requirements: pip install -r requirements.txt
3.Run the app: streamlit run app.py

Usage:
To use the app, simply upload an image of a business card by clicking on the "Upload a business card image" button. Once the image is processed, the extracted information will be displayed in a table. To save the information to the database, click on the "Save" button.
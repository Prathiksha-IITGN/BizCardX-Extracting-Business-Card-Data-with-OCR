# -*- coding: utf-8 -*-
"""Untitled29.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f0UpO1jMwy2eiWXOYp1De9HQHkR5IR_D
"""

# !pip install streamlit
# !pip install easyocr
# !pip install sqlalchemy

import streamlit as st
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import easyocr
import sqlite3

# Set up database
conn = sqlite3.connect('business_cards.db')

# Create table if it does not exist
with conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS business_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            designation TEXT,
            company TEXT,
            mobile_number TEXT,
            email TEXT,
            website_url TEXT,
            area TEXT,
            city TEXT,
            state TEXT,
            pin_code TEXT,
            image BLOB
        )
    """)

# Set up Streamlit app
st.set_page_config(page_title='Business Card OCR', page_icon=':credit_card:', layout='wide')

st.title('Business Card OCR')

# Upload image and extract information
uploaded_file = st.file_uploader('Upload a business card image', type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Process the uploaded image
    image = Image.open(uploaded_file)
    with st.spinner('Processing...'):
        # Convert the image to an array
        img_array = np.array(image)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Apply adaptive thresholding
        threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Invert the thresholded image
        threshold = cv2.bitwise_not(threshold)

        # Convert the thresholded image back to PIL format
        pil_image = Image.fromarray(threshold)

        # Apply OCR
        reader = easyocr.Reader(['en'])
        results = reader.readtext(np.array(pil_image))

        # Extract information
        name = None
        designation = None
        company = None
        mobile_number = None
        email = None
        website_url = None
        area = None
        city = None
        state = None
        pin_code = None
        for result in results:
            text = result[1]
            if name is None and len(text.split()) >= 2:
                name = text
            elif designation is None and any(word in text.lower() for word in ['ceo', 'cto', 'cfo', 'coo','Director','Manager','Executive']):
                designation = text
            elif company is None and len(text) > 3:
                company = text
            elif mobile_number is None and text.isdigit() and len(text) == 10:
                mobile_number = text
            elif email is None and '@' in text:
                email = text
            elif website_url is None and ('www.' in text or 'http' in text):
                website_url = text
            elif area is None and len(text) > 3:
                area = text
            elif city is None and len(text) > 3:
                city = text
            elif state is None and len(text) > 3:
                state = text
            elif pin_code is None and text.isdigit() and len(text) == 6:
                pin_code = text

        # Display the information using Streamlit widgets
      
        st.write('## Extracted Information')
        info_table = [['Field','Value']]
        if name is not None:
            info_table.append(['Name', name])
        if designation is not None:
            info_table.append(['Designation', designation])
        if company is not None:
            info_table.append(['Company', company])
        if mobile_number is not None:
                info_table.append(['Mobile Number', mobile_number])
        if email is not None:
          info_table.append(['Email', email])
        if website_url is not None:
          info_table.append(['Website', website_url])
        if area is not None:
          info_table.append(['Area', area])
        if city is not None:
          info_table.append(['City', city])
        if state is not None:
          info_table.append(['State', state])
        if pin_code is not None:
          info_table.append(['Pin Code', pin_code])

        st.table(info_table)

        # Save the information to the database
        if st.button('Save'):
          with conn:
            conn.execute("""
               INSERT INTO business_cards (
                    name,
                    designation,
                    company,
                    mobile_number,
                    email,
                    website_url,
                    area,
                    city,
                    state,
                    pin_code,
                    image
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                designation,
                company,
                mobile_number,
                email,
                website_url,
                area,
                city,
                state,
                pin_code,
                uploaded_file.read()
            ))

        st.success('Business card information saved successfully.')
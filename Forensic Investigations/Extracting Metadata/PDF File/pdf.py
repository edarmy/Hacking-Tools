#!/bin/python3
# Author: DEAD ARMY
# Version: 0.1
# Date: 2024-10-30
# Description: Extracting PDF Metadata with formatted dates
# Usage: python3 script_name.py pdf_file

import sys
import pikepdf
from datetime import datetime, timedelta

def parse_pdf_date(date_str):
    """Parse PDF date string in the format D:YYYYMMDDHHmmSS+02'00' and convert to datetime."""
    try:
        if date_str.startswith("D:"):
            date_str = date_str[2:]  # Remove 'D:' prefix
        
        # Split the date and timezone
        date_part, tz_part = date_str[:14], date_str[14:]

        # Create a datetime object from the date part
        dt = datetime.strptime(date_part, "%Y%m%d%H%M%S")

        # Parse the timezone offset
        if tz_part:
            tz_hours = int(tz_part[1:3])  # +02
            tz_minutes = int(tz_part[4:6])  # '00'
            tz_delta = timedelta(hours=tz_hours, minutes=tz_minutes)

            # Apply the timezone offset
            if tz_part[0] == '-':
                dt -= tz_delta
            else:
                dt += tz_delta

        return dt
    except ValueError:
        return date_str  # Return the original if parsing fails

def pdf_metadata(pdf_file):
    try:
        pdf = pikepdf.Pdf.open(pdf_file)  # Open the PDF file
        metadata = dict(pdf.docinfo)      # Extract metadata as a dictionary
        
        # Convert creation and modification dates if present
        if "/CreationDate" in metadata:
            metadata["/CreationDate"] = parse_pdf_date(metadata["/CreationDate"])
        if "/ModDate" in metadata:
            metadata["/ModDate"] = parse_pdf_date(metadata["/ModDate"])
        
        return metadata
    except Exception as e:
        print(f"Error: Unable to read PDF metadata. {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 script_name.py pdf_file")
        sys.exit(1)

    pdf_file = sys.argv[1]
    metadata = pdf_metadata(pdf_file)

    if metadata:
        print("PDF Metadata:")
        for key, value in metadata.items():
            print(f"{key}: {value}")

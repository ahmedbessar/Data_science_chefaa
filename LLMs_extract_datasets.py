import os
import PyPDF2
import csv
import openai
from config import OPENAI_API_KEY

# Set up the OpenAI API
openai.api_key = OPENAI_API_KEY

def extract_data_from_pdf(pdf_file):
    # Get the current working directory
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")

    # Check if the PDF file is in the current directory
    pdf_path = os.path.join(cwd, pdf_file)
    if os.path.isfile(pdf_path):
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(file)

            # Extract the text from the PDF
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ''

        # Debug: Print extracted text (optional, can be very verbose)
        print(f"Extracted text:\n{text[:500]}...")

        # Use GPT-3.5-turbo to identify and extract the datasets
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Please identify and extract the two datasets in the following text:\n\n{text}"}
            ],
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Debug: Print the GPT-3.5-turbo response
        print(f"GPT-3.5-turbo response:\n{response.choices[0].message['content']}")

        # Parse the GPT-3.5-turbo response to extract the dataset examples
        dataset_examples = response.choices[0].message['content'].strip().split("\n\n")

        # Save the dataset examples to separate CSV files
        for i, dataset_example in enumerate(dataset_examples):
            with open(f"dataset_{i+1}.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # Split by rows first, then split each row by commas
                rows = [row.strip().split(",") for row in dataset_example.strip().split("\n")]
                writer.writerows(rows)
            print(f"Dataset {i+1} saved to dataset_{i+1}.csv")
    else:
        print(f"Error: {pdf_file} not found in the current directory.")

# Example usage
extract_data_from_pdf('Data_science.pdf')

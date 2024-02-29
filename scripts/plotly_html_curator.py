import sys
from bs4 import BeautifulSoup
import re
import os

def truncate_floats_and_arrays_and_rgb(input_html_file):
    # Extract the filename and extension
    filename, ext = os.path.splitext(input_html_file)
    output_html_file = f"{filename}_modified.html"

    with open(input_html_file, 'r') as input_file:
        soup = BeautifulSoup(input_file, 'html.parser')
        
        # Remove all h1 tags
        for h1_tag in soup.find_all('h1'):
            h1_tag.extract()

        # Find all script tags containing Plotly plots
        script_tags = soup.find_all('script')
        
        for tag in script_tags:
            # Check if the script contains Plotly initialization code
            if 'Plotly.newPlot' in tag.text:
                # Use regex to find and truncate floating-point numbers to 3 decimals
                modified_script = re.sub(r'(\d+\.\d{3})\d+', r'\1', tag.text)

                # Convert long arrays of zeros to "black" string
                modified_script = re.sub(r'\[\[\s*0\.0+\s*(,\s*0\.0+)*\s*\]\s*(,\s*\[\s*0\.0+\s*(,\s*0\.0+)*\s*\]\s*)*\]', '"black"', modified_script)
                
                # Replace "rgb(a, b, c)" with [a, b, c]
                modified_script = re.sub(r'"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"', r'[\1, \2, \3]', modified_script)
                
                # Convert multiple consecutive spaces to a single space
                modified_script = re.sub(r'\s{2,}', ' ', modified_script)

                # Remove unnecessary spaces between comma-separated values
                modified_script = re.sub(r',\s*', ',', modified_script)
                
                # Replace the original script with the modified one
                tag.string.replace_with(modified_script)
                
    # Write the modified HTML to the output file
    with open(output_html_file, 'w') as output_file:
        output_file.write(str(soup))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_html_file")
        sys.exit(1)

    input_html_file_path = sys.argv[1]
    truncate_floats_and_arrays_and_rgb(input_html_file_path)

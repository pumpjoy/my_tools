''' Load Text
import os

def load_text_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

data_dir = os.path.join(os.getcwd(), 'data')
file_path = os.path.join(data_dir, 'example.txt')

# Load the text file
data_content = load_text_file(file_path)
print(data_content)
'''



''' Load csv
# !pip install pandas
import pandas as pd

def load_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

data_dir = os.path.join(os.getcwd(), 'data')
file_path = os.path.join(data_dir, 'example.csv')


# Load the CSV file
df = load_csv_file(file_path)
print(df)
'''

''' Load Image
import os

def load_image_file(file_path):
    image = Image.open(file_path)
    return image

data_dir = os.path.join(os.getcwd(), 'data')
file_path = os.path.join(data_dir, 'example.png')

# Load the image file
image = load_image_file(file_path)
image.show()'''
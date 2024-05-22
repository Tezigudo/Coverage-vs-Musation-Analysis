import os
from bs4 import BeautifulSoup
import pandas as pd


def parse_index_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    
    data = []
    table = soup.find_all('table')
    if not table or len(table) < 2:
        return data
    rows = table[1].tbody.find_all('tr')

    for row in rows[1:]:  # Skip the header row
        cells = row.find_all('td')

        try:
            if len(cells) >= 3:
                
                class_name = cells[0].a.text.strip()
                line_coverage = cells[1].find('div', class_='coverage_percentage').text.strip('% ')
                mutation_coverage = cells[2].find('div', class_='coverage_percentage').text.strip('% ')
                data.append({
                    'Class Name': class_name,
                    'Line Coverage (%)': float(line_coverage),
                    'Mutation Coverage (%)': float(mutation_coverage)
                })

        except Exception as e:
            continue
    return data

def collect_data_from_reports(report_directory):
    all_data = []
    for root, _, files in os.walk(report_directory):
        for file in files:
            if file == 'index.html':
                file_path = os.path.join(root, file)
                data = parse_index_html(file_path)
                all_data.extend(data)
    return all_data

# Specify the path to the PIT reports directory
report_directory = '/Users/god/Desktop/MyFolder/Programming/naist/algorithm-java/target/pit-reports/'
report_data = collect_data_from_reports(report_directory)

df = pd.DataFrame(report_data)
df.to_csv('mutation_coverage_data.csv', index=False)
print(df)

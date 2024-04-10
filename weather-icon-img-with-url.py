import requests
import json
import csv


# URL of the webpage containing the JSON data
#url = 'https://github.com/yosiefTecleab/sample_data_set/tree/main/weather-images'
url='https://github.com/yosiefTecleab/sample_data_set/tree/main/img'

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the content of the script tag containing JSON data
    start_index = response.text.find('<script type="application/json" data-target="react-app.embeddedData">')
    end_index = response.text.find('</script>', start_index)
    json_data = response.text[start_index:end_index]
    
    # Parse the JSON data
    json_data = json_data.split('>', 1)[-1]  # Remove the <script> tag
    json_data = json_data.strip()  # Remove leading/trailing whitespace
    json_data = json.loads(json_data)

    payload = json_data['payload']
    path_or_folder = payload['path']
    repo_info = payload['repo']['ownerLogin']
    branch_name=payload['repo']['defaultBranch']
    repo_name=payload['repo']['name']
   

    #url link e.g https://raw.githubusercontent.com/yosiefTecleab/sample_data_set/main/img/cloudy.png
    #url_img=f'https://raw.githubusercontent.com/{repo_info}/{repo_name}/{branch_name}/{path_or_folder}/{name}'

    # Extract names of the image files
    tree_items = json_data['payload']['tree']['items']
    image_names = [item['name'] for item in tree_items if item['contentType'] == 'file']
    
    icon_list={}
    line=''
    # Print the image names
    count=0
    for name in image_names:

        img=name.replace('.png','')
        url=f'https://raw.githubusercontent.com/{repo_info}/{repo_name}/{branch_name}/{path_or_folder}/{name}'

        icon_list[img]=url
        line+=f'{img},{url}\n'
        #print(name)
    #print(icon_list)
    #print(line)
    with open('weather-icon-img-with-url.csv','w')as f:
        f.write(line)

else:
    print("Failed to fetch webpage. Status code:", response.status_code)

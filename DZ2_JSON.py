import os
import json

for filename in os.listdir("JSONFiles"):
   with open(os.path.join("JSONFiles", filename), 'r') as f:
       match filename:
           case "services_1.json":
               text = f.read()
               print(filename)
               #print(text)
               json_record = json.loads(text)
               for txt in json_record['services']:  # создали цикл, который будет работать построчно
                   print(txt['id'], ':', txt['name'], ':', txt['code'], ':', txt['createdAt'])
           case "services_2.json":
               text = f.read()
               print(filename)
               #print(text)
               json_record = json.loads(text)
               for txt in json_record['accountServices']:  # создали цикл, который будет работать построчно
                   print(txt['serviceName'], ':', txt['serviceCode'])
           case "services_3.json":
               print(filename)
           case _:
               print(f'unknown file {filename}')
       #text = f.read()
       #print(filename)
       #print(text)
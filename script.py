import os
from py_files.tools import mapFiles, createDataTypes, addDataToPerson, publishToWorkbook, backup
from py_files.DataType1 import DataType1

""" set to true to backup files before proceeding """
bbackup = True

# backup files
if bbackup:
    backup(os.path.join(os.getcwd(), 'maer_raw'))

# gather the names of all the files and their parent folder (only 1 level deep)
directory = mapFiles(os.path.join(os.getcwd(), "maer_raw"))

# go through R1 P1 files and create DataType objects, store them in list
listofData = []
for key in directory:
    if key == "R1 P1":
        for file in directory[key]:
            listofData += createDataTypes(0, os.path.join(os.getcwd(), 'maer_raw', key, file), expName=key)
    elif "R1 P1" in key:
        print(key)

# go through listofData and add them to a Person object; maintain list of Person objects
listofPeople = addDataToPerson(listofData, [])

# # print list of people
# for person in listofPeople:
#     print("{} has {} pieces of data".format(person.id, len(person.data1)))
# print("\n{} people have {} pieces of data, total\n".format(len(listofPeople), len(listofPeople)*12))
# print(listofData[0])

# # add people to experiment
# exp = Experiment("R1 P1", listofPeople)

# create header row
DataType1.unique_id_list.sort()
rows = [[]]
rows[0] = ("participant", "date", "expName")
for id in DataType1.unique_id_list:
    rows[0] += ("prt_1_vas.response_raw_i{}".format(id), "prt_1_vas.rt_raw_i{}".format(id),
                "prt_image_intens_resp.keys_raw_i{}".format(id), "prt_image_intens_resp.rt_raw_i{}".format(id),
                "prt_order_i{}".format(id))

# append a row for each participant
for person in listofPeople:
    person.sortData()
    row = (person.id, person.data1[0].date, person.data1[0].experiment)
    for data in person.data1:
        row += data.getAllFields()
    rows.append(row)

# write to excel worksheet
name = "maer_auto"
publishToWorkbook(name, rows)
from pymongo import MongoClient

def main():
    itchy_trigger_finger_niggers = True
    while itchy_trigger_finger_niggers:
        # chossing option to do CRUD operations
        selection = input('Select\n'
                          '1 to insert,\n'
                          '2 to update,\n'
                          '3 to read,\n'
                          '4 to delete,\n'
                          'exit to exit\n')

        if selection == '1':
            insert()
        elif selection == '2':
            update()
        elif selection == '3':
            read()
        elif selection == '4':
            delete()
        elif selection == 'exit':
            break
        else:
            print('\n INVALID SELECTION \n')


def insert():
    try:
        flavoringName = input('Enter the Flavoring name :')
        flavoringProducer = input('Enter the flavoring Producer :')
        db.Flavorings.insert_one(
            {
                flavoringName: {
                    "producer": flavoringProducer
                }
            })
        print('Data inserted successfully')
    except Exception as e:
        print('funk')
        print(str(e))


def update():
    try:
        criteria = input('Enter id to update')
        flavoringName = input('Enter the Flavoring name :')
        flavoringProducer = input('Enter the flavoring Producer :')
        db.Flavorings.update_one(
            {"_id": criteria},
            {
                "$set": {
                    flavoringName: {
                        "producer": flavoringProducer
                    }
                }
            })
        print('Data updated successfully')
    except Exception as e:
        print('funk')
        print(str(e))

def read():
    try:
        empCol = db.Flavorings.find()
        print('\n All data from Flavorings Database \n')
        for emp in empCol:
            print(emp)

    except Exception as e:
        print(str(e))


def delete():
    try:
        criteria = input('Enter id to update')
        db.Flavorings.delete_many({"_id": criteria})
        print('Deletion successfully')
    except Exception as e:
        print('funk')
        print(str(e))


client = MongoClient()  # 'localhost:27017'
db = client.test_1
main()

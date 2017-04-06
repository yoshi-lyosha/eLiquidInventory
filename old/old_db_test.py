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
        flavoring_name = input('Enter the Flavoring name :')
        flavoring_producer = input('Enter the flavoring Producer :')
        db.Flavorings.insert_one(
            {
                    "flavoringName": flavoring_name,
                    "producer": flavoring_producer
            })
        print('Data inserted successfully')
    except Exception as e:
        print(str(e))


def update():
    try:
        flavoring_name = input('Enter the Flavoring name :')
        flavoring_producer = input('Enter the flavoring Producer :')
        new_flavoring_name = input('Enter the new Flavoring name :')
        new_flavoring_producer = input('Enter the new flavoring Producer :')
        db.Flavorings.update_one(
            {
                "flavoringName": flavoring_name,
                "producer": flavoring_producer
            }, {
                "$set": {
                    "flavoringName": new_flavoring_name,
                    "producer": new_flavoring_producer
                }
            })
        print('Data updated successfully')
    except Exception as e:
        print(str(e))


def read():
    try:
        json_all_db = db.Flavorings.find()
        print('\n All data from Flavorings Database \n')
        for string in json_all_db:
            print(string)
    except Exception as e:
        print(str(e))


def delete():
    try:
        flavoring_name = input('Enter flavoring name to delete\n')
        flavoring_producer = input('Enter flavoring producer to delete\n')
        result = db.Flavorings.delete_many({
            "flavoringName": flavoring_name,
            "producer": flavoring_producer})
        print('Items deleted: ', result.deleted_count)
    except Exception as e:
        print(str(e))


client = MongoClient()  # 'localhost:27017'
db = client.test_1
main()

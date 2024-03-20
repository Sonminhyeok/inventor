import datetime


def get_data_by_name(df,name,column):
    return list(filter(lambda item : item['name'] == name, df))[0][column]

# def get_datetime_by_name(df,name,time="start"):
#     return datetime.datetime.strptime(list(filter(lambda item : item['name'] == name, df))[0][time],"%Y-%m-%d")
def get_datetime_by_applicant(record_list, applicant, time):
    for record in record_list:
        if record['applicant'] == applicant:
            return datetime.datetime.strptime(record[time], "%Y-%m-%d")
    return None
def str_to_datetime(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")
def datetime_to_str(date):
    return datetime.datetime.strftime(date,"%Y-%m-%d")

def find_common_item(address, previous_address):
    address_list=address.split("|")
    previous_address_list=previous_address.split("|")
    common_address_list=[]
    
    for address1 in address_list:
        for address2 in previous_address_list:
            if address1 == address2:
                common_address_list.append(address1)
    if common_address_list:
        common_address= "|".join(common_address_list)
        return common_address
    else:
        return "No"

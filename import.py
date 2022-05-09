from mastersxml import mastersxml
from vouchersxml import vouchersxml
import requests
headers = {"Content-type": "text/xml;charset=UTF-8", "Accept": "text/xml"}


def print_menu():
    print ('1 -- Set server host' )
    print ('2 -- Set masters path' )
    print ('3 -- Set vouchers path' )
    print ('4 -- Request Import Masters' )
    print ('5 -- Request Import Vouchers' )
    print ('6 -- Request Import Masters => Vouchers' )
    print ('0 -- Print Menu' )
    print ('* -- Exit Script' )

if __name__=='__main__':
    host_url = 'http://localhost:9000'
    masters_uri = 'masters.csv'
    vouchers_uri = 'vouchers.csv'
    print_menu()
    while(True):
        option = ''
        try:
            option = int(input('#> '))
        except:
            print('Bye ...')
            exit()
        #Check what choice was entered and act accordingly
        if option == 0:
           print_menu()
        elif option == 1:
            host_url = input('Server Host: ')
            print(host_url)
        elif option == 2:
            masters_uri = input('Masters CSV: ')
            print(masters_uri)
        elif option == 3:
            vouchers_uri = input('Vouchers CSV: ')
            print(vouchers_uri)
        elif option == 4:
            response = requests.post(host_url, data=mastersxml(masters_uri), headers=headers)
            print(response.text)
            # print(mastersxml(masters_uri))
        elif option == 5:
            response = requests.post(host_url, data=vouchersxml(vouchers_uri), headers=headers)
            print(response.text)
            # print(vouchersxml(vouchers_uri))
        elif option == 6:
            response = requests.post(host_url, data=mastersxml(masters_uri), headers=headers)
            print(response.text)
            response = requests.post(host_url, data=vouchersxml(vouchers_uri), headers=headers)
            print(response.text)            
            # print(mastersxml(masters_uri))
            # print(vouchersxml(vouchers_uri))
        else:
            print('Bye ...')
            exit()

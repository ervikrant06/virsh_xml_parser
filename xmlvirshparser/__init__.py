import xmltodict
import pprint
import collections
import sys
import argparse
from prettytable import PrettyTable
from prettytable import ALL as ALL
x=PrettyTable(hrules=ALL)
y=PrettyTable()

x.field_names=['name','domain-id','instance-uuid','instance-name','flavor','image-id','infac-cnt','infac-details','disk-cnt','disk-details']
x.align="l"


def extracting_vm_info(doc, list1):
    '''
    Extract the VM information like name, domainid, nova instance UUID, etc..
    '''
    list1.append(doc['domain']['name'])
    list1.append(doc['domain'].get('@id','Not-Running'))
    list1.append(doc['domain']['sysinfo']['system']['entry'][4]['#text'])
    list1.append(doc['domain']['metadata']['nova:instance'].get('nova:name'))
    list1.append(doc['domain']['metadata']['nova:instance']['nova:flavor']['@name'])
    if doc['domain']['metadata']['nova:instance'].get('nova:root'):
        list1.append(doc['domain']['metadata']['nova:instance']['nova:root'].get('@uuid'))
    else:
        list1.append("None")
    '''
    Reserve for future usage
    '''
    #for key,value in doc['domain']['metadata']['nova:instance']['nova:flavor'].items():
    #    list1.append(value)

    #list1.append(doc['domain']['metadata']['nova:instance']['nova:owner']['nova:user']['@uuid'])
    #list1.append(doc['domain']['metadata']['nova:instance']['nova:owner']['nova:project']['@uuid'])
    return(list1)


def number_of_interfaces(doc, list1):
    '''
    Calculate the number of interfaces
    '''
    if type(doc['domain']['devices']['interface']) == collections.OrderedDict:
        return(list1.append(int(1)))
    else:
        return(list1.append(len(doc['domain']['devices']['interface'])))
    

def number_of_disks(doc, list1):
    '''
    Calculate the number of disks
    '''
    if type(doc['domain']['devices']['disk']) == collections.OrderedDict:
        return(list1.append(int(1)))
    else:
        return(list1.append(len(doc['domain']['devices']['disk'])))
    

def interface_details(doc, list1):
    '''
    Capture the interface details in list. if/else condition is used to avoid
    the failure of code when only one interface is attached to a VM. 
    '''
    if type(doc['domain']['devices']['interface']) == collections.OrderedDict:
        list_of_interfaces=[]
        '''
        Nested loop to check whether interface is DPDK or SRIOV based.
        Depending upon it, add the information to list
        '''
        if doc['domain']['devices']['interface'].get('@type') in ['vhostuser','hostdev']:
            list_of_interfaces=[doc['domain']['devices']['interface'].get('@type'),
                                doc['domain']['devices']['interface']['mac'].get('@address'),
                               ]
            list1.extend([list_of_interfaces])
        else:
            list_of_interfaces=[doc['domain']['devices']['interface'].get('@type'),
                                doc['domain']['devices']['interface']['mac'].get('@address'),
                                doc['domain']['devices']['interface']['target'].get('@dev'),
                               ]
            list1.extend([list_of_interfaces])
    else:
        _combining_lists=[]
        for number_of_interface in range(0,len(doc['domain']['devices']['interface'])):
            list_of_interfaces=[]
            if doc['domain']['devices']['interface'][number_of_interface].get('@type') in ['vhostuser','hostdev']:
                list_of_interfaces=[doc['domain']['devices']['interface'][number_of_interface].get('@type'),
                                    doc['domain']['devices']['interface'][number_of_interface]['mac'].get('@address'),
                                   ]
            else:
                list_of_interfaces=[doc['domain']['devices']['interface'][number_of_interface].get('@type'),
                                    doc['domain']['devices']['interface'][number_of_interface]['mac'].get('@address'),
                                    doc['domain']['devices']['interface'][number_of_interface]['target'].get('@dev')
                                   ]
            _combining_lists.extend([list_of_interfaces])
        list1.extend([_combining_lists])
    return(list1)


def disk_details(doc, list1):
    '''
    Capture the disk details in list. if/else condition is used to avoid
    the failure of code when only one disk is used to spawn a VM.
    '''
    if type(doc['domain']['devices']['disk']) == collections.OrderedDict:
        list_of_disks=[]
        list_of_disks=[doc['domain']['devices']['disk'].get('@type'),
                      doc['domain']['devices']['disk']['target'].get('@dev'),
                      doc['domain']['devices']['disk']['target'].get('@bus'),
                      doc['domain']['devices']['disk'].get('serial')
                      ]
        list1.extend([list_of_disks])
    else:
        _combining_lists=[]
        for number_of_disks in range(0,len(doc['domain']['devices']['disk'])):
            list_of_disks=[]
            list_of_disks=[doc['domain']['devices']['disk'][number_of_disks].get('@type'),
                           doc['domain']['devices']['disk'][number_of_disks]['target'].get('@dev'),
                           doc['domain']['devices']['disk'][number_of_disks]['target'].get('@bus'),
                           doc['domain']['devices']['disk'][number_of_disks].get('serial')
                          ]
            _combining_lists.extend([list_of_disks])
        list1.extend([_combining_lists])
    return(list1)


def main():
    # for loop to loop through all input file and call functions.
    for i in sys.argv[1:]:
        list1=[]
        with open(i) as fd:
            doc=xmltodict.parse(fd.read())
        extracting_vm_info(doc, list1)
        number_of_interfaces(doc, list1)
        interface_details(doc, list1)    
        number_of_disks(doc, list1)
        disk_details(doc, list1)
        '''
        Logic to change nested list separator from "," to "\n"
        e.g:
        From : 
    
        [
         [u'bridge', u'fa:16:3e:59:ba:21', u'virtio'],
         [u'bridge', u'fa:16:3e:a7:de:e7', u'virtio']
        ]
    
        To :-
    
        [
         [u'bridge', u'fa:16:3e:59:ba:21', u'virtio'\n
          u'bridge', u'fa:16:3e:a7:de:e7', u'virtio']
        ]
        '''
        for index,eachelement in enumerate(list1):
            if type(eachelement) == list:
                list1[index]=str(eachelement).replace('], [','\n')
        x.add_row(list1)
    print(x)

#FUNCTION_MAP={'detail_instance_information': []
#              'Instance_and_Network_information':
#              'Instance_and_disk_information':
#             }
#parser=argparse.ArgumentParser(description="Parse xml files")
#parser.add_argument('command',choices=FUNCTION_MAP.keys())
#parser.add_argument('xmlfiles',description="List of xml files")
#args=parser.parse_args()
#func=FUNCTION_MAP[args.command]
#func()

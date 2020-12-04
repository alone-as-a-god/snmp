from pysnmp import hlapi
import quicksnmp


quicksnmp.set('localhost', {'1.3.6.1.2.1.1.5.0': 'SNMPHost'}, hlapi.CommunityData('public'))


print(quicksnmp.get('localhost', ['1.3.6.1.2.1.1.5.0'], hlapi.CommunityData('public')))


its = quicksnmp.get_bulk_auto('localhost', [
    '1.3.6.1.2.1.2.2.1.2 ',
    '1.3.6.1.2.1.31.1.1.1.18'
    ], hlapi.CommunityData('public'), '1.3.6.1.2.1.2.1.0')

for it in its:
    for k, v in it.items():
        print("{0}={1}".format(k, v))

    print('')
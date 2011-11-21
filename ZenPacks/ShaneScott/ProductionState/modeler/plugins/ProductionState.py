import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap, MultiArgs

class ProductionState(SnmpPlugin):

    maptype = "ProductionState"

    snmpGetMap = GetMap({
        '.1.3.6.1.2.1.1.5.0': 'setEcProdState',
         })


    def process(self, device, results, log):
        """collect snmp name information from this device to test if up"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        om = self.objectMap(getdata)
        if om.setEcProdState:
           log.info('Pre-Production state set')
           om.setEcProdState = 500

        return om

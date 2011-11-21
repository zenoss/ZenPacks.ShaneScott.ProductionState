import Globals
import logging
import os

log = logging.getLogger('zen.ProductionState')

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.ZenMenu import ZenMenu
from Products.ZenUtils.Utils import zenPath
from Products.ZenUtils.Utils import monkeypatch

class ZenPack(ZenPackBase):
    def install(self, app):
        super(ZenPack, self).install(app)
        log.info('Cleaning up old values')
        self.cleanup(app)
        log.info('Creating custom schema')
        self.createCustomSchema()


    def remove(self, app, leaveObjects=False):
        super(ZenPack, self).remove(app, leaveObjects=leaveObjects)
        if not leaveObjects:
            log.info('Removing custom schema')
            self.removeCustomSchema()
            log.info('Cleaning up old values')
            self.cleanup(app)


    def createCustomSchema(self):
        if not self.dmd.Devices.hasProperty('EcProdState'):
            self.dmd.Devices._setProperty('EcProdState', 1, label='EC Instance Production State Flag', type='int')

        self.dmd.Devices.setZenProperty('EcProdState', 1)


    def removeCustomSchema(self):
        if self.dmd.Devices.hasProperty('EcProdState'):
            self.dmd.Devices.deleteZenProperty('EcProdState')


    def cleanup(self, app):
        for i in app.dmd.Devices.getSubDevices():
            try:
                del i.EcProdState
            except:
                pass


@monkeypatch('Products.ZenModel.Device.Device')
def setEcProdState(self, state):
    if self.EcProdState == 1:
       self.EcProdState = int(state)
       self.setProdState(int(state))


@monkeypatch('Products.ZenModel.Device.Device')
def getEcProdState(self):
    if hasattr(self, 'EcProdState'):
        return self.EcProdState
    else:
        return 1

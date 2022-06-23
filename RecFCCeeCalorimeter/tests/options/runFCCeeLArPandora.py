from os import environ, path
from uuid import uuid4
from Gaudi.Configuration import INFO, DEBUG

#
# Start the Application Manager
#
from Configurables import ApplicationMgr

ApplicationMgr().EvtSel = 'NONE'
ApplicationMgr().EvtMax = 2
ApplicationMgr().OutputLevel = INFO
ApplicationMgr().StopOnSignal = True

#
# Define source from where to load events
#
from Configurables import k4DataSvc

podio_event = k4DataSvc('EventDataSvc')
podio_event.input = 'input_fullCalo_SimAndDigi_500.root'
ApplicationMgr().ExtSvc += [podio_event]

#
# Define collections in the event
#
from Configurables import PodioInput

podio_input = PodioInput('PodioInput')
podio_input.collections = ['GenParticles', 'ECalBarrelCells']
ApplicationMgr().TopAlg += [podio_input]

#
# Load event counter
#
from Configurables import EventCounter

event_counter = EventCounter('EventCounter')
event_counter.Frequency = 10
ApplicationMgr().TopAlg += [event_counter]


#
# Load detector
#
from Configurables import GeoSvc

geo_service = GeoSvc('GeoSvc')
# detector_path = environ.get('FCCDETECTORS', '')
# detectors = [
#     'Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml'
# ]
# geo_service.detectors = [path.join(detector_path, d) for d in detectors]
geo_service.detectors = ['/home/jsmiesko/Work/FCC/FCCDetectors/Detector/'
                         'DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml']
# geo_service.detectors = ['/home/jsmiesko/Work/FCC/FCCDetectors/Detector/'
#                          'DetFCCeeIDEA/compact/FCCee_DectMaster.xml']
# geo_service.detectors = ['/home/jsmiesko/Work/FCC/FCCDetectors/Detector/'
#                          'DetFCCeeCLD/compact/FCCee_o2_v02/FCCee_o2_v02.xml']
# geo_service.detectors = ['/home/jsmiesko/Work/FCC/lcgeo/FCCee/compact/'
#                          'FCCee_o1_v04/FCCee_o1_v04.xml']
geo_service.OutputLevel = DEBUG
ApplicationMgr().ExtSvc += [geo_service]

### from Configurables import MarlinProcessorWrapper

### detector_path = environ.get('FCCDETECTORS', '')
### detectors = [
###     'Detector/DetFCCeeIDEA-LAr/compact/FCCee_DectMaster.xml'
### ]

### dd4hep = MarlinProcessorWrapper('InitDD4hep')
### dd4hep.OutputLevel = DEBUG
### dd4hep.ProcessorType = 'InitializeDD4hep'
### dd4hep.Parameters = {
###     'DD4hepXMLFile': [path.join(detector_path, d) for d in detectors],
### }
### ApplicationMgr().TopAlg += [dd4hep]

#
# Pandora in Marlin Wrapper
#
from Configurables import MarlinProcessorWrapper

pandora = MarlinProcessorWrapper('DDMarlinPandora')
pandora.OutputLevel = DEBUG
pandora.ProcessorType = 'DDPandoraPFANewProcessor'
pandora.Parameters = {
    'Verbosity': ['DEBUG2'],
    'PandoraSettingsXmlFile': ['/some/path'],
    'CreateGaps': ['False'],
    'ECalCaloHitCollections': ['ECalBarrelCells']
}
ApplicationMgr().TopAlg += [pandora]


#
# Define output root file
#
from Configurables import PodioOutput

podio_output = PodioOutput('PodioOutput')
podio_output.filename = 'output_pandora_' + uuid4().hex[:8] + '.root'
ApplicationMgr().TopAlg += [podio_output]

#
# Show calculation cost
#
from Configurables import AuditorSvc, ChronoAuditor

chrono_auditor = ChronoAuditor()
auditor_service = AuditorSvc()
auditor_service.Auditors = [chrono_auditor]
podio_input.AuditExecute = True
event_counter.AuditExecute = True
podio_output.AuditExecute = True
ApplicationMgr().ExtSvc += [auditor_service]

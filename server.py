from pynetdicom import AE, evt
from pynetdicom.sop_class import (
    Verification,
    UltrasoundImageStorage,
    UltrasoundMultiFrameImageStorage,
    EnhancedUSVolumeStorage,
    RawDataStorage,
    SpatialRegistrationStorage,
    SpatialFiducialsStorage,
    ModalityWorklistInformationFind
)
import logging
from pydicom.datadict import keyword_for_tag
from datetime import datetime
from pydicom.dataset import Dataset

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler()])

# Define a handler for the DICOM C-ECHO requests
def handle_echo(event):
    logging.info("Received C-ECHO request from %s", event.assoc.requestor.address)
    logging.info("Handling C-ECHO request...")
    return 0x0000

# Define a handler for the DICOM C-STORE requests
def handle_store(event):
    logging.info("Received C-STORE request from %s", event.assoc.requestor.address)
    logging.info("Handling C-STORE request...")

    # Decode the DICOM dataset
    ds = event.dataset
    ds.file_meta = event.file_meta

    # Log more information about the received dataset
    logging.info("Modality: %s", ds.get("Modality", "N/A"))
    logging.info("SOP Class UID: %s", ds.file_meta.MediaStorageSOPClassUID)
    logging.info("SOP Instance UID: %s", ds.SOPInstanceUID)
    logging.info("Study Instance UID: %s", ds.StudyInstanceUID)
    logging.info("Patient's Name: %s", ds.PatientName)

    # Save the dataset to a file
    file_path = f"{ds.SOPInstanceUID}.dcm"
    logging.info("Saving DICOM file to %s", file_path)
    ds.save_as(file_path, write_like_original=False)
    logging.info("Saved DICOM file to %s", file_path)

    return 0x0000

# Define a handler for the Modality Worklist requests
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from datetime import datetime, timedelta

def handle_find(event):
    logging.info("Received C-FIND request from %s", event.assoc.requestor.address)
    logging.info("Handling C-FIND request...")

    request = event.identifier
    logging.info("C-FIND request dataset:")
    for elem in request.elements():
        tag = f"({elem.tag.group:04x},{elem.tag.element:04x})"
        keyword = keyword_for_tag(elem.tag)
        value = elem.value if elem.value is not None else "(no value available)"
        logging.info(f"{tag}: {keyword} = {value}")

    patient_id = request.get('PatientID', '').strip()
    start_date = None
    if 'ScheduledProcedureStepSequence' in request:
        seq = request.ScheduledProcedureStepSequence
        if seq and 'ScheduledProcedureStepStartDate' in seq[0]:
            start_date = seq[0].ScheduledProcedureStepStartDate

    logging.info(f"Searching for PatientID: {patient_id}, StartDate: {start_date}")

    if patient_id == "12345" and start_date == "20240627-20240627":
        ds = Dataset()
        
        # Patient information
        ds.PatientName = "DOE^JOHN"
        ds.PatientID = "12345"
        ds.PatientBirthDate = "19700101"
        ds.PatientSex = "M"

        # Study information
        ds.StudyInstanceUID = "1.2.3.4.5.6.7.8.9.0"
        ds.AccessionNumber = "ACC12345"
        ds.StudyDescription = "US ABDOMEN"

        # Scheduled Procedure Step Sequence
        sps_seq = Sequence()
        sps_item = Dataset()
        sps_item.ScheduledStationAETitle = "GEVOLUSON"
        sps_item.ScheduledProcedureStepStartDate = "20240627"
        sps_item.ScheduledProcedureStepStartTime = "090000"
        sps_item.Modality = "US"
        sps_item.ScheduledProcedureStepDescription = "US ABDOMEN"
        sps_item.ScheduledProcedureStepID = "SPS12345"
        sps_item.ScheduledStationName = "ROOM1"
        sps_item.ScheduledPerformingPhysicianName = "SMITH^JOHN"
        sps_seq.append(sps_item)
        ds.ScheduledProcedureStepSequence = sps_seq

        # Requested Procedure
        ds.RequestedProcedureID = "RP12345"
        ds.RequestedProcedureDescription = "US ABDOMEN"

        # Other relevant fields
        ds.SpecificCharacterSet = "ISO_IR 100"
        ds.StudyDate = "20240627"
        ds.StudyTime = "090000"

        logging.info(f"Returning scheduled exam data for PatientID: {patient_id}")
        return [(0xFF00, ds)]
    else:
        logging.info(f"No matching data found for PatientID: {patient_id}")
        return []

# Initialise the Application Entity (AE)
logging.info("Initialising Application Entity (AE)")
ae = AE()

# Add supported presentation contexts
logging.info("Adding supported presentation contexts")
ae.add_supported_context(Verification)
ae.add_supported_context(UltrasoundImageStorage)
ae.add_supported_context(UltrasoundMultiFrameImageStorage)
ae.add_supported_context(EnhancedUSVolumeStorage)
ae.add_supported_context(RawDataStorage)
ae.add_supported_context(SpatialRegistrationStorage)
ae.add_supported_context(SpatialFiducialsStorage)
ae.add_supported_context(ModalityWorklistInformationFind)

# Define the handlers for incoming association requests
logging.info("Defining handlers for incoming association requests")
handlers = [
    (evt.EVT_C_ECHO, handle_echo),
    (evt.EVT_C_STORE, handle_store),
    (evt.EVT_C_FIND, handle_find),
]

# Start the DICOM server on port 8080
server_address = ('', 8080)
logging.info('Starting DICOM server on port %d...', server_address[1])

try:
    ae.start_server(server_address, evt_handlers=handlers)
except Exception as e:
    logging.error('Failed to start DICOM server: %s', e)
else:
    logging.info('DICOM server successfully started on port %d', server_address[1])

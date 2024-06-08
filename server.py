from pynetdicom import AE, evt
from pynetdicom.sop_class import Verification, CTImageStorage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', handlers=[logging.StreamHandler()])

# Define a handler for the DICOM C-ECHO requests
def handle_echo(event):
    logging.info("Received C-ECHO request from %s", event.assoc.requestor.address)
    return 0x0000

# Define a handler for the DICOM C-STORE requests
def handle_store(event):
    # Decode the DICOM dataset
    ds = event.dataset
    ds.file_meta = event.file_meta

    # Log some information about the received dataset
    logging.info("Received C-STORE request from %s", event.assoc.requestor.address)
    logging.info("SOP Instance UID: %s", ds.SOPInstanceUID)
    logging.info("Study Instance UID: %s", ds.StudyInstanceUID)
    logging.info("Patient's Name: %s", ds.PatientName)

    # Save the dataset to a file
    file_path = f"{ds.SOPInstanceUID}.dcm"
    ds.save_as(file_path, write_like_original=False)
    logging.info("Saved DICOM file to %s", file_path)

    return 0x0000

# Initialise the Application Entity (AE)
ae = AE()

# Add supported presentation contexts
ae.add_supported_context(Verification)
ae.add_supported_context(CTImageStorage)

# Define the handlers for incoming association requests
handlers = [
    (evt.EVT_C_ECHO, handle_echo),
    (evt.EVT_C_STORE, handle_store),
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

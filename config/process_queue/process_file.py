"""
Process an arbitrary file...
"""
import errno
import logging
import os
import sys

import django
logger = logging.getLogger(name='remapp.netdicom.storescp')
# setup django/OpenREM
basepath = os.path.dirname(__file__)
projectpath = os.path.abspath(os.path.join(basepath, ".."))
if projectpath not in sys.path:
    sys.path.insert(1, projectpath)
os.environ['DJANGO_SETTINGS_MODULE'] = 'openremproject.settings'
django.setup()

os.chdir(projectpath)
logger.warning(projectpath)

try:
    import netdicom
    from distutils.version import StrictVersion

    if StrictVersion(netdicom.__version__.__version__) <= StrictVersion('0.8.1'):
        sys.exit(u'Pynedicom > 0.8.1 needs to be installed, see https://docs.openrem.org/en/latest/install.html')
except ImportError:
    sys.exit(u'Pynedicom > 0.8.1 needs to be installed, see https://docs.openrem.org/en/latest/install.html')
from netdicom.SOPclass import StorageSOPClass, VerificationSOPClass
from dicom.dataset import Dataset, FileDataset
from dicom import read_file
from django.views.decorators.csrf import csrf_exempt





def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def process_file(filename):
    print(os.getcwd())
    from remapp.extractors.dx import dx
    from remapp.extractors.mam import mam
    from remapp.extractors.rdsr import rdsr
    from remapp.extractors.ct_philips import ct_philips
    from remapp.models import DicomDeleteSettings
    from remapp.version import __netdicom_implementation_version__
    from remapp.version import __version__ as openrem_version
    from openremproject.settings import MEDIA_ROOT

    try:
        DS = read_file(filename)
    except Exception as e:
        logger.info('Could not load file...')
        print('did not work' + str(e) )
        return
    try:
        logger.info(u"Received C-Store. Stn name %s, Modality %s, SOPClassUID %s, Study UID %s and Instance UID %s",
                     DS.StationName, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID)
    except AttributeError:
        try:
            logger.info(
                u"Received C-Store - station name missing. Modality %s, SOPClassUID %s, Study UID %s and "
                u"Instance UID %s",
                DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID)
        except AttributeError:
            logger.info(u"Received C-Store - error in logging details")

    if 'TransferSyntaxUID' in DS:
        del DS.TransferSyntaxUID  # Don't know why this has become necessary

    del_settings = DicomDeleteSettings.objects.get()
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = DS.SOPClassUID
    file_meta.MediaStorageSOPInstanceUID = DS.SOPInstanceUID
    file_meta.ImplementationClassUID = "1.3.6.1.4.1.45593.1.{0}".format(__netdicom_implementation_version__)
    file_meta.ImplementationVersionName = "OpenREM_{0}".format(openrem_version)
    path = os.path.join(
        MEDIA_ROOT, "dicom_in"
    )
    mkdir_p(path)
    #new_filename = os.path.join(path, u"{0}.dcm".format(DS.SOPInstanceUID))
    ds_new = FileDataset(filename, {}, file_meta=file_meta, preamble="\0" * 128)
    ds_new.update(DS)
    ds_new.is_little_endian = True
    ds_new.is_implicit_VR = True

    while True:
        try:
            station_name = DS.StationName
        except:
            station_name = u"missing"
        try:
            ds_new.save_as(filename)
            break
        except ValueError as e:
            # Black magic pydicom method suggested by Darcy Mason:
            # https://groups.google.com/forum/?hl=en-GB#!topic/pydicom/x_WsC2gCLck
            if "Invalid tag (0018, 7052)" in e.message or "Invalid tag (0018, 7054)" in e.message:
                logger.debug(u"Found illegal use of multiple values of filter thickness using comma. "
                             u"Changing before saving.")
                thickmin = dict.__getitem__(ds_new, 0x187052)
                thickvalmin = thickmin.__getattribute__('value')
                if ',' in thickvalmin:
                    thickvalmin = thickvalmin.replace(',', '\\')
                    thicknewmin = thickmin._replace(value = thickvalmin)
                    dict.__setitem__(ds_new, 0x187052, thicknewmin)
                thickmax = dict.__getitem__(ds_new, 0x187054)
                thickvalmax = thickmax.__getattribute__('value')
                if ',' in thickvalmax:
                    thickvalmax = thickvalmax.replace(',', '\\')
                    thicknewmax = thickmax._replace(value = thickvalmax)
                    dict.__setitem__(ds_new, 0x187054, thicknewmax)
            elif "Invalid tag (01f1, 1027)" in e.message:
                logger.warning(u"Invalid value in tag (01f1,1027), 'exposure time per rotation'. Tag value deleted. "
                               u"Stn name {0}, modality {1}, SOPClass UID {2}, Study UID {3}, Instance UID {4}".format(
                                station_name, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID))
                priv_exp_time = dict.__getitem__(ds_new, 0x1f11027)
                blank_val = priv_exp_time._replace(value='')
                dict.__setitem__(ds_new, 0x1f11027, blank_val)
            elif "Invalid tag (01f1, 1033)" in e.message:
                logger.warning(u"Invalid value in unknown private tag (01f1,1033). Tag value deleted. "
                               u"Stn name {0}, modality {1}, SOPClass UID {2}, Study UID {3}, Instance UID {4}".format(
                                station_name, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID))
                priv_tag = dict.__getitem__(ds_new, 0x1f11033)
                blank_val = priv_tag._replace(value='')
                dict.__setitem__(ds_new, 0x1f11033, blank_val)
            else:
                logger.error(
                    u"ValueError on DCM save {0}. Stn name {1}, modality {2}, SOPClass UID {3}, Study UID {4}, "
                    u"Instance UID {5}".format(
                        e.message, station_name, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID, DS.SOPInstanceUID))
                return
        except IOError as e:
            logger.error(
                    u"IOError on DCM save {0} - does the user running storescp have write rights in the {1} "
                    u"folder?".format(e.message, path))
            return
        except:
            logger.error(
                u"Unexpected error on DCM save: {0}. Stn name {1}, modality {2}, SOPClass UID {3}, Study UID {4}, "
                u"Instance UID {5}".format(
                    sys.exc_info()[0], DS.StationName, DS.Modality, DS.SOPClassUID, DS.StudyInstanceUID,
                    DS.SOPInstanceUID))
            return

    logger.info(u"File %s rewritten", filename)
    
    
    if (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.67'  # X-Ray Radiation Dose SR
        or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.88.22'  # Enhanced SR, as used by GE
        ):
        logger.info(u"Processing as RDSR")
        rdsr(filename)
    elif (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1'  # CR Image Storage
          or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.1'  # Digital X-Ray Image Storage for Presentation
          or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.1.1'  # Digital X-Ray Image Storage for Processing
          ):
        logger.info(u"Processing as DX")
        dx(filename)
    elif (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.2'  # Digital Mammography X-Ray Image Storage for Presentation
          or DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.1.2.1'  # Digital Mammography X-Ray Image Storage for Processing
          or (DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7'  # Secondary Capture Image Storage, for processing
              and DS.Modality == 'MG'  # Selenia proprietary DBT projection objects
              and 'ORIGINAL' in DS.ImageType
              )
          ):
        logger.info(u"Processing as MG")
        mam(filename)
    elif DS.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7':
        try:
            manufacturer = DS.Manufacturer
            series_description = DS.SeriesDescription
        except AttributeError:
            if del_settings.del_no_match:
                os.remove(filename)
                logger.info(u"Secondary capture object with either no manufacturer or series description. Deleted.")
            return
        if manufacturer == 'Philips' and series_description == 'Dose Info':
            logger.info(u"Processing as Philips Dose Info series")
            ct_philips(filename)
        elif del_settings.del_no_match:
            os.remove(filename)
            logger.info(u"Can't find anything to do with this file - it has been deleted")
    elif del_settings.del_no_match:
        os.remove(filename)
        logger.info(u"Can't find anything to do with this file - it has been deleted")

    # must return appropriate status
    return



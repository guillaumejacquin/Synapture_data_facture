import os
import subprocess
import sys
from tika import parser
import time
import json
import os.path


from elems_facture.numero_facture import *
from elems_facture.date import *
from elems_facture.montant_total import *
from elems_facture.tva import *
from elems_facture.indicefacture import *
from elems_facture.print_data import *
from elems_facture.isfacture import *
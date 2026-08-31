from astroquery.simbad import Simbad
import warnings
warnings.filterwarnings('ignore')

result = Simbad.query_object('GD 153')
print('Columns:', result.colnames)
print(result)
print()
print('RA:', result['RA'][0] if 'RA' in result.colnames else 'no RA')
print('DEC:', result['DEC'][0] if 'DEC' in result.colnames else 'no DEC')

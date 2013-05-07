from bitdeli.widgets import set_theme, Description, Title
from bitdeli.chain import Profiles
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import GeoIP

set_theme('eighties')

TIMELINE_DAYS = 30 
TFORMAT = '%Y-%m-%d'
               
text = {'window': TIMELINE_DAYS}

def growth(profiles):
    repos = {}
    for profile in profiles:
        for repo, events in profile['repos'].iteritems():
            first = min(e['tstamp'] for e in events)
            repos[repo.split('?')[0]] = first.split('T')[0]
    c = Counter(repos.itervalues())
    yield sorted(c.items())[1:]
               
def num_events(profiles):
    s = 0
    for profile in profiles:
        s += sum(len(ev) for ev in profile['repos'].itervalues())
    yield {'head': s}
    
Profiles().map(num_events).show('text')    
Profiles().map(growth).show('line',
                            size=(12, 4))

#Profiles().map(countries).show('map',
#                               label='Visitors',
#                               size=(12, 4))


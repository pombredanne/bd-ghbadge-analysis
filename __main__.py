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
    yield sorted(c.items())

def weekly(daily):
    w = {}
    for day, count in daily.next():
        d = datetime.strptime(day, TFORMAT)
        _year, week, _dnum = d.isocalendar()
        if week in w:
            w[week][1] += count
        else:
            w[week] = [d.strftime('%m/%d'), count]
    yield sorted(w.itervalues())

def cumu(daily):
    c = []
    cum = 0
    for day, count in daily.next():
        c.append((day, cum))
        cum += count
    yield c
         
def num_events(profiles):
    s = 0
    for profile in profiles:
        s += sum(len(ev) for ev in profile['repos'].itervalues())
        yield profile
    text['total'] = s
  
Profiles().map(num_events)\
          .map(growth)\
          .show('line',
                label='Daily new badges',
                size=(12, 4))

Profiles().map(growth)\
          .map(cumu)\
          .show('line',
                label='Total number of badges',
                size=(12, 4))
        
Profiles().map(growth)\
          .map(weekly)\
          .show('bar',
                label='Weekly new badges',
                size=(12, 4))

Title("{total:,} badge views in total", text)    

#Profiles().map(countries).show('map',
#                               label='Visitors',
#                               size=(12, 4))


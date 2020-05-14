"""
This module has class and methods needed for create DGA and benign domain data set
"""
import random
import os
import json

from joblib import Parallel, delayed
from datetime import datetime,timedelta
from algorithms.banjori.dga import Banjori
from algorithms.chinad.dga import Chinad
from algorithms.corebot.dga import Corebot
from algorithms.dircrypt.dga import Dircypt
from algorithms.dnschanger.dga import DnsChanger
from algorithms.fobber.dga import Fobber
from algorithms.gameoverzeus import dga as GameoverZeus
from algorithms.gozi.dga import Gozi
from algorithms.kraken.v1 import dga_v1 as KrakenV1
from algorithms.kraken.v2 import dga_v2 as  KrakenV2
from algorithms.locky import dgav2 as lockyv2
from algorithms.locky import dgav3 as lockyv3
from algorithms.matsnu import dga as Matsnu
from algorithms.monerodownloader import dga as moneroD
from algorithms.murofet.v1 import dga as murofetv1
from algorithms.murofet.v2 import dga as murofetv2
from algorithms.mydoom import dga as Mydoom
from algorithms.necurs import dga as Necurs
from algorithms.newgoz import dga as Newgoz
from algorithms.nymaim import dga as nymaimV1
from algorithms.nymaim2 import dga as nymaimV2
from algorithms.padcrypt import dga as Padcrypt
from algorithms.pitou import dga as Pitou
from algorithms.pizd import dga as Pizd
from algorithms.proslikefan import dga as proslikeFan
from algorithms.pushdo import dga as Pushdo
from algorithms.pushdo import dga2 as Pushdo2
from algorithms.pykspa.improved import dga as pykspa_im
from algorithms.pykspa.precursor import dga as pykspa_pre
from algorithms.qadars import dga as Qadars
from algorithms.qakbot import dga as Qakbot
from algorithms.qsnatch import dga_a as qsnatchA
from algorithms.qsnatch import dga_b as qsnatchB
from algorithms.ramdo.dga import Ramdo
from algorithms.ramnit import dga as Ramnit
from algorithms.ranbyus import dga as Ranbyus
from algorithms.reconyc import dga as Reconyc
from algorithms.rovnix import dga as Rovnix
from algorithms.shiotob import dga as Shiotob
from algorithms.simda import dga as Simda
from algorithms.sisron import dga as Sisron
from algorithms.suppobox import dga as Suppobox
from algorithms.symmi import dga as Symmi
from algorithms.tempedreve import dga as TempeDreve
from algorithms.tinba import dga as Tinba
from algorithms.tinba import tinbadga as Tinba2
from algorithms.unknown_malware import dga as un_malware
# from algorithms.unnamed_downloader import dga as un_downloader
from algorithms.unnamed_javascript_dga import dga as un_js
from algorithms.vawtrak import dga as VawTrak1
from algorithms.vawtrak import dga2 as VawTrak2
from algorithms.vawtrak import dga3 as VawTrak3
from algorithms.zloader import dga as Zloader

import pandas as pd

SEEDS= ["16647BB4",
            "E7392D18",
            "C129388E",
            "E706B455",
            "DC485593",
            "EF214BBF",
            "28488EEA",
            "4BFCBC6A",
            "79159C10",
            "92F4BE35",
            "4302C04A",
            "52278648",
            "9753029A",
            "A6EAB21A500",
            "46CF1B28500",
            "1CCEC41C",
            "0C5787AE2",
            "0FCFFD9E9",
            "75EA95C2",
            "8A0AEC7D",
            "1DF640A8",
            "14DF29DD",
            "8222270B",
            "55536A85",
            "5C39E467",
            "D2B3C361",
            "F318D47D",
            "231D9480",
            "13317EAC",
            "89547381",
            "6C36D41D"]

def rovnix(count=100000):
    d = Rovnix.generate_domains(count=count)
    df = pd.DataFrame(data=d, columns=['domainName'])
    df['dgafaimly'] = 'rovnix'
    write_file(df)

def matsnu(count=10000):
    d = Matsnu.generate_domains(count=count)
    df = pd.DataFrame(data=d, columns=['domainName'])
    df['dgafaimly'] = 'matsnu'
    write_file(df)

def gameover(count=10000):
    d = GameoverZeus.engine(maxiter=count)
    df = pd.DataFrame(data=d, columns=['domainName'])
    df['dgafaimly'] = 'gameoverzeus'
    write_file(df)

def banjori(count=100):
    b = Banjori(count)
    df=pd.DataFrame(data=b.generate_domain(),columns=['domainName'])
    df['dgafaimly'] = 'banjori'
    write_file(df)


def chinad(count=100):
    df=pd.DataFrame(data=Chinad().generate_domain(),columns=['domainName'])
    df['dgafaimly'] = 'chinad'
    write_file(df)


def corebot(count=None):
    c = Corebot(count=count)
    c.generate_domain()
    df = pd.DataFrame(data=c.domains, columns=['domainName'])
    df['dgafaimly'] = 'corebot'
    write_file(df)



def dircrypt(count=100,seed=SEEDS):
    count = round(count / len(seed))
    for s in seed :
        d = Dircypt(seed=s,count=count)
        df = pd.DataFrame(data=d.generate_domain(), columns=['domainName'])
        df['dgafaimly'] = 'dircypt'
        write_file(df)


def dnschanger(count,seed=112435):
    d=DnsChanger(seed,count)
    df = pd.DataFrame(data=d.generate_domain(), columns=['domainName'])
    df['dgafaimly'] = 'dnscharger'
    write_file(df)


def fobber(version=2,count=500):
    f = Fobber(version=version,count=count)
    f.dga()
    df = pd.DataFrame(data=f.domains, columns=['domainName'])
    df['dgafaimly'] = 'fobber'
    write_file(df)

def gozi(count=500):
    g = Gozi(count=count)
    df = pd.DataFrame(data=g.generate_domain(), columns=['domainName'])
    df['dgafaimly'] = 'gozi'
    write_file(df)

def kraken(count=100):
    domains = KrakenV1.get_domains(nr=round(count/4), seed_set='a') + \
              KrakenV1.get_domains(nr=round(count / 4), seed_set='b') + \
              KrakenV2.get_domains(nr=round(count / 4), seed='a',tld_set=1) + \
              KrakenV2.get_domains(nr=round(count / 4), seed='b',tld_set=2)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'kraken'
    write_file(df)


def locky(count=500):
    domains= []
    for i in range(round(count / 2)):
        domain1 = lockyv2.dga(date=datetime.now(),config_nr=random.choice(range(1,8,1)),domain_nr=i)
        domain2 = lockyv3.dga(date=datetime.now(),config_nr=random.choice(range(1,21,1)), domain_nr=i)
        domains = domains+[domain1,domain2]
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'locy'
    write_file(df)


def monero(date=datetime.now(),count=500):
    for counter in range(round(count/2500)):

        domains= moneroD.generate_domains(date,count)
        df = pd.DataFrame(data=domains, columns=['domainName'])
        df['dgafaimly'] = 'monero'
        write_file(df)
        date = date - timedelta(days=1)


def murofet(count=500):
    domains = murofetv1.dga(date=datetime.now(),nr=round(count / 2)) + \
        murofetv2.dga(date=datetime.now(),key=int("0x12F",16),nr=round(count / 2))

    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'murofet'
    write_file(df)


def mydoom(count=500):
    domains = Mydoom.dga(date=datetime.now(),magic=int("0x12F",16),number=count)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'mydoom'
    write_file(df)

def necurs(count=500):
    domains= []
    for i in range(round(count / 2)):
        domain = Necurs.generate_necurs_domain(i,18,date=datetime.now())
        domains = [*domains, domain]
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'necurs'
    write_file(df)


def newgoz(count=500):
    domains= []
    for i in range(round(count / 2)):
        domain = Newgoz.create_domain(i,date=datetime.now())
        domains = [*domains, domain]
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'newgoz'
    write_file(df)


def nymaim(count=500):
    domains = nymaimV1.dga(date=datetime.now(),nr=count) +\
              nymaimV2.dga(date=datetime.now())
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'nymaim'
    write_file(df)


def padcrypt(count=500):

    domains= Padcrypt.dga(date=datetime.now(),
                                    config_nr=random.choice(["2.2.86.1", "2.2.97.0"]),
                                    count = round(count/2))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'padcrypt'
    write_file(df)

def pitou(count=500):
    d=datetime.now()
    seed= Pitou.date2seed(d)
    domains=[]
    for c in range(count):
        domains = [*domains,Pitou.dga(d.year, seed, c, int("0x12F", 16))]
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'pitou'
    write_file(df)

def pizd(count=500,date=None):
    d = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    d -= datetime.utcfromtimestamp(0)
    domains = Pizd.pizd(int(d.total_seconds() * 1000), count)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'pizd'
    write_file(df)

def proslikefan(count=500):
    domains=proslikeFan.dga(date=datetime.now()-timedelta(days=2), magic='mylovehatechoice',nr=round(count/10)) # account from 10 tlds
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'proslikefan'
    write_file(df)

def pushdo2(count=100000):
    d = Pushdo2.initDGA(salt=0,count=count)
    df = pd.DataFrame(data=d, columns=['domainName'])
    df['dgafaimly'] = 'pushdo'
    write_file(df)


def pushdo(count=None):
    d = datetime.now()
    for counter in range(round(count / 2500)):
        domains= Pushdo.dga1(d, random.choice(["kz_v1", "kz_v2", "com_v1"])) + \
                 Pushdo.dga1(d, random.choice(["kz_v1", "kz_v2", "com_v1"])) + \
                 Pushdo.dga1(d, random.choice(["kz_v1", "kz_v2", "com_v1"]))
        df = pd.DataFrame(data=domains, columns=['domainName'])
        df['dgafaimly'] = 'pushdo'
        write_file(df)
        d = d-timedelta(days=1)

def pykspa(count=5000):
    # 20 % noise and 80 % correct
    domains= pykspa_im.generate_domains(datetime.now()-timedelta(days=300),round(count/10),1) + \
        pykspa_im.generate_domains(datetime.now()-timedelta(days=300), round(count / 2.5), 2)+\
        pykspa_pre.generate_domains(datetime.now()-timedelta(days=300), round(count / 2))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'pykspa'
    write_file(df)

def qadars(count=500):
    domains=[]
    d = datetime.now()
    for counter in range(round(count / 2500)):
        for seed in ["89f5", "4449", "E1F1", "E1F2", "E08A", "E1F5"]:
            domains += Qadars.dga(d,int(seed, 16))
            df = pd.DataFrame(data=domains, columns=['domainName'])
            df['dgafaimly'] = 'qadars'
        write_file(df)
        d = d - timedelta(days=1)

def qakbot(count=5000):
    d, tlds, nr, sandbox, seed = Qakbot.set_arg()
    domains= Qakbot.dga(d, tlds, count, sandbox, seed)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'qakbot'
    write_file(df)

def qsnatch(count=None):
    d = datetime.now()
    for counter in range(round(count / 2500)):
        domains= qsnatchA.dga(date=d)+qsnatchB.dga(date=datetime.now()-timedelta(days=10))
        df = pd.DataFrame(data=domains, columns=['domainName'])
        df['dgafaimly'] = 'qsnatch'
        write_file(df)
        d = d - timedelta(days=1)

def ramdo(count=5000):
    domains= Ramdo(count=count).generate_dga()
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'ramdo'
    write_file(df)

def ramnit(count=1000):
    seeds = random.sample(SEEDS, 10)
    domains =[]
    for seed in seeds:
        domains += Ramnit.get_domains(seed=int(seed,16), nr=round(count/10))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'ramnit'
    write_file(df)

def ranbyus(count=None):
    seeds = random.sample(SEEDS, 10)
    domains = []
    d = datetime.now()
    for counter in range(round(count / 2500)):
        for seed in seeds:
            domains += Ranbyus.dga(d.year, d.month, d.day, seed=int(seed, 16))
        df = pd.DataFrame(data=domains, columns=['domainName'])
        df['dgafaimly'] = 'ranbyus'
        write_file(df)
        d = d - timedelta(days=1)

def reconyc(count=5000):
    domains= Reconyc.generate_domains(nr=count)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'reconyc'
    write_file(df)

def shiotob(count=5000):
    domains= Shiotob.generate_domains(count)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'shiotob'
    write_file(df)

def simda(count=5000):
    domains= Simda.generate_domains(count=count)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'simda'
    write_file(df)

def sisron(count=5000):
    d = datetime.now()
    for counter in range(round(count / 40)):
        domains= Sisron.generate_domains(d, 100)
        df = pd.DataFrame(data=domains, columns=['domainName'])
        df['dgafaimly'] = 'sisron'
        write_file(df)
        d = d - timedelta(days=1)

def suppobox(count=5000):
    domains =[]
    for c in range(1,3,1):
        time_ , d = Suppobox.set_arg()
        domains+=Suppobox.generate_domains(time_ ,c,round(count/3))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'suppobox'
    write_file(df)

def symmi(count=5000):
    seed = Symmi.create_seed(datetime.now()-timedelta(20))
    domains= Symmi.dga(seed, ".ddns.net", count)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'symmi'
    write_file(df)

def tempedreve(count=None):
    d = datetime.now()
    for counter in range(round(count / 1800)):
        domains= TempeDreve.dga(d)
        df = pd.DataFrame(data=domains, columns=['domainName'])
        df['dgafaimly'] = 'tempedreve'
        write_file(df)
        d = d - timedelta(days=1)

def tinba(count=None):
    domains= Tinba.generate_domains()
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'tinba'
    write_file(df)

def tinba2(count=100000):
    domains= Tinba2.tinbaDGA(idomain='worldisgreat.com',count=count)
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'tinba'
    write_file(df)

def unmalware(count=1000):
    domains=[]
    for p in ["sn", "al"]:
        domains=domains+un_malware.dga(p,round(count/12))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'unmalware'
    write_file(df)

def unjs(count=1000):
    domains= un_js.dga(seed="hello", d=datetime.now(),nr=round(count/3))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'unjavascript'
    write_file(df)

def zloader(count=1000):
    domains=[]
    for key in ["q23Cud3xsNf3","41997b4a729e1a0175208305170752dd", "kZieCw23gffpe43Sd"]:
        seed = Zloader.seeding(d=datetime.now()-timedelta(days=2),
                           key=key)
        domains+=Zloader.dga(seed, round(count/2))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'zloader'
    write_file(df)

def vawtrak(count=100):
    domains= VawTrak1.generate_domains(count=round(count/10)) + \
            VawTrak2.generate_domains(count=round(count/10)) +\
            VawTrak3.generate_domains(count=round(count/10))
    df = pd.DataFrame(data=domains, columns=['domainName'])
    df['dgafaimly'] = 'vawtrak'
    write_file(df)


def write_file(df):
    df.to_csv(DATA_FILE, compression="gzip", mode='a', header=False,index=False)


def generate_data(config_file=None):

    if not config_file:
        config ={
                'gameover' : 30,
                            }
    else:
        with open(config_file) as json_file:
            config = json.load(json_file)

    function_map ={'banjori': banjori,
        'chinad': chinad,
        'corebot': corebot,
        'dircrypt': dircrypt,
        'dnschanger': dnschanger,
        'fobber': fobber,
        'gameover': gameover,
        'gozi': gozi,
        'kraken': kraken,
        'locky': locky,
        'matsnu': matsnu,
        'monero': monero,
        'murofet': murofet,
        'mydoom': mydoom,
        'necurs': necurs,
        'newgoz': newgoz,
        'nymaim': nymaim,
        'padcrypt': padcrypt,
        'pitou': pitou,
        'pizd': pizd,
        'proslikefan': proslikefan,
        'pushdo': pushdo,
        'pushdo2': pushdo2,
        'pykspa': pykspa,
        'qadars': qadars,
        'qakbot': qakbot,
        'qsnatch': qsnatch,
        'ramdo': ramdo,
        'ramnit': ramnit,
        'ranbyus': ranbyus,
        'reconyc': reconyc,
        'rovnix': rovnix,
        'shiotob': shiotob,
        'simda': simda,
        'sisron': sisron,
        'suppobox': suppobox,
        'symmi': symmi,
        'tempedreve': tempedreve,
        'tinba': tinba,
        'tinba2': tinba2,
        'un_malware': unmalware,
        'un_js': unjs,
        'vawtrak': vawtrak,
        'zloader': zloader
        }

    def execute(key,count=10):
        print(f"running function {key} for count {count}")
        func=function_map[key]
        func(count=count)
        print(f"running function {key} for count {count} complete")

    Parallel(n_jobs=4)(delayed(execute)(key=key,count=config[key]) for key in config.keys())


if __name__ == "__main__":
    import sys
    DATA_FILE = "{}/processingdata.csv.gz".format(os.getenv('datadir',"."))
    DATA_CONFIG = "{}/config.json".format(os.getenv('configdir',"config"))
    try:
        print("overriding data file")
        print(DATA_FILE)
        os.remove(DATA_FILE)
    except OSError:
        pass
    generate_data()






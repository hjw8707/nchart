import re
import math

##################################################################
# NuDB
##################################################################
#
# class to load the database for nuclear properties
#
# loading mass_1.mas??
# loading rct1.mas??
# loading rct2_1.mas??
# loading nubase_3.mas??
#
class NuDB:
    def __init__(self):
        self.dbDic = {}
        self.LoadData()

    def LoadData(self):
        ##################################################################
        # Database Loading
        #
        # to 'dbDic' (dictionary)
        ##################################################################
        # 1. mass table
        ##################################################################
        f = open('./mass_1.mas20','r')
        lines = f.readlines()
        f.close()
        del lines[:36]

        keys = ['cc', 'NZ', 'N', 'Z', 'A', '', 'el', 'o', '', 'mass', 'massu', 
                'bind', '', 'bindu','', 'B', 'beta', 'betau', '', 'atm1', '', 'atm2', 'atmu']
        lens = [1, 3, 5, 5, 5, 1, 3, 4, 1, 14, 12, 13, 1, 10, 1, 2, 13, 11, 1, 3, 1, 13, 12]

        self.dbDic = {}
        for line in lines:
            tempDic = {}
            for (k, v) in zip(keys, [line[sum(lens[:i]):sum(lens[:i])+lens[i]] for i in range(len(lens))]):
                if k == '': continue
                tempDic[k] = v.strip()
            self.dbDic[(int(tempDic['Z']),int(tempDic['N']))] = tempDic

        ##################################################################
        # 2. S(2n), ...
        ##################################################################
        f = open('./rct1.mas20','r')
        lines = f.readlines()
        f.close()
        del lines[:35]

        keys = ['cc', 'A', '', 'el', 'Z', '', 's2n', 's2nu', 's2p', 's2pu', 'qa', 'qau', 
                'q2b', 'q2bu', 'qep', 'qepu', 'qbn', 'qbnu' ]
        lens = [ 1, 3, 1, 3, 3, 1, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10 ]

        for line in lines:
            tempDic = {}
            for (k, v) in zip(keys, [line[sum(lens[:i]):sum(lens[:i])+lens[i]] for i in range(len(lens))]):
                if k == '': continue
                tempDic[k] = v.strip()
            z = int(tempDic['Z'])
            n = int(tempDic['A']) - z
            if (z, n) in self.dbDic:
                for k in tempDic.keys():
                    if k not in self.dbDic[(z,n)]:
                        self.dbDic[(z,n)][k] = tempDic[k]

        ##################################################################
        # 3. S(n), ...
        ##################################################################
        f = open('./rct2_1.mas20','r')
        lines = f.readlines()
        f.close()
        lines = lines[37:3595]

        keys = ['cc', 'A', '', 'el', 'Z', '', 'sn', 'snu', 'sp', 'spu', 'q4b', 'q4bu', 
                'qda', 'qdau', 'qpa', 'qpau', 'qna', 'qnau' ]
        lens = [ 1, 3, 1, 3, 3, 1, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10, 12, 10 ]

        for line in lines:
            tempDic = {}
            for (k, v) in zip(keys, [line[sum(lens[:i]):sum(lens[:i])+lens[i]] for i in range(len(lens))]):
                if k == '': continue
                tempDic[k] = v.strip()
            z = int(tempDic['Z'])
            n = int(tempDic['A']) - z
            if (z, n) in self.dbDic:
                for k in tempDic.keys():
                    if k not in self.dbDic[(z,n)]:
                        self.dbDic[(z,n)][k] = tempDic[k]

        ##################################################################
        # 4. Nubase
        ##################################################################
        f = open('./nubase_3.mas20','r')
        lines = f.readlines()
        f.close()
        lines = lines[25:]

        keys = ['A', '', 'Z', 'I', '', 'Ael', 's', '', 'mass', 'massu', 'iex', 'iexu', 
                'exo', 'iu', 'ii', 't', 'tuni', '', 'tu', 'jpi', 'year', '', 'dis', '', 'br' ]
        lens = [ 3, 1, 3, 1, 3, 5, 1, 1, 13, 11, 12, 11, 2, 1, 1, 9, 2, 1, 7, 14, 2, 10, 4, 1, 90 ]

        for line in lines:
            tempArr = [line[sum(lens[:i]):sum(lens[:i])+lens[i]] for i in range(len(lens))]
            if int(tempArr[3]) != 0: continue # no isomer
            tempDic = {}
            for (k, v) in zip(keys, tempArr):
                if k == '': continue
                tempDic[k] = v.strip()
                if k == 'br':
                    brs = v.strip().split(';')
                    tempDic['brs'] = brs
            z = int(tempDic['Z'])
            n = int(tempDic['A']) - z
            if (z, n) in self.dbDic:
                for k in tempDic.keys():
                    if k not in self.dbDic[(z,n)]:
                        self.dbDic[(z,n)][k] = tempDic[k]
        
    ############################################################
    # internal functions
    #
    # IsExist: check the nucleus exists
    def IsExist(self, z, n):
        return (z,n) in self.dbDic

    # GetItem: get the item for (z,n)
    def GetItem(self, z, n, item):
        if (z,n) in self.dbDic:
            try:    bind = float(self.dbDic[(z,n)][item])
            except: 
                try: bind = float(self.dbDic[(z,n)][item].replace('#','.'))
                except: return None
            return bind
        else:
            return None
    
    # GetTimeConvFactor: get the time conversion factor (ref = 1 sec.)
    def GetTimeConvFactor(self, x):
        return {'s': 1., 'ms': 1E-3, 'us': 1E-6, 'ns': 1E-9, 'ps': 1E-12, 
                'fs': 1E-15, 'as': 1E-18, 'zs': 1E-21, 'ys': 1E-24, 
                'm': 60., 'h': 3600., 'd': 86400., 
                'y': 3.1536E7, 'ky': 3.1536E10, 'My': 3.1536E13, 'Gy': 3.1536E16, 
                'Ty': 3.1536E19, 'Py': 3.1536E22, 'Ey': 3.1536E25, 'Zy': 3.1536E28,
                'Yy': 3.1536E31}.get(x, 0)

    # DecayChannelConv: conversion the decay channel to number
    def DecayChannelConv(self, x):
        return {'2n': -4, 'n': -3, 'B-': -2, 'SF': -1, 'IS': 0, 
                'A': 1, 'B+': 2, 'EC': 3, 'p': 4, '2p':5, '3p':6}.get(x, -20)

    # DecayChannelStable: conversion the decay channel to the stability 
    def DecayChannelStable(self, x): # return +1 (p-rich), 0: 
        return {'2n': -1, 'n': -1, 'B-': -1, 'SF': 1, 'IS': 0, 
                'A': 1, 'B+': 1, 'EC': 1, 'p': 1, '2p': 1, '3p':1}.get(x, -20)
    ############################################################

    def GetName(self, z, n, sup = True):
        nuEl = ["n", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Ed", "Fl", "Ef", "Lv", "Eh", "Ei"]
        if (z,n) in self.dbDic:
            if sup: return '$^{'+self.dbDic[(z,n)]['A']+'}$'+self.dbDic[(z,n)]['el']
            else:   return self.dbDic[(z,n)]['A']+self.dbDic[(z,n)]['el']         
        elif z >= 0 and z < len(nuEl):
            if sup: return '$^{'+str(z+n)+'}$'+nuEl[z]
            else:   return str(z+n)+nuEl[z]            
        return None  

    def GetZN(self, name):
        nuEl = ["n", "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Ed", "Fl", "Ef", "Lv", "Eh", "Ei"]
        p = re.compile('(\d+)([a-zA-Z]+)')
        m = p.match(name)
        if m is None: return None
        a = int(m.group(1))
        for i, s in zip(range(len(nuEl)),nuEl):
            if m.group(2).casefold() == s.casefold():
                z = i
                break
        else:
            return None
        return (z, a-z)

    ############################################################
    def GetBE (self, z, n): return self.GetItem(z, n, 'bind')
    def GetSn (self, z, n): return self.GetItem(z, n, 'sn')
    def GetSp (self, z, n): return self.GetItem(z, n, 'sp')
    def GetS2n(self, z, n): return self.GetItem(z, n, 's2n')
    def GetS2p(self, z, n): return self.GetItem(z, n, 's2p')
    def GetQa (self, z, n): return self.GetItem(z, n, 'qa')
    ############################################################

    tStbl = 1E40
    tUnstbl = 1E-40

    def GetTime(self, z, n):
        if (z,n) in self.dbDic:
            t = self.dbDic[(z,n)]['t']
            tuni = self.dbDic[(z,n)]['tuni']
            if tuni == '':
                if t == 'stbl': return self.tStbl
                else:           return self.tUnstbl
            fac = self.GetTimeConvFactor(tuni)
            try:    tfl = float(t)
            except: tfl = float(t.replace('#', '.').replace('>', '').replace('<','').replace('~',''))
            return tfl * fac
        else:
            return None

    def GetLogTime(self, z, n): return math.log10(self.GetTime(z,n))
    def GetStringTime(self, z, n):
        if (z,n) in self.dbDic:
            t = self.dbDic[(z,n)]['t']
            tuni = self.dbDic[(z,n)]['tuni']
            return t+' '+tuni
        else:
            return None        
        
    def GetMajorDecayChannel(self, z, n): # returning 2n, n, B-, SF, IS, A, B+, EC, p, 2p, 3p
        if (z,n) in self.dbDic:
            br = self.dbDic[(z,n)]['br']
            return re.split('[ =~><]', br)[0]
        else:
            return None
    def GetDecayChannels(self, z, n): # returning 2n, n, B-, SF, IS, A, B+, EC, p, 2p, 3p
        if (z,n) in self.dbDic:
            brs = self.dbDic[(z,n)]['brs']
            return [re.split('[ =~><]', x)[0] for x in brs]
        else:
            return None        

    def GetMajorDecayChannelNum(self, z, n):
        return self.DecayChannelConv(self.GetMajorDecayChannel(z,n))

    def GetStableOrNotNum(self, z, n):
        return self.DecayChannelStable(self.GetMajorDecayChannel(z,n))
    
    
if __name__=="__main__":
    nu = NuDB()
    z=nu.GetDecayChannels(2,4)
    print(nu.GetStringTime(2,4))
    magic_n = [ 2, 8, 20, 28, 50, 82, 126 ]
    for z in magic_n:
        for i in range(0,100):  
            if nu.IsExist(i, z):
                a0 = i
                break
        for i in range(200,0,-1):  
            if nu.IsExist(i, z):
                a1 = i
                break
        print(a0, a1)
    
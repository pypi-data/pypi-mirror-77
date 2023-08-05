# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 21:04:20 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, landfil_sorption
from .LandfillInput import LandfillInput
from .ProcessModel import ProcessModel


class Landfill(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. PFAS-containing waste and bulk MSW are well mixed.
        4. Annual time horizon.
    """
    ProductsType = ['LF_Leachate']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = LandfillInput(input_data_path)

    def calc(self, Inc_flow=None):
        # Initialize the Incoming flow
        if Inc_flow:
            self.Inc_flow = Inc_flow
        else:
            self.Inc_flow = Flow()
            kwargs = {}
            for key, data in self.InputData.IncProp.items():
                kwargs[key] = data['amount']
            kwargs['PFAS_cont'] = {}
            for key, data in self.InputData.IncPFAS.items():
                kwargs['PFAS_cont'][key] = data['amount']
            self.Inc_flow.set_flow(**kwargs)

        # Calculating the mass of MSW in Landfill
        MSW_Mass = self.Inc_flow.mass / self.InputData.LFMSW['frac_of_msw']['amount'] - self.Inc_flow.mass

        # Initializing the MSW in Landfill
        self.MSW_flow = Flow()
        kwargs = {}
        kwargs['mass_flow'] = MSW_Mass
        kwargs['ts_cont'] = self.InputData.LFMSW['ts_cont']['amount']
        kwargs['C_cont'] = self.InputData.LFMSW['C_cont']['amount']
        kwargs['bulk_dens'] = self.InputData.LFMSW['bulk_dens']['amount']
        self.MSW_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with MSW in landfill
        self.Mixture = mix(self.Inc_flow, self.MSW_flow)

        # Calculating the volume of percipitation (includes RunOff and Leachate)
        LF_Leachate_Vol = self.InputData.Water_Blnc['leach_gpad']['amount'] * 365.25 * self.InputData.Water_Blnc['is_leach_col']['amount'] * \
            self.InputData.Water_Blnc['frac_leach_col']['amount'] / 264.172 * 1000  # L/yr
        Leachate_Vol = (self.InputData.Water_Blnc['leach_gpad']['amount'] * (1-self.InputData.Water_Blnc['is_leach_col']['amount']) +
                        self.InputData.Water_Blnc['leach_gpad']['amount'] * self.InputData.Water_Blnc['is_leach_col']['amount'] *
                        (1 - self.InputData.Water_Blnc['frac_leach_col']['amount'])) * 365.25 / 264.172 * 1000  # L/yr

        # Calculating the PFAS in water and soil partitions
        self.LF_storage, self.LF_Leachate, self.Leachate = landfil_sorption(self.Mixture, self.InputData.LogPartCoef, LF_Leachate_Vol, Leachate_Vol)

        # add to Inventory
        self.Inventory.add('Leachate', 'Landfill', 'Water', self.Leachate)
        self.Inventory.add('Storage', 'Landfill', 'Storage', self.LF_storage)

    def products(self):
        Products = {}
        Products['LF_Leachate'] = self.LF_Leachate
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        report['LF_Leachate'] = self.LF_Leachate.PFAS
        report['Leachate'] = self.Leachate.PFAS
        report['Storage'] = self.LF_storage.PFAS
        return(report)

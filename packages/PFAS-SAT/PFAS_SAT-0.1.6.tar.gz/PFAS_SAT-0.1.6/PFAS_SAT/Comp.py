# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:48:31 2020

@author: msmsa
"""
import pandas as pd
from .Flow import Flow
from .SubProcesses import mix, aerobic_composting
from .CompInput import CompInput
from .ProcessModel import ProcessModel


class Comp(ProcessModel):
    """
    Assumptions:
        1. No volatilization or degradation of PFAS.
        2. Steady state.
        3. Feedstocks, active piles, and curing piles are well mixed.
        4. Annual time horizon.
    """
    ProductsType = ['CompFin', 'ContactWater']

    def __init__(self, input_data_path=None, CommonDataObjct=None, InventoryObject=None):
        super().__init__(CommonDataObjct, InventoryObject)
        self.InputData = CompInput(input_data_path)

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

        # Calculating the mass of Amendments
        Amnd_mass = self.InputData.AmndProp['mass_ratio']['amount'] * self.Inc_flow.mass

        # Initializing the Soil flow
        self.Amnd_flow = Flow()
        kwargs = {}
        kwargs['mass_flow'] = Amnd_mass
        kwargs['ts_cont'] = self.InputData.AmndProp['ts_cont']['amount']
        kwargs['C_cont'] = self.InputData.AmndProp['C_cont']['amount']
        self.Amnd_flow.set_flow(**kwargs)

        # Mixing the Incoming flow with soil
        self.Mix_to_ac = mix(self.Inc_flow, self.Amnd_flow)

        # Active Composting
        self.Mix_to_cu, self.Leachate_ac, self.RunOff_ac, self.Contact_water_ac = aerobic_composting(self.Mix_to_ac,
                                                                                                     self.InputData.AComp,
                                                                                                     self.InputData.LogPartCoef,
                                                                                                     self.InputData.Percip)

        # Curing
        self.Finished_Comp, self.Leachate_cu, self.RunOff_cu, self.Contact_water_cu = aerobic_composting(self.Mix_to_cu,
                                                                                                         self.InputData.Curing,
                                                                                                         self.InputData.LogPartCoef,
                                                                                                         self.InputData.Percip)

        self.Leachate = mix(self.Leachate_ac, self.Leachate_cu)
        self.RunOff = mix(self.RunOff_ac, self.RunOff_cu)
        self.Contact_water = mix(self.Contact_water_ac, self.Contact_water_cu)

        # add to Inventory
        self.Inventory.add('Leachate', 'Comp', 'Water', self.Leachate)
        self.Inventory.add('RunOff', 'Comp', 'Water', self.RunOff)

    def products(self):
        Products = {}
        Products['CompFin'] = self.Finished_Comp
        Products['ContactWater'] = self.Contact_water
        return(Products)

    def setup_MC(self, seed=None):
        self.InputData.setup_MC(seed)

    def MC_Next(self):
        input_list = self.InputData.gen_MC()
        return(input_list)

    def report(self):
        report = pd.DataFrame(index=self.Inc_flow._PFAS_Index)
        report['Finished Compost'] = self.Finished_Comp.PFAS
        report['Leachate'] = self.Leachate.PFAS
        report['RunOff'] = self.RunOff.PFAS
        report['Contact water'] = self.Contact_water.PFAS
        return(report)

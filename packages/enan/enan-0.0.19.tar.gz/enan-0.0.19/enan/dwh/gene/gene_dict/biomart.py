# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:05:34 2019

Data warehouse control class

Analyzer o-- DWHControl <|.. GeneControl <|.. Biomart

@author: tadahaya
"""
import pandas as pd
import os

from ...._utils.converter import SynoDict
from ...dwh_control import StoredDict

# concrete class
class Biomart(StoredDict):
    def __init__(self):
        self.__fileprefix = "mart_export_" # hard coding
        self.__sp_dict = {"human":"HGNC", # hard coding
                          "mouse":"MGI", # hard coding
                          "rat":"RGD"} # hard coding
        self.dic = SynoDict()
        self.__base = os.path.dirname(__file__) # ~\enapy\dwh\gene\gene_dict
        self.__state = {"database":"BioMart","name":""}

    def get_(self):
        return self.dic

    def load_(self,species="human"):
        """ get converter pickle path derived from biomart """
        print("species='{}'".format(species))
        key = self.__fileprefix + self.__sp_dict[species]
        url = self.__base + "\\biomart"
        p_pkl = self.__checker(url,key,extension="pkl")
        if len(p_pkl)==0:
            p_txt = self.__checker(url,key,extension="txt")
            if len(p_txt)==0:
                raise ValueError("!! check data existence !!")
            else:
                self.__generate_conv(p_txt,self.__sp_dict[species])
        else:
            self.dic.read_pickle(p_pkl)
        self.__state["name"] = species

    def prep_(self):
        raise NotImplementedError

    def get_state(self):
        return self.__state

    def __checker(self,url,key,extension="pkl"):
        """ check existence of files with the indicated extension """
        f_intr = "{0}.{1}".format(key,extension)
        p_intr = url + "\\{}".format(f_intr)
        ps = os.listdir(url)
        if f_intr in ps:
            return p_intr
        else:
            return ""

    def __generate_conv(self,url,key):
        """ generate dictionary from Biomart data """
        names,ids,synonyms = self.__prep_gene_conv(url,key + " symbol")
        self.dic = SynoDict(names,ids,synonyms,processing=True)
        self.dic.to_pickle(url.replace("txt","pkl"))

    def __prep_gene_conv(self,url,symbol_name="HGNC symbol"): # hard coding
        """
        generate necessary information for converter from BioMart data
        HGNC/MGI/RGD symbol, NCBI gene ID, Gene synonym
        
        Parameters
        ----------
        url: str
            a path for the BioMart derived file

        symbol_name: str
            indicate the column name for symbol
            "HGNC symbol": human
            "MGI symbol": mouse
            "RGD symbol": rat

        """
        df = pd.read_csv(url,sep="\t").dropna(subset=["NCBI gene ID"])
        df.loc[df["Gene Synonym"]!=df["Gene Synonym"],"Gene Synonym"] = df[symbol_name]
        df = df.groupby(["NCBI gene ID"],as_index=False).agg(set)
        df["NCBI gene ID"] = df["NCBI gene ID"].astype(int)
        df[symbol_name] = df[symbol_name].apply(lambda x: x.pop())
        df.set_index(symbol_name,drop=True,inplace=True)
        return list(df.index),list(df["NCBI gene ID"]),list(df["Gene Synonym"])
from argparse import ArgumentParser
import os
import sys
import socket
import time

# ENVIOREMENT VARIABLES
def loadENVIROMENTVARIABLES():
    machine = socket.gethostname()
    print("Estas en la maquina: ", machine)

    if "Savins" in machine or "kent.ac.uk"in machine or "edu" in machine:
        os.environ["SPM_machine"] = "laptopSavins"
        loadLaptopSavins()


def loadLaptopSavins():
    print("Loading MacBookSavins Enviorement Variables")
    os.environ["SPM_SAVINSPHD_PATH"] = "/Users/savins/repositorios/PhDSoftware/python"
    os.environ["SPM_ROOT_PATH"] = "/Users/savins/repositorios/PhDSoftware/python/"
    os.environ["SPM_DRUGBANK_PATH"] = "/home/users/hperez/Savins/DB/DrugBank/DB-201016_M2"
    os.environ["SPM_FDA_PATH"] = "/Users/savins/DB/fda"

loadENVIROMENTVARIABLES()

os.environ["savinsPHD_path"] = os.getcwd()

######END
import PhDlibrary


if __name__ == "__main__":
    # ArgumentParser con una descripcion de la aplicacion
    parser = ArgumentParser(description='%(prog)s controla toda la experimentacion de la tesis de Savins.')
    SAVINSList = ["savins", "scp_bull", "scp_polonia"]
    GENERACIONlist = ['generate_FDA_ROCS']
    PROCESSlist = ["process_FDA_ROCS"]
    SearchList = ["change_name_fda_compound","round_decimal"]
    EVALlist = ["EVAL_RANKING_NEW_OF", "EVAL_ROCS"]
    DataframeList = ["join_dataframe", "sort_csv"]
    PlotList = ["PLOT_COMPOUNDS"]
    FullList = ["N_DUDE_OP","N_MAYBRIDGE_OP", "completoOPES_DrugBank", "evalROCSandZAP", "N_ADN","completoOPSS"]
    ReflexList = ["procesar_Reflex3D"]
    DatabaseList = ["splitDatabase", "applyPCA"]
    ExtrasList = ["cleanFDA", "cleanDrugBank514"]
    MultiobjectiveList = ["pareto", "checkVAR", "manyPareto",
                          "selectParetos", "plotManyParetoIndividually", "selectNonDominatedPoints", "plotParetosDifferentColors", "selectNonDominatedTargets","plotTargetsDifferentColors"]

    optionArgument = SAVINSList + GENERACIONlist + PROCESSlist + EVALlist + DataframeList + \
        SearchList+PlotList + FullList + ReflexList + \
        DatabaseList + ExtrasList+MultiobjectiveList
    parser.add_argument("function", nargs="?", choices=optionArgument)
    
    args, sub_args = parser.parse_known_args()
    if args.function == "savins":
        parser = ArgumentParser(description="Procesa los resultados de FDA obtenidos por OptiPharm.")
        parser.add_argument('-dataframe',help='Directorio de entrada')
        parser.add_argument('-path',help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.savinsTEST.main(args.dataframe, args.path)
    elif args.function == "scp_bull":
        os.system("rsync -rvu savinsPhDmain.py bullxual:~/scratch/")
        os.system("rsync -rvu savinsPhD/*.py bullxual:~/scratch/savinsPhD/")
        os.system("rsync -rvu savinsPhD/lanzador/principales/ bullxual:~/scratch/savinsPhD/lanzador/principales/")
        os.system("rsync -rvu savinsPhD/scriptVarios bullxual:~/scratch/savinsPhD/")
    elif args.function == "scp_polonia":
        os.system("rsync -ruv savinsPhD/*.py polonia:~/Savins/experiments/savinsPhD/")
        os.system("rsync -ruv savinsPhD/lanzador/principales/ polonia:~/Savins/experiments/savinsPhD/lanzador/principales/")
        os.system("rsync -ruv savinsPhDmain.py polonia:~/Savins/experiments/")
        os.system("rsync -ruv savinsPhD/scriptVarios polonia:~/Savins/experiments/savinsPhD/")
    elif args.function == "scp_noruega":
        os.system("rsync -ruv savinsPhD/*.py noruega:~/savins/experiments/savinsPhD/")
        os.system("rsync -ruv savinsPhD/lanzador/principales/ noruega:~/savins/experiments/savinsPhD/lanzador/principales/")
        os.system("rsync -ruv savinsPhDmain.py noruega:~/savins/experiments/")
        os.system("rsync -ruv savinsPhD/scriptVarios noruega:~/savins/experiments/savinsPhD/")
        
        #os.system("scp -r savinsPhD/ polonia:~/Savins/savinsPhD/")
    ##########################
    ## GENERATION
    #########################
    elif args.function == "generate_FDA_ROCS":
        PhDlibrary.Generation.generate_FDA_ROCS()
    #########################
    ## PROCESS
    #########################
    elif args.function == "procesar_FDA_ROCS":
        parser = ArgumentParser(description="Procesa los resultados de FDA obtenidos por OptiPharm.")
        parser.add_argument('-ipath', required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.Process.procesar_FDA_ROCS(args.ipath)
    
    ##########################
    ## EVALS
    ##########################
    elif args.function == "EVAL_RANKING_NEW_OF":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")        
        parser.add_argument('-path', required=True,help='Directorio de entrada')
        parser.add_argument("-of",required=True,help='OP_SS')
        parser.add_argument('-numbers',required = True, type=int,help='Numero de ranking')
        args = parser.parse_args(sub_args)
        PhDlibrary.Eval.eval_ranking_with_new_objetive_function(args.path, args.numbers, args.of)
    elif args.function == "EVAL_ROCS":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")        
        parser.add_argument('-path', required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.Eval.evalWithROCS(args.path)
    ##########################
    ## DATAFRAME
    ##########################
    elif args.function == "join_dataframe":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")
        parser.add_argument('-csvs',nargs='+',help='csv que se quieren combinar')
        args = parser.parse_args(sub_args)
        PhDlibrary.Dataframe.join_dataframe(args.csvs)
    elif args.function == "sort_csv":
        parser = ArgumentParser(description="Ordena un csv mediante una columna.")
        parser.add_argument('-csvs',nargs='+',help='csv que se quieren combinar')
        parser.add_argument('-by', required=True,help='columna por la que se ordena')
        parser.add_argument('-asc', required=True,type=int, help='orden ascendente')
        args = parser.parse_args(sub_args)
        PhDlibrary.Dataframe.sort_dataframe(args.csvs, args.by, args.asc)
    elif args.function == "change_name_fda_compound":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")        
        parser.add_argument('-csv', nargs="+", required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.Search.change_name_fda_compound(args.csv)
    elif args.function == "round_decimal":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")        
        parser.add_argument('-csv', required=True,help='Directorio de entrada')
        parser.add_argument('-decimal',required = True, type=int,help='Numero de ranking')
        args = parser.parse_args(sub_args)
        PhDlibrary.Search.round_decimal(args.csv,args.decimal)
    ##########################
    ## PYMOL
    ##########################
    elif args.function == "PLOT_COMPOUNDS":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")
        parser.add_argument('-path', required=True,help='Directorio de entrada')
        parser.add_argument('-numbers',required = True, type=int,help='Numero de ranking')
        args = parser.parse_args(sub_args)
        PhDlibrary.Plot.plot_pymol_N_compounds(args.path, args.numbers)
    ##########################
    ## REFLEX3D
    ##########################
    elif args.function == "procesar_Reflex3D":
        parser = ArgumentParser(description="Une experimentos en un unico archivo.")
        parser.add_argument('-path', required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.myREFLEX3D.procesar_REFLEX_output(args.path)
    ##########################
    ## DATABASE
    ##########################
    elif args.function == "splitDatabase":
        parser = ArgumentParser(description="Divide una base de datos en tantos archivos como moleculas tenga la base de datos.")
        parser.add_argument('-input', required=True,help='Directorio de entrada')
        parser.add_argument('-output', required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.Database.splitDatabase(args.input, args.output)
    elif args.function == "applyPCA":
        parser = ArgumentParser(description="Divide una base de datos en tantos archivos como moleculas tenga la base de datos.")
        parser.add_argument('-input', required=True,help='Directorio de entrada')
        args = parser.parse_args(sub_args)
        PhDlibrary.Database.applyPCA(args.input)
    ##########################
    ## FULL PROCESS
    #########################
    elif args.function == "N_DUDE_OP":
        parser = ArgumentParser()
        parser.add_argument('-n',required = True, type=int,help='Numero de repeticiones')
        args = parser.parse_args(sub_args)
        
        PhDlibrary.FullProcess.N_DUDE_OP(args.n)
    elif args.function == "N_ADN":
        parser = ArgumentParser()
        parser.add_argument('-n',required = True, type=int,help='Numero de repeticiones')
        args = parser.parse_args(sub_args)
        
        PhDlibrary.FullProcess.N_ADN(args.n)
    elif args.function == "N_MAYBRIDGE_OP":
        parser = ArgumentParser()
        parser.add_argument('-n',required = True, type=int,help='Numero de repeticiones')
        args = parser.parse_args(sub_args)
        PhDlibrary.FullProcess.N_MAYBRIDGE_OP(args.n)

    elif args.function == "completoOPES_DrugBank":
        parser = ArgumentParser()
        parser.add_argument('-n',required = True, type=int,help='Numero de repeticiones')
        args = parser.parse_args(sub_args)
        PhDlibrary.FullProcess.completoOPES_DrugBank(args.n)
    elif args.function == "completoOPSS":
        parser = ArgumentParser()
        parser.add_argument('-n',required = True, type=int,help='Numero de repeticiones')
        args = parser.parse_args(sub_args)
        PhDlibrary.FullProcess.completoOPSS(args.n)
    elif args.function == "evalROCSandZAP":
        parser = ArgumentParser()
        args = parser.parse_args(sub_args)
        PhDlibrary.FullProcess.evalROCSandZAP()
    ##########################
    ## MULTIOBJETIVE
    #########################
    elif args.function == "pareto":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True,
                            help='Archivo donde esta el frente de pareto')
        args = parser.parse_args(sub_args)
        
        PhDlibrary.Multiobjective.plotPareto(args.f)
    elif args.function == "manyPareto":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True,
                            help='Archivo donde esta el frente de pareto')
        args = parser.parse_args(sub_args)
    

        PhDlibrary.Multiobjective.plotManyPareto(args.f)
    elif args.function == "plotManyParetoIndividually":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True,
                            help='Archivo donde esta el frente de pareto')
        args = parser.parse_args(sub_args)
        PhDlibrary.Multiobjective.plotManyParetoIndividually(args.f)
    elif args.function == "selectParetos":
        PhDlibrary.Multiobjective.selectParetos()
    elif args.function == "checkVAR":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True,
                            help='Archivo donde esta el frente de pareto')
        parser.add_argument('-q', required=True,
                            help='Path of query compound')
        parser.add_argument('-v', required=True,
                            help='Path of variable compound')
        args = parser.parse_args(sub_args)
        
        PhDlibrary.Multiobjective.checkVar(args.f, args.q, args.v)
    elif args.function =="selectNonDominatedPoints":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True, nargs='+',
                            help='Archivo donde esta el frente de pareto')
        args = parser.parse_args(sub_args)
        PhDlibrary.Multiobjective.selectNonDominatedPoints(args.f)
    elif args.function== "plotParetosDifferentColors":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True,  nargs='+',
                            help='Archivo donde esta el frente de pareto')
        args = parser.parse_args(sub_args)
        PhDlibrary.Multiobjective.plotParetosDifferentColors(args.f)
    elif args.function == "selectNonDominatedTargets":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True,  nargs='+',
                            help='Archivo donde esta el frente de pareto')
        args = parser.parse_args(sub_args)
        PhDlibrary.Multiobjective.selectNonDominatedTargets(args.f)
    elif args.function == "plotTargetsDifferentColors":
        parser = ArgumentParser()
        parser.add_argument('-f', required=True,  nargs='+',
                            help='Archivo donde esta el frente de pareto')
        args = parser.parse_args(sub_args)
        PhDlibrary.Multiobjective.plotTargetsDifferentColors(args.f)
    
    ##########################
    ## EXTRAS
    #########################
    elif args.function == "cleanFDA":
        parser = ArgumentParser()
        parser.add_argument('-paths',nargs='+',help='folder que quiero borrar')
        args = parser.parse_args(sub_args)
        PhDlibrary.Clean.cleanFDA(args.paths)
    elif args.function == "cleanDrugBank514":
        parser = ArgumentParser()
        parser.add_argument('-path',help='where compounds are')
        args = parser.parse_args(sub_args)
        PhDlibrary.Clean.cleanDrugBank514(args.path)
        
    else:
        print("\nGENERATION methods:")
        for item in GENERACIONlist:
            print("\t", item)
        print("\nPROCESS methods: ")
        for item in PROCESSlist:
            print("\t", item)
        print("\nEVALS methods: ")
        for item in EVALlist:
            print("\t", item)
        print("\nDataframeList methods: ")
        for item in DataframeList:
            print("\t", item)
        print("\nSearchList methods: ")
        for item in SearchList:
            print("\t", item)
        print("\nPlotList methods: ")
        for item in PlotList:
            print("\t", item)
        print("\nFULLList methods: ")
        for item in FullList:
            print("\t", item)    
        print("\nREFLEX3DList methods: ")
        for item in ReflexList:
            print("\t", item)   
        print("\nDataBase methods: ")
        for item in DatabaseList:
            print("\t", item)  
        print("\nExtra methods: ")
        for item in ExtrasList:
            print("\t", item)    
        print("\nMultiobjectives methods: ")
        for item in MultiobjectiveList:
            print("\t", item)

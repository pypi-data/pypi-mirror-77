#!/usr/bin/env python3

import glob
import os
import datetime
import subprocess
import pandas as pd
import shutil
import sys
from Bio import SeqIO
import time
import argparse
from ete3 import Tree
import copy
import itertools
import multiprocessing as mp
from ete3 import Tree, TreeStyle, faces
import fileinput
import zipfile
import traceback
from Bio import AlignIO


"""

TO RUN:
source activate py3

EXAMPLES
python3 sgtree.py proteomes models --num_cpus integer

python3 /global/projectb/scratch/jwhittak/jwhittak/sgtree.py /global/projectb/scratch/jwhittak/jwhittak/try_qual_new_genomes/cont /global/projectb/scratch/jwhittak/jwhittak/final_scripts/uni56 --num_cpus 8 --save_dir /global/projectb/scratch/jwhittak/jwhittak/test_run123 --ref /global/projectb/scratch/jwhittak/jwhittak/1genome

EXAMPLE:
python3 sgtree.py testgenomes/Chloroflexi hmms/UNI56 --num_cpus 8

Possible issues:
fastreeMP does not run... with more than 4 cpus, already parallelized w 3 cpus. <---- test for larger datasets (more models)
"""


parser = argparse.ArgumentParser()
parser.add_argument("genomedir", help="run the script w genome dir provided w/out duplicates",
                    type=str)
parser.add_argument("modeldir", help="run the script w model dir provided w/out duplicates",
                    type=str)
parser.add_argument("ref_concat", help="folder with previously created concat files for reference genomes",
                    type=str)
parser.add_argument("--num_cpus", default=8, help="run the scripts with user provided number of cpus",
                    type=int)
parser.add_argument("--marker_selection", default="no",
                    help="recommended feature, run sgtree without marker selection if no",
                    type=str)
parser.add_argument("--ref", help="run query genomes along with reference database",
                    type=str)
parser.add_argument("--percent_models", default=10, help="eliminate genomes with less than 10 percent of models",
                    type=int)
parser.add_argument("--save_dir", help="new directory name to save to",
                    type=str)
parser.add_argument("--singles", default="no",
                    help="experimental feature with limited testing, remove single markers without number of neighbors",
                    type=str)
# parser.add_argument("--cutoff", default=1, help="score cutoff for genomes",
#                     type=int)
parser.add_argument("--num_nei", default=15, help="number of neighbors to check",
                    type=int)
parser.add_argument("--mafft", default="no", help="run mafft or hmmalign",
                    type=str)

args = parser.parse_args()
start_time = str(datetime.datetime.now())

## make save directory
if args.save_dir == None:
    currentdir = os.getcwd() + "/BG" + "-" + str(args.genomedir.split("/")[-1]) + "-"
    + str(args.modeldir.split("/")[-1]) + "-" + str(start_time.replace(":", "-").replace(" ", "_"))
    currentdir = currentdir.split(".")[0]
    cmd_mk_exdir = ["mkdir", "-p", currentdir]
    mk_dir = subprocess.run(cmd_mk_exdir, stdout=subprocess.PIPE)
else:
    currentdir = args.save_dir
    cmd_mk_exdir = ["mkdir", "-p", currentdir]
    mk_dir = subprocess.run(cmd_mk_exdir, stdout=subprocess.PIPE)

## initialize vars
genomes = args.genomedir
uni56 = args.modeldir
num_cpus = args.num_cpus
percent_models = args.percent_models
ref_concat = args.ref_concat

## vv making reference directory concat files
if args.ref != None:
    ref = str(args.ref)
    ls_refs = os.listdir(str(args.ref))
    if os.path.exists(ref_concat + "/" + ref.split("/")[-1] + "_" + uni56.split("/")[-1] + "/" + "tree.nwk"):
        print("already have files for references")

    else:
        cmd_runprog = ["python3", "/mnt/sgtree/sgtree.py", ref, uni56, ref_concat, "--num_cpus", str(1),
                       "--save_dir", ref_concat + "/" + ref.split("/")[-1] + "_" + uni56.split("/")[-1]]
        print(cmd_runprog)
        subprocess.run(cmd_runprog, stdout=subprocess.PIPE)

else:
    ref = str(args.ref)
    ls_refs = None
    print("no reference directory")

print("init", args.genomedir, args.modeldir, currentdir, str(args.num_cpus), args.percent_models, str(args.ref),
      "--marker_selection", args.marker_selection)

## see fi we have already run in this directory if so we remove the tree and all other files.


try:

    if os.path.isfile(currentdir + "/tree.nwk") or os.path.isfile(currentdir + "/tree_final.nwk"):
        for file in glob.glob(currentdir + "/*", recursive=True):
            if os.path.isdir(file):
                shutil.rmtree(file)
            else:
                os.remove(file)

    # write color file for ITOL.
    with open(currentdir + "/color.txt", 'w') as myfile:
        myfile.write("DATASET_COLORSTRIP")
        myfile.write("\n")
        myfile.write("SEPARATOR SPACE")
        myfile.write("\n")
        myfile.write("DATASET_LABEL label1")
        myfile.write("\n")
        myfile.write("COLOR #ff0000")
        myfile.write("\n")
        myfile.write("COLOR_BRANCHES 0")
        myfile.write("\n")
        myfile.write("DATA")
        myfile.write("\n")
        for filename in glob.glob(genomes + "/*", recursive=True):
            myfile.write(filename.split("/")[-1].split(".")[0] + " " + "#FF0000")
            myfile.write("\n")
        for filename in glob.glob(ref + "/*", recursive=True):
            myfile.write(filename.split("/")[-1].split(".")[0] + " " + "#C0C0C0")
            myfile.write("\n")


    def concat():
        """
        concat takes models and genomes and concatenates them into single files (uni56 and genomes), returns number of models
        also writes color.txt.
        """
        model_count = 0
        destination = open(currentdir + "/" + "models", 'w+')
        for filename in glob.glob(uni56 + "/*", recursive=True):
            model_count += 1
            shutil.copyfileobj(open(filename, 'r+'), destination)
        destination.close()

        destinationfaa = open(currentdir + "/" + "proteomes", 'w+')
        if os.path.isdir(genomes):
            for filename in glob.glob(genomes + "/*.faa", recursive=True):
                shutil.copyfileobj(open(filename, 'r+'), destinationfaa)
            destinationfaa.close()
        else:
            for filename in glob.glob(genomes, recursive=True):
                print("copying", filename)
                shutil.copyfileobj(open(filename, 'r+'), destinationfaa)
            destinationfaa.close()
        return model_count


    modelfam = currentdir + "/" + "models"
    genomesfaa = currentdir + "/" + "proteomes"

    model_count = concat()

    ## run HMMSEARCH and save output to hitsoutdir
    hitsoutdir = currentdir + "/hits.hmmout"
    cmd_search = ["hmmsearch", "--cut_ga", "--cpu", str(4), "--domtblout", hitsoutdir, "--noali", modelfam, genomesfaa]
    ran_hmmsearch_time = datetime.datetime.now()
    search_datetime = time.time()
    print(cmd_search)
    capture_search = subprocess.run(cmd_search, stdout=subprocess.PIPE)
    search_runtime = time.time() - search_datetime
    print("HMMsearch runtime", search_runtime)

    ## make tables
    cmd_mk_exdir = ["mkdir", "-p", currentdir + "/tables"]
    mk_dir = subprocess.run(cmd_mk_exdir, stdout=subprocess.PIPE)

    min_models = percent_models / 100
    dict_counts = {}
    print("MINIMUM MODELS", min_models)


    ## OPTION: paralellize this
    def clean_df(df_dir):
        """ takes a df, makes a dictionary format: {genome:
        {model1: #occurences, model2: #occurences, etc...]},
        if the length of this list is less than the user specified flag this
        all the rows containing this genome is eliminated from the final_df. It also writes the count matrix
        and number different markers plots"""
        df = pd.read_csv(df_dir)
        df = df[~df[str(df.columns[0])].str.startswith('#')]
        vs = pd.Series()
        for col in df.columns[~df.columns.isin(['row_name'])]:
            vs = vs.append(df[col].str.split('\s+'))
        tempdf = vs.groupby(vs.index).sum().to_frame()
        finaldf = pd.DataFrame(tempdf[0].values.tolist())
        for row in finaldf.iterrows():
            name = row[1][0].split("|")[0]
            model = row[1][3]
            if name in dict_counts.keys():
                if model in dict_counts[name].keys():
                    dict_counts[name][model] += 1
                else:
                    dict_counts[name][model] = 1
            else:
                dict_counts[name] = {}
        ## make a list of incomplete genomes here then check if it reaches the percentage we care about w len(dict_counts[each]).
        incomplete_genomes = []
        for each in dict_counts.keys():
            if len(dict_counts[each]) < (model_count * (min_models)):
                incomplete_genomes.append(each)
        index = 0
        rows_deleted = 0
        for row in finaldf.copy().iterrows():
            name = row[1][0].split("|")[0]
            model = row[1][3]
            if name in incomplete_genomes:
                finaldf = finaldf.drop([index])
                rows_deleted += 1
            index += 1
        with open(currentdir + "/log_genomes_removed.txt", "w") as myfile:
            incom = '\n'.join(incomplete_genomes)
            myfile.write(incom)
        print("AFTER hmmout", finaldf.shape, "# rows deleted", rows_deleted)
        count_mat = pd.DataFrame.from_dict(dict_counts)
        count_mat.to_csv(currentdir + "/marker_count_matrix.csv")
        return finaldf


    def make_df():
        """
        read the table from hitsoutdir, keeps only a certain number of duplicates, as seen in (tables/) duplicates namemodel,
        dropped_namemodel and merged final.
        """
        try:
            finaldf = clean_df(hitsoutdir)
            finaldf["savedname"] = finaldf[0]
            finaldf["savedname"] = finaldf["savedname"].apply(lambda c: c.replace("|", "/"))
            df = finaldf.applymap(lambda x: x.split("|")[0])
            df['namemodel'] = df[0] + "/" + df[3]
            ## Possible problem here:
            df = df.drop_duplicates(subset='savedname', keep='first')
            df.to_csv(currentdir + "/tables/before_drops_elim_incompletes")
            # IMPORTANT:        ## FLAG if 5 > len > 1, keep max of 5 duplicates
            ## OPTION PARRALELLIZE.
            helperdf = pd.concat(g for _, g in df.groupby("namemodel") if 5 >= len(g) >= 1)
            ## CHANGE FIVE TO USER SPECIFIED FLAG.
            helperdf.to_csv(currentdir + "/tables/duplicates_namemodel")
            newdf = df.drop_duplicates(subset='namemodel', keep=False)
            newdf.to_csv(currentdir + "/tables/dropped_namemodel")
            df = pd.merge(helperdf, newdf, how='outer')
            df.to_csv(currentdir + "/tables/merged_final")
            return df
            # drop duplicates might not be the be the fastest way, compare the third and the first fields somehow?
        except KeyError:
            print("Key error: because you have already made " +
                  "the dataframe so it isn't formatted this way anymore." + "\n" + "error:", sys.exc_info())
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


    df = make_df()
    if args.ref != None:
        df_ref = pd.read_csv(ref_concat + "/" + ref.split("/")[-1]
                             + "_" + uni56.split("/")[-1] + "/tables/merged_final")
        df = df.append(df_ref)

    ## make table fordups, which is the same thing as df except with the index as the saved name for easy access later when we
    ## remove all duplicates that are not the highest score for the construction of initial species tree.
    # df = pd.read_csv(currentdir + "/tables/merged_final")
    df_fordups = df.set_index(df["savedname"])
    df_fordups.to_csv(currentdir + "/table_elim_dups")

    ## make extracted directory.
    cmd_mk_exdir = ["mkdir", "-p", currentdir + "/extracted"]
    mk_dir = subprocess.run(cmd_mk_exdir, stdout=subprocess.PIPE)
    extracted_dir = currentdir + "/extracted"


    ## make initiate file so we can loop through files in parsefunc_extract
    # with open(extracted_dir + "/" + "initiation", "a") as myfile:
    #     myfile.write("")

    def parsefunc_extract(row_string, modelstr):
        """
        This function writes the files in extract, making a list of the prtein sequences from each genome that
        have hits for a a certain model,
        OPTION: FORLOOP
        """
        count = 0
        ls_of_files = os.listdir(extracted_dir)
        for filename in ls_of_files:
            count += 1
            if filename == modelstr:
                with open(extracted_dir + "/" + filename, "a") as myfile:
                    myfile.write(row_string + "\n")
                    break
            ## if weve searched all the files and we havent this model yet, then make it.

    def edit_df(index):
        """
        Edit a row of DF, making savedname which is the fullname, and namemodel, which is the genome/model.
        """
        return (df.iloc[index]["savedname"].replace("/", "|"), df.iloc[index]["namemodel"].split("/")[1])


    def extract(ls):
        """
        first maps the edit_df function which takes a row of df (index) and rewrites the row to have name/model and
        saved name columns then returns it as input to this function. parsefunc extract then wrties the files.
        """
        try:
            pool = mp.Pool(num_cpus)
            pool.starmap(parsefunc_extract, [(pair[0], pair[1]) for pair in ls])
            pool.close()
            pool.join()
        except:
            print("multi error", sys.exc_info()[0], sys.exc_info()[2])

    ran_extraction_time = datetime.datetime.now()
    extraction_datetime = time.time()

    pool = mp.Pool(num_cpus)
    empty = pool.map(edit_df, [index for index in range(0, len(df))])
    ls_seq_model = empty
    pool.close()
    pool.join()

    ## initiate all the files so that when we start adding hits we cna
    ## search through all of them in parsefunc.
    make_file_ls = set(
        list(map(lambda item: item[1], ls_seq_model)))  ## get unique models from list of hits/model from df.


    def write_init(model):
        """ writes an empty file to append to in parsefunc for a model"""
        with open(extracted_dir + "/" + model, "w") as myfile:
            myfile.write("")


    pool = mp.Pool(num_cpus)
    empty = pool.map(write_init, [model for model in make_file_ls])
    pool.close()
    pool.join()


    # OPTION: ADD CHECK HERE!!!
    def Diff(li1, li2):
        return list(set(li1) - set(li2))


    dff = Diff(list(map(lambda x: x + ".hmm", make_file_ls)),
               list(map(lambda x: x.split("/")[-1], glob.glob(genomes + "/*", recursive=True))))

    ## run extract
    extract(ls_seq_model)

    extract_runtime = time.time() - extraction_datetime
    print("extract runtime", extract_runtime)


    ##############################

    def write_extr_seqs(file):
        """
        takes the files in extracted and then gets the correspoding sequence writing it to extracted_seqs.
        OPTION: PARRALELLIZE FORLOOP
        """
        try:
            with open(file, "r") as myfile:
                ls_of_seq = myfile.read().split("\n")
                seq_count = 0
                for seq in ls_of_seq:
                    seq_count += 1
                    filename = currentdir + "/" + "proteomes"
                    exists = os.path.isfile(filename)
                    ## check whether sequence comes from reference or query database ^^ genomes +"/".
                    if not exists:
                        filename = ref + "/" + seq.split("|")[0] + ".faa"
                    hmm_match = file.split("/")[-1]
                    record_dict = SeqIO.index(filename, "fasta")
                    try:
                        with open(extracted_seqs + "/" + hmm_match + ".faa", "a") as output_handle:
                            SeqIO.write(record_dict[seq], output_handle, "fasta")
                    except:
                        if args.ref != None:
                            pass
                        else:
                            print("Error for writing extracted sequences", traceback.format_exc())
                    if seq_count == len(ls_of_seq) - 1:
                        break

        except:
            print("Error for writing extracted sequences", traceback.format_exc())


    ## Makes extracted seqs directory.
    cmd_mk_dir = ["mkdir", "-p", currentdir + "/extracted_seqs"]
    mk_dir = subprocess.run(cmd_mk_dir, stdout=subprocess.PIPE)
    extracted_seqs = currentdir + "/extracted_seqs"

    ## for each of the lists in extracted extract the sequence and write to extracted seqs.
    ## first get a list of all thefiles in extracted.

    ls_of_files = glob.glob(extracted_dir + "/*", recursive=True)

    if len(ls_of_files) + 1 == model_count:
        pool = mp.Pool(num_cpus)
        pool.map(write_extr_seqs, [file for file in ls_of_files])
        pool.close()
        pool.join()
    else:
        pool = mp.Pool(num_cpus)
        pool.map(write_extr_seqs, [file for file in ls_of_files])
        pool.close()
        pool.join()

    ## 1) make aligned dir to put mafft into, and define out directories.
    # 1

    if args.ref != None:
        def copy_file_content(file):
            fin = open(ref_concat + "/" + ref.split("/")[-1] + "_" + uni56.split("/")[-1] +
                       "/extracted_seqs/" + file.split("/")[-1] + ".faa", "r")
            data2 = fin.read()
            fin.close()
            fout = open(currentdir + "/extracted_seqs/" + file.split("/")[-1] + ".faa", "a")
            fout.write(data2)
            fout.close()


        if ref != None:
            pool = mp.Pool(num_cpus)
            pool.map(copy_file_content, [file for file in ls_of_files])
            pool.close()
            pool.join()

    cmd_mk_aldir = ["mkdir", "-p", currentdir + "/aligned"]
    mk_dir = subprocess.run(cmd_mk_aldir, stdout=subprocess.PIPE)
    aligned_dir = currentdir + "/aligned"

    ## set up runtime for mafft.
    ran_mafft_time = datetime.datetime.now()
    mafft_datetime = time.time()


    def run_mafft(file):
        """
        takes a file of extracted sequences and runs mafft on them, storing them in the aligned directory.
        """
        try:
            with open(extracted_seqs + "/" + file, "r") as myfile:
                if file == ".DS_Store":
                    print("ignoring DS store")
                else:
                    aligned_dest = aligned_dir + "/" + file
                    filename = extracted_seqs + "/" + file
                    ## OPTION THREAD NUM FOR MAFFT
                    cmd_runmafft = ["mafft", "--auto", "--thread", str(4), "--quiet", filename]
                    print(cmd_runmafft)
                    mafft_result = subprocess.run(cmd_runmafft, stdout=subprocess.PIPE)
                    with open(aligned_dest, "w") as myfile:
                        myfile.write(mafft_result.stdout.decode('utf-8') + "\n")
        except:
            print("Unexpected error for mafft initial SpecTree_alignment:", sys.exc_info()[0])
            raise


    def run_hmmalign(file):
        """
        takes a file of extracted sequences and runs mafft on them, storing them in the aligned directory.
        """
        try:
            with open(extracted_seqs + "/" + file, "r") as myfile:
                if file == ".DS_Store":
                    print("ignoring DS store")
                else:
                    aligned_dest = aligned_dir + "/" + file
                    filename = extracted_seqs + "/" + file
                    ## OPTION THREAD NUM FOR MAFFT
                    model = file.split(".")[0]
                    modfile = uni56 + "/" + model + ".hmm"
                    cmd_aln = ["hmmalign", "--trim", "-o", aligned_dir + "/" + model + ".sto", modfile, filename]
                    print(cmd_aln)
                    align_result = subprocess.run(cmd_aln, stdout=subprocess.PIPE)
                    aln = AlignIO.read(aligned_dir + "/" + model + ".sto", "stockholm")
                    AlignIO.write(aln, aligned_dir + "/" + model + ".faa", "fasta")

                for line in fileinput.input(aligned_dir + "/" + model + ".faa", inplace=True):
                    line = line.rstrip()
                    if not line:
                        continue
                    if '>' in line:
                        print("|".join(line.split("|")[0:]))
                    else:
                        print(line)
        except:
            print("Unexpected error for mafft initial SpecTree_alignment:", sys.exc_info()[0])
            raise


    ## for each of the files in extracted_seqs run mafft and put in aligned.

    if args.mafft == "no":
        ls_of_files = glob.glob(extracted_seqs + "/*", recursive=True)
        pool = mp.Pool(num_cpus)
        pool.map(run_hmmalign, [file.split("/")[-1] for file in ls_of_files])
        pool.close()
        pool.join()
    else:
        ls_of_files = glob.glob(extracted_seqs + "/*", recursive=True)
        pool = mp.Pool(num_cpus)
        pool.map(run_mafft, [file.split("/")[-1] for file in ls_of_files])
        pool.close()
        pool.join()

    mafft_runtime = time.time() - mafft_datetime
    print("MAFFT/hmmalign runtime", mafft_runtime)

    ##############################
    ## make aln_SpecTree directory.
    cmd_mk_dir = ["mkdir", "-p", currentdir + "/aln_SpecTree"]
    mk_dir = subprocess.run(cmd_mk_dir, stdout=subprocess.PIPE)
    aln_SpecTree_dir = currentdir + "/aln_SpecTree"


    # duplicate: checks if ID is in ls_ids
    def duplicate(id, ls_ids):
        for match in ls_ids:
            if id == match:
                return True
        else:
            return False


    # get_score: takes a string of the full identifier, looks up its score in df, and spits out the "identifier_score".
    def get_score(identifier):
        return df_fordups.loc[identifier.replace("|", "/")]["savedname"] + ":" + str(
            df_fordups.loc[identifier.replace("|", "/")][7])


    # takes a list of ids and scores and deletes the id that has the best score from the list.
    def del_best_score(ls):
        lst = list(map(lambda str: str.split(":")[1], ls))
        lst = list(map(lambda str: float(str), lst))
        largest = max(lst)
        for id_score in ls:
            if float(id_score.split(":")[1]) == largest:
                ls.remove(id_score)
        return ls


    ## remove an item from a list
    def del_item(item, ls):
        for id_score in ls:
            if id_score == item:
                ls.remove(item)
        return ls


    def elim_dups(file):
        """
        for a model in the aligned directory, eliminate any duplicates for a genome
        that is not the highest score from HMM search.
        """
        try:
            dups = {}
            with open(file, "r+") as myfile:
                record_dict = SeqIO.to_dict(SeqIO.parse(file, "fasta"))
                for key in record_dict:
                    ls = list(record_dict.keys())
                    lscopy = list(ls)
                    lscopy.remove(key)
                    if duplicate(key.split("|")[0], list(map(lambda k: k.split("|")[0], lscopy))):
                        if key.split("|")[0] in dups:
                            dups[key.split("|")[0]] = dups[key.split("|")[0]] + "," + key
                        else:
                            dups[key.split("|")[0]] = key

                for key, value in dups.items():
                    dups[key] = value.split(",")
                    dups[key] = list(map(lambda value: get_score(value), dups[key]))
                # delete the best scoring ids from the list of duplicates.
                for key, value in dups.items():
                    dups[key] = del_best_score(dups[key])
                for key, value in dups.items():
                    for each in value:
                        del_item(each.split(":")[0].replace("/", "|"), ls)
                for key in record_dict.copy():
                    if not (key in ls):
                        del record_dict[key]
                # ^^ if a key is in record dict which is not in our list of cleaned proteins (without best score)
                # (ls) delete it. ^^
                for key in record_dict.keys():
                    with open(aln_SpecTree_dir + "/" + file.split("/")[-1], "a") as output_handle:
                        SeqIO.write(record_dict[key], output_handle, "fasta")

        except:
            print("elimination of duplicates exception", sys.exc_info())
            raise


    ## for each of the files in extracted_seqs run mafft and put in aligned.
    ran_aln_SpecTree_time = datetime.datetime.now()
    aln_SpecTree_datetime = time.time()

    ls_of_files = glob.glob(aligned_dir + "/*.faa", recursive=True)
    pool = mp.Pool(num_cpus)
    pool.map(elim_dups, [file for file in ls_of_files])
    pool.close()
    pool.join()

    aln_SpecTree_runtime = time.time() - aln_SpecTree_datetime
    print("aligned to aln_SpecTree runtime", aln_SpecTree_runtime)


    ##############################
    def run_trimal(file):
        """
        takes a file and runs trimal on it, saving the output into a corresponding filename in trimmed_SpeciesTree.
        """
        print("Running trimal on FILE:", file)
        try:
            with open(file, "r") as myfile:
                destination_file = trimmed_dir + "/" + file.split("/")[-1]
                cmd_run_trimal = ["trimal", "-in", file, "-out", destination_file, "-gt", "0.1"]
                capture_trimal = subprocess.run(cmd_run_trimal, stdout=subprocess.PIPE)
                for line in fileinput.input(file, inplace=True):
                    line = line.rstrip()
                    if not line:
                        continue
                    if '>' in line:
                        print("|".join(line.split("|")[0:]))
                    else:
                        print(line)

        except:
            print("Unexpected error for trimal:", sys.exc_info()[0])
            raise


    ## make trimmed species directory
    cmd_mk_trdir = ["mkdir", "-p", currentdir + "/trimmed_SpeciesTree"]
    mk_dir = subprocess.run(cmd_mk_trdir, stdout=subprocess.PIPE)
    trimmed_dir = currentdir + "/trimmed_SpeciesTree"

    ## run trimal on every file in aln_SpecTree
    ran_trimal_time = datetime.datetime.now()
    trimal_datetime = time.time()

    ls_of_files = glob.glob(aln_SpecTree_dir + "/*", recursive=True)
    pool = mp.Pool(num_cpus)
    pool.map(run_trimal, [file for file in ls_of_files])
    pool.close()
    pool.join()

    trimal_runtime = time.time() - trimal_datetime
    print("trimal runtime", trimal_runtime)
    ##############################
    ran_concat_time = datetime.datetime.now()
    concat_datetime = time.time()


    def trimmed_to_df():
        """
        takes files in the trimmed directory and puts them all in a table for replacement of NaNs.
        """
        try:
            df_conc = pd.DataFrame(columns=['SeqID'])
            for file in glob.glob(trimmed_dir + "/*", recursive=True):
                record_dict = SeqIO.to_dict(SeqIO.parse(file, "fasta"))
                record_dict = {k: v.format("fasta").split("\n", 1)[1] for k, v in record_dict.items()}
                new_dict = dict()
                for key in record_dict.keys():
                    new_dict[key.split("|")[0]] = record_dict[key]
                    new_df = pd.DataFrame(list(new_dict.items()), columns=['SeqID', file.split("/")[-1]])
                df_conc = pd.merge(new_df, df_conc, how='outer')
            return df_conc
        except:
            print("Unexpected error for production of initial df in concat:", sys.exc_info()[0])


    global df_conc
    df_conc = trimmed_to_df()


    def rem_NaN():
        """
        takes a cell in the table if its none, replace it with right number of X, else replace the "\n".
        cannot be fully parralellized because needs to remember len_string.
        """
        try:
            for j in range(1, df_conc.shape[1]):
                len_string = 0
                for i in range(0, df_conc.shape[0]):
                    if isinstance(df_conc.loc[i][j], float):
                        if len_string == 0:
                            x = "this better be the first row otherwise this breaks."
                        else:
                            df_conc.loc[i].iat[j] = "X" * (len_string)
                    else:
                        len_string = len(df_conc.loc[i][j].replace("\n", ""))
        except:
            print("Unexpected error for production df_concatenated, rem_NaN", sys.exc_info()[0])


    ## run rem NaN on every cell in the table.
    rem_NaN()


    def rem_rest():
        """
        replaces for first and last lines, which are not considered in the first round.
        """
        try:
            for index in range(1, df_conc.shape[1]):
                if isinstance(df_conc.loc[0][index], float):
                    count = 0
                    for i in range(1, len(df_conc.index)):
                        if not (isinstance(df_conc.loc[count][index], float)):
                            break
                        else:
                            df_conc.loc[count].iat[index] = "X" * len(
                                df_conc.loc[len(df_conc.index) - 1][index].replace("\n", ""))
                            count += 1
        except:
            print("Unexpected error for production df_concatenated, rem_rest", sys.exc_info()[0])


    ## run rem_rest on every column for important indicies.
    rem_rest()

    ## make concat directory, convert df_conc to a record dict, and write the record dict to the concatenated.faa.
    cmd_mk_concdir = ["mkdir", "-p", currentdir + "/concat"]
    mk_dir = subprocess.run(cmd_mk_concdir, stdout=subprocess.PIPE)
    concat_dir = currentdir + "/concat/concatenated.faa"

    try:
        df_conc.to_csv(currentdir + "/tables/table_df_concatenated_w_X")
    except:
        print("Cant write table")

    df_conc = pd.read_csv(currentdir + "/tables/table_df_concatenated_w_X")
    df_conc = df_conc.set_index('SeqID')
    record_dict = df_conc.T.to_dict('list')
    record_dict = {k: v[1::] for k, v in record_dict.items()}
    record_dict = {k: ''.join(v) for k, v in record_dict.items()}
    record_dict = {k: v.replace("\n", "") for k, v in record_dict.items()}
    with open(concat_dir, "w") as myfile:
        for k, v in record_dict.items():
            myfile.write(">" + k + "\n" + v + "\n")

    concat_runtime = time.time() - concat_datetime
    print("concat runtime", concat_runtime)

    ##############################
    ran_Fastree_time = datetime.datetime.now()
    Fastree_datetime = time.time()

    try:
        concat_dir = currentdir + "/concat/concatenated.faa"
        tree_dir = currentdir + "/" + "tree.nwk"
        cmd_runFastree = ["FastTree", "-quiet", "-out", tree_dir, concat_dir]
        FastTree_result = subprocess.run(cmd_runFastree, stdout=subprocess.PIPE)
    except:
        print("Unexpected error for Fastree no duplicates:", sys.exc_info()[0])
        raise

    Fastree_runtime = time.time() - Fastree_datetime
    print("Fastree_runtime", Fastree_runtime)
    #######################
    logfile_dir = currentdir + "/logfile_"
    logfile = logfile_dir + str(start_time) + ".txt"

    try:
        with open(logfile, "w") as myfile:
            myfile.write(currentdir + "\n" + ("=" * 80) + "\n"
                         + "Sg_Tree v.2" + "\n" + "start time: " + start_time
                         + "\n" + ("=" * 80) + "\n"
                         + "Genomes database " + genomes + " contains "
                         + str(len(glob.glob(genomes, recursive=True))) + " genomes"
                         + "\n" + ("=" * 80) + "\n"
                         + "Marker database " + uni56 + " contains "
                         + str(len(glob.glob(uni56, recursive=True))) + " models"
                         + "\n" + ("=" * 80) + "\n")
            myfile.write(str(ran_hmmsearch_time) + "- running hmmsearch v.3.0")
            myfile.write("\n" + "marker protein detection done - runtime: "
                         + str(search_runtime)
                         + " seconds"
                         + "\n" + ("=" * 80) + "\n")
            myfile.write(str(ran_extraction_time) + "- ...extracting best hits")
            myfile.write("\n" + "extraction of best hits done - runtime: "
                         + str(extract_runtime)
                         + " seconds"
                         + "\n" + ("=" * 80) + "\n")
            myfile.write(str(ran_mafft_time) + "- ...running mafft v.")
            myfile.write("\n" + "alignment done - runtime:  "
                         + str(mafft_runtime)
                         + " seconds"
                         + "\n" + ("=" * 80) + "\n")

            myfile.write(str(ran_trimal_time) + "- ...running trimal v.?")
            myfile.write("\n" + "trimming done - runtime: "
                         + str(trimal_runtime)
                         + " seconds"
                         + "\n" + ("=" * 80) + "\n")
            myfile.write(str(ran_concat_time) + "- ...creating supermatrix")
            myfile.write("\n" + "supermatrix created - runtime: "
                         + str(concat_runtime)
                         + " seconds"
                         + "\n" + ("=" * 80) + "\n")
            myfile.write(str(ran_Fastree_time) + "- ...running FastTree v.")
            # TO DO: update versions somehow?
            myfile.write("\n" + "FastTree done - total runtime: "
                         + str(Fastree_runtime)
                         + " seconds"
                         + "\n" + ("=" * 80) + "\n")
            myfile.write("Sgtree endtime: " + "\n"
                         + str(datetime.datetime.now())
                         + " seconds"
                         + "\n" + str(len(glob.glob(genomes + "/*", recursive=True))) + " genomes"
                         + "\n" + str(len(glob.glob(uni56 + "/*", recursive=True))) + " models"
                         + "\n" + start_time
                         + "\n" + str(datetime.datetime.now()))
    except FileExistsError:
        print("Unexpected error creating log file", sys.exc_info())
    except:
        print("Unknown Error for logfile", sys.exc_info())

except Exception as e:
    print("ERROR FOR WRITING STDOUT OF SGTREE_PIPE init.py", e.__doc__, "\n", str(e))
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

#####
if args.marker_selection == "yes":
    try:
        def run_trimal(file):
            """
            takes a file and runs trimal on it, saving the output into a corresponding filename in trimmed_ProtTrees
            """
            print("Running trimal on FILE:", file)
            try:
                with open(file, "r") as myfile:
                    destination_file = trimmed_dir + "/" + file.split("/")[-1]
                    cmd_run_trimal = ["trimal", "-in", file, "-out", destination_file, "-gt", "0.1"]
                    capture_trimal = subprocess.run(cmd_run_trimal, stdout=subprocess.PIPE)
            except:
                pass


        ## make trimmed prot Trees
        cmd_mk_trdir = ["mkdir", "-p", currentdir + "/trimmed_protTrees"]
        mk_dir = subprocess.run(cmd_mk_trdir, stdout=subprocess.PIPE)
        trimmed_dir = currentdir + "/trimmed_protTrees"
        aligned_dir = currentdir + "/aligned"

        ## run trimal on every file in aligned (with duplicates in it)
        ran_trimal_time = datetime.datetime.now()
        trimal_datetime = time.time()

        ls_of_files = glob.glob(aligned_dir + "/*", recursive=True)
        pool = mp.Pool(num_cpus)
        pool.map(run_trimal, [file for file in ls_of_files])
        pool.close()
        pool.join()

        trimal_runtime = time.time() - trimal_datetime
        print("trimal runtime", trimal_runtime)
        ##############################
        ## make directory for treeouts
        cmd_mk_treedir = ["mkdir", "-p", currentdir + "/treeouts_protTrees"]
        mk_dir = subprocess.run(cmd_mk_treedir, stdout=subprocess.PIPE)

        ran_Fastree_time = datetime.datetime.now()
        Fastree_datetime = time.time()


        def run_Fastree(file):
            try:
                tree = currentdir + "/" + "treeouts_protTrees" + "/" + file.split("/")[-1] + "_" + "tree.out"
                cmd_runFastree = ["FastTree", "-quiet", "-out", tree, file]
                print("Running Fastree", cmd_runFastree)
                FastTree_result = subprocess.run(cmd_runFastree, stdout=subprocess.PIPE)
                print((FastTree_result.stdout.decode('utf-8')))
            except:
                print("Unexpected error for FastreeMP:", sys.exc_info()[0])
                raise


        ## Run Fastree for every directory in the trimmed directory.
        ls_of_files = glob.glob(trimmed_dir + "/*", recursive=True)
        ## OPTION
        pool = mp.Pool(4)
        pool.map(run_Fastree, [file for file in ls_of_files])
        pool.close()
        pool.join()

        Fastree_runtime = time.time() - Fastree_datetime
        print("Fasttree runtime", Fastree_runtime)
        ##############################
        ## make relevant directories.
        cmd_mk_treesdir1 = ["mkdir", "-p", currentdir + "/protTrees"]
        mk_dir = subprocess.run(cmd_mk_treesdir1, stdout=subprocess.PIPE)

        cmd_mk_treesdir = ["mkdir", "-p", currentdir + "/protTrees/no_duplicates"]
        mk_dir = subprocess.run(cmd_mk_treesdir, stdout=subprocess.PIPE)

        cmd_mk_treesdire = ["mkdir", "-p", currentdir + "/protTrees/no_duplicates/out"]
        mk_dir = subprocess.run(cmd_mk_treesdire, stdout=subprocess.PIPE)

        cmd_mk_treesdires = ["mkdir", "-p", currentdir + "/protTrees/no_singles"]
        mk_dir = subprocess.run(cmd_mk_treesdires, stdout=subprocess.PIPE)

        cmd_mk_treesdires1 = ["mkdir", "-p", currentdir + "/removed"]
        mk_dir = subprocess.run(cmd_mk_treesdires1, stdout=subprocess.PIPE)


        def get_ascore(identifier):
            """gets a score for a given sequence"""
            dfa = pd.read_csv(currentdir + "/table_elim_dups")
            dfa = dfa.set_index(dfa["savedname"])
            return dfa.loc[identifier.replace("|", "/")]["savedname"] + ":" + str(
                dfa.loc[identifier.replace("|", "/")][8])


        def best_score(lst):
            """gets a score for a given slist of sequences"""
            ls = list(map(lambda str: str.split(":")[1], lst))
            ls = list(map(lambda str: float(str), ls))
            largest = max(ls)
            for each in lst:
                if float(each.split(":")[1]) == largest:
                    return each


        def removekey(d, key):
            """removes a key from a dictionary without mutating existing dict"""
            r = dict(d)
            del r[key]
            return r


        def Diff(li1, li2):
            return list(set(li1) - set(li2))


        def run_Noperm(file):
            """does marker selection for a tree out file, first it makes lst ndoes which is all the nodes in the tree
            it makes a seen dict of all the nodes, checking if there are duplicates, then it makes dups which is a list of nodes
            and thier scores, multiple values in this dict if there are duplicates, after that it compares RF distances generated from trees pruned for duplicates"""
            t = Tree(file)
            lst_nodes = [node.name for node in next(t.copy().traverse())]
            seen = {}

            ### NUMBER OF UNIQUE NODES IN LST NODES FROM SEEN
            for x in lst_nodes:
                if x.split("|")[0] not in seen:
                    seen[x.split("|")[0]] = x
                elif x.split("|")[0] in seen:
                    seen[x.split("|")[0]] = seen[x.split("|")[0]] + "," + x

            d2 = dict((k, v.split(",")) for k, v in seen.items())
            dups = d2

            for key, value in dups.items():
                dups[key] = list(map(lambda value: get_ascore(value), dups[key]))
            speciestree = Tree(currentdir + "/tree.nwk")
            ls_best_nodes = []
            bad_nodes = []
            for key, value in dups.items():
                ## check if node in refs if it is we skip this step.
                if key.split("|")[0] + ".faa" in ls_refs:
                    continue
                if len(value) == 1:
                    continue
                rdist = 10000
                for each in value:
                    bad_nodes.append(each)
                for each in value:
                    ## make list of nodes we're going to prune our marker tree with.
                    ls_nodes = []
                    ls_nodes.append(each)
                    ## first we append the duplicate we're lookign at.
                    dcopy = removekey(dups, key)
                    ## remove the key in the dict for that duplicate^^, vv then append the best score for everything else in the tree.
                    for k, v in dcopy.items():
                        ls_nodes.append(best_score(v))

                    ## replace everything with correct names
                    alt = list(map(lambda str: str.split(":")[0].replace("/", "|"), ls_nodes))

                    ## prune the species tree for the genomes we're considering for this protein marker.
                    speciestree.prune([node.split("|")[0] for node in alt])

                    ## prune the marker tree for the genmoes ""    ""    ""    ""
                    t_prot = t.copy()
                    t_prot.prune(alt)
                    t_protcopy = t_prot.copy()

                    ## change node names so we cna compare to species tree which does not have sequence identifiers (seq ids after "|")
                    for node in next(t_protcopy.traverse()):
                        node.name = node.name.split("|")[0]


                    rf, maxrf, get, y, a, x, z = speciestree.robinson_foulds(t_protcopy, unrooted_trees=True)
                    maxrf = maxrf + .0001
                    if rf / maxrf <= rdist:
                        rdist = rf / maxrf
                        best_tree = t_prot
                        best_tree_file = file
                        best_each = each
                ls_best_nodes.append(best_each)
                bad_nodes.remove(best_each)
            bad_nodes = list(map(lambda str: str.split(":")[0].replace("/", "|"), bad_nodes))

            with open(currentdir + "/removed/" + file.split("/")[-1].split(".")[0], 'w') as f:
                for item in bad_nodes:
                    f.write("%s\n" % item)
                f.write("%s\n" % str(len(bad_nodes)) + " " + str(len(lst_nodes)) + "\n" + str((80 * "*")))

            t_final = t.copy()

            for each in lst_nodes.copy():
                if each in bad_nodes:
                    lst_nodes.remove(each)

            t_final.prune(lst_nodes)
            t_final.write(format=1, outfile=currentdir + "/protTrees/no_duplicates/out" + "/" + "_no_dups_" +
                                            file.split("/")[-1].split(".")[0] + "_" + ".nw")
            best_tree = t_final


        ## run noperm on everything in the tree
        ran_Fastree_time = datetime.datetime.now()
        Fastree_datetime = time.time()

        ls_of_files = glob.glob(currentdir + "/" + "treeouts_protTrees" + "/*", recursive=True)

        try:
            pool = mp.Pool(num_cpus)
            pool.map(run_Noperm, [file for file in ls_of_files])
            pool.close()
            pool.join()
        except:
            print("ERROR for marker selection:", sys.exc_info()[0])
            raise

        files = glob.glob(currentdir + "/protTrees/no_duplicates/out" + "/" + "/*")


        def score_func(ls_mod, ls_in):
            score = 0
            for init in ls_in:
                i = 0
                ## get index of this marker in each of the lists, then absolute difference
                ## between those is substracted from total possible score for each init which is length of list.
                if init in ls_mod:
                    score += len(ls_in) - abs(ls_in.index(init) - ls_mod.index(init)) - i
                    i += 1
            return score


        def rem_singles(file):
            tf = Tree(file)
            td = Tree(file)

            ## make td able to be compared with rf.
            for node in next(td.traverse()):
                node.name = node.name.split("|")[0]
            lst_nodes = [node for node in next(tf.copy().traverse())]
            dict_neighbors = {}
            ## iterate up until you have a list of five or more for each node in the tree
            ## (node.get_leaves has original node in it)

            ti = Tree(currentdir + "/tree.nwk")
            ## MAYBE WE WANT TO PRUNE HERE SO THAT THE LIST OF NEIGHBORS FROM ORIGINAL TREE IS SAME AS PROT TREE WHICH MIGHT HAVE MISSING GENOMES.???

            ti.prune(list(map(lambda str: str.name.split("|")[0], lst_nodes)))
            rf, maxrf, get, y, a, x, z = ti.robinson_foulds(td, unrooted_trees=True)
            maxrf = maxrf + .0001
            rdist = rf / maxrf
            num_nei = round(len(lst_nodes) * (1 - rdist))
            total_score = num_nei ** 2
            cutoff = total_score / 15

            for node in lst_nodes:
                ori_leaf = node
                while len(node.get_leaves()) - 1 < num_nei:
                    node = node.up
                dict_neighbors[ori_leaf.name] = {}
                for node in node.get_leaves():
                    if node.name != ori_leaf.name:
                        ## add all neighbors to dictionary
                        dict_neighbors[ori_leaf.name][node.name] = ori_leaf.get_distance(node.name)
                ## put flag in here for number of neighbors.
                # get closest n neighbors
                dict_neighbors[ori_leaf.name] = sorted(dict_neighbors[ori_leaf.name],
                                                       key=dict_neighbors[ori_leaf.name].get)[:num_nei]
                ## check to see if top five neighbors are the same in species tree for this node,

            ## now we have a dictionary of the closest neighbors for each genome, we do the same for the species tree
            ## and finally compare making a list of leaves to prune from the tree.
            ## IDENTICAL ^^vv

            print("made its to nex")
            lst_nodesi = [node for node in next(ti.copy().traverse())]
            dict_neighborsi = {}
            for nodei in lst_nodesi:
                ori_leafi = nodei
                while len(nodei.get_leaves()) - 1 < num_nei:
                    nodei = nodei.up
                dict_neighborsi[ori_leafi.name] = {}
                for nodei in nodei.get_leaves():
                    if nodei.name != ori_leafi.name:
                        dict_neighborsi[ori_leafi.name][nodei.name] = ori_leafi.get_distance(nodei.name)
                dict_neighborsi[ori_leafi.name] = sorted(dict_neighborsi[ori_leafi.name],
                                                         key=dict_neighborsi[ori_leafi.name].get)[:num_nei]

            flagged = []
            i = 0
            for node in lst_nodes:
                # check if node in refs if it is we skip this step.
                ls_model = list(map(lambda str: str.split("|")[0], [each for each in dict_neighbors[node.name]]))
                ls_init = dict_neighborsi[node.name.split("|")[0]]
                ## checks the two sorted lists to see if they have the same nodes, makes a list.
                score = score_func(ls_model, ls_init)
                if score > cutoff:
                    flagged.append(node)
                else:
                    i += 1
                    with open(currentdir + "/removed/" + file.split("/")[-1].split(".")[0].split("_")[-2], 'a') as f:
                        f.write("\n" + "%s\n" % ("sin" + node.name))

            with open(currentdir + "/removed/" + file.split("/")[-1].split(".")[0].split("_")[-2], 'a') as f:
                f.write("\n" + str(i) + "/" + str(len(lst_nodes)) + " " + str(rdist))

            ## flagged is the list of nodes we want to keep.
            flagged = list(map(lambda x: x.name, flagged))
            t_prot = tf.copy()
            t_prot.prune(flagged)
            t_prot.write(format=1,
                         outfile=currentdir + "/protTrees/no_singles/" + file.split("/")[-1].split(".")[0] + ".nw")


        ## OPTION: parralellize this.
        if str(args.singles) == "yes":
            #             for file in files:
            #                 print(file)
            #                 rem_singles(file)

            try:
                pool = mp.Pool(num_cpus)
                pool.map(rem_singles, [file for file in files])
                pool.close()
                pool.join()
            except:
                print("ERROR for marker selection:", sys.exc_info()[0])
                raise

        Fastree_runtime = time.time() - Fastree_datetime
        print("Marker selection runtime", Fastree_runtime)

        ## WRITE LOGFILE
        logfile_dir = currentdir + "/logfile_"
        logfile = logfile_dir + str(start_time) + ".txt"

        ## ADDED
        try:
            with open(logfile, "w") as myfile:
                myfile.write(currentdir + "\n" + ("=" * 80) + "\n"
                             + "Sg_Tree v.2" + "\n" + "start time: " + start_time)
                myfile.write(str(ran_trimal_time) + "- ...running trimal v.?")
                myfile.write("\n" + "trimming done - runtime: "
                             + str(trimal_runtime)
                             + " seconds"
                             + "\n" + ("=" * 80) + "\n")
                myfile.write(str(ran_Fastree_time) + "- ...running FastTree v.")
                # TO DO: update versions somehow?
                myfile.write("\n" + "Marker selection - total runtime: "
                             + str(Fastree_runtime)
                             + " seconds"
                             + "\n" + ("=" * 80) + "\n")
                myfile.write("Sgtree endtime: " + "\n"
                             + str(datetime.datetime.now())
                             + " seconds"
                             + "\n" + start_time
                             + "\n" + str(datetime.datetime.now()))
        except FileExistsError:
            print("Unexpected error creating log file", sys.exc_info())
        except:
            print("Unknown Error for logfile", sys.exc_info())
    except Exception as e:
        print("ERROR FOR WRITING STDOUT OF SGTREE_PIPE fin.py", e.__doc__, "\n", str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    try:
        ## if were doing single marker selection we make set the newick dir to be the singles dir else just the regular.
        if str(args.singles) == "yes":
            newick_dir = currentdir + "/protTrees/no_singles/*"
        else:
            newick_dir = currentdir + "/protTrees/no_duplicates/out/*"

        aligned_dir = currentdir + "/aligned"

        cmd_mk_trdir = ["mkdir", "-p", currentdir + "/aligned_final"]
        mk_dir = subprocess.run(cmd_mk_trdir, stdout=subprocess.PIPE)
        aligned_final_dir = currentdir + "/aligned_final"


        def write_outs_to_aln(file):
            """takes output from sgtree_fin in the no_duplicates/out folder and writes it to aligned final"""
            t = Tree(file)
            lst_nodes = [node.name for node in t.traverse("postorder")]
            # print("LST OF NODES", lst_nodes)
            print(aligned_dir + "/" + file.split("/")[-1].split("_")[3] + ".faa")
            with open(aligned_dir + "/" + file.split("/")[-1].split("_")[3] + ".faa", "r+") as myfile:
                record_dict = SeqIO.to_dict(SeqIO.parse(myfile, "fasta"))
                for key in record_dict.copy().keys():
                    # print(key)
                    if key not in lst_nodes:
                        # print("FOUDN BAD KEY", key)
                        del record_dict[key]
                # print(record_dict.keys())
                for k, v in record_dict.items():
                    with open(aligned_final_dir + "/" + file.split("/")[-1].split("_")[3] + ".faa",
                              'a') as output_handle:
                        SeqIO.write(record_dict[k], output_handle, "fasta")


        ### Apply write_outs to every file in no_dups/out
        ls_of_files = glob.glob(newick_dir, recursive=True)
        print("nodups/out", ls_of_files)
        print(newick_dir)
        pool = mp.Pool(num_cpus)
        pool.map(write_outs_to_aln, [file for file in ls_of_files])
        pool.close()
        pool.join()

        #####################################################
        # TRIMAL
        ran_trimal_time = datetime.datetime.now()
        trimal_datetime = time.time()

        cmd_mk_trdir = ["mkdir", "-p", currentdir + "/trimmed_final"]
        mk_dir = subprocess.run(cmd_mk_trdir, stdout=subprocess.PIPE)
        trimmed_final_dir = currentdir + "/trimmed_final"


        def run_trimal(file):
            """
            takes a file and runs trimal on it, saving the output into a corresponding filename in trimmed_ProtTrees
            """
            print("Running trimal on FILE:", file)
            try:
                with open(file, "r") as myfile:
                    destination_file = trimmed_final_dir + "/" + file.split("/")[-1]
                    cmd_run_trimal = ["trimal", "-in", file, "-out", destination_file, "-gt", "0.1"]
                    capture_trimal = subprocess.run(cmd_run_trimal, stdout=subprocess.PIPE)
            except:
                print("Unexpected error for trimal:", sys.exc_info()[0])
                raise


        ## run trimal on every file in aligned (with duplicates in it)
        ran_trimal_time = datetime.datetime.now()
        trimal_datetime = time.time()

        ls_of_files = glob.glob(aligned_final_dir + "/*", recursive=True)
        pool = mp.Pool(num_cpus)
        pool.map(run_trimal, [file for file in ls_of_files])
        pool.close()
        pool.join()

        trimal_runtime = time.time() - trimal_datetime
        print("trimal runtime", trimal_runtime)
        print(ls_of_files)

        #####################################################
        ran_concat_time = datetime.datetime.now()
        concat_datetime = time.time()


        def trimmed_to_df():
            """
            takes files in the trimmed directory and puts them all in a table for replacement of NaNs.
            """
            try:
                df_conc = pd.DataFrame(columns=['SeqID'])
                for file in glob.glob(trimmed_final_dir + "/*", recursive=True):
                    record_dict = SeqIO.to_dict(SeqIO.parse(file, "fasta"))
                    record_dict = {k: v.format("fasta").split("\n", 1)[1] for k, v in record_dict.items()}
                    new_dict = dict()
                    for key in record_dict.keys():
                        new_dict[key.split("|")[0]] = record_dict[key]
                        new_df = pd.DataFrame(list(new_dict.items()), columns=['SeqID', file.split("/")[-1]])
                    df_conc = pd.merge(new_df, df_conc, how='outer')
                return df_conc
            except:
                print("Unexpected error for production of initial df in concat:", sys.exc_info()[0])


        df_conc = trimmed_to_df()



        def rem_NaN():
            """
            takes a cell in the table if its none, replace it with right number of X, else replace the "\n".
            cannot be fully parralellized because needs to remember len_string.
            """
            try:
                for j in range(1, df_conc.shape[1]):
                    len_string = 0
                    for i in range(0, df_conc.shape[0]):
                        if isinstance(df_conc.loc[i][j], float):
                            if len_string == 0:
                                x = "this better be the first row otherwise this breaks."
                                # print(i,j,x)
                            else:
                                df_conc.loc[i].iat[j] = "X" * (len_string)
                                # df.set_value(i, i, "X" * (len_string))
                                # print("FOUND AND REPLACED", i, j, df_conc.loc[i][j])
                        else:
                            len_string = len(df_conc.loc[i][j].replace("\n", ""))
            except:
                print("Unexpected error for production df_concatenated, rem_NaN", sys.exc_info()[0])


        ## run rem NaN on every cell in the table.
        rem_NaN()


        def rem_rest():
            """
            replaces for first and last lines, which are not considered in the first round.
            """
            try:
                for index in range(1, df_conc.shape[1]):
                    if isinstance(df_conc.loc[0][index], float):
                        count = 0
                        for i in range(1, len(df_conc.index)):
                            if not (isinstance(df_conc.loc[count][index], float)):
                                break
                            else:
                                df_conc.loc[count].iat[index] = "X" * len(
                                    df_conc.loc[len(df_conc.index) - 1][index].replace("\n", ""))
                                count += 1
            except:
                print("Unexpected error for production df_concatenated, rem_rest", sys.exc_info()[0])


        ## run rem_rest on every column for important indicies.
        rem_rest()

        try:
            df_conc.to_csv(currentdir + "/tables/table_df_concatenated_w_X_final")
        except:
            print("Cant write table")

        ## make directory for final concat
        cmd_mk_concdir = ["mkdir", "-p", currentdir + "/concat_final"]
        mk_dir = subprocess.run(cmd_mk_concdir, stdout=subprocess.PIPE)
        concat_dir = currentdir + "/concat_final/concatenated.faa"

        ## make record dict for concat
        df_conc = pd.read_csv(currentdir + "/tables/table_df_concatenated_w_X_final")
        df_conc = df_conc.set_index('SeqID')
        record_dict = df_conc.T.to_dict('list')
        record_dict = {k: v[1::] for k, v in record_dict.items()}
        record_dict = {k: ''.join(v) for k, v in record_dict.items()}
        record_dict = {k: v.replace("\n", "") for k, v in record_dict.items()}

        ## write final concat
        with open(concat_dir, "w") as myfile:
            for k, v in record_dict.items():
                myfile.write(">" + k + "\n" + v + "\n")

        concat_runtime = time.time() - concat_datetime
        print("concat runtime", concat_runtime)

        #####

        color_dict = {}
        try:
            with open(currentdir + "/color.txt") as f:
                content = f.readlines()
                for each in content[6:]:
                    color_dict[each.split(" ")[0]] = each.split(" ")[1].replace("\n", "")
        except:
            print("ERROR creating colordict")


        def add_branchcolor(node):
            if node.is_leaf():
                if node.name in color_dict:
                    color = color_dict[node.name]
                    taxonNode = faces.TextFace(node.name, fgcolor=color_dict[node.name], fsize=10, fstyle='bold')
                    faces.add_face_to_node(taxonNode, node, 1)
                node.img_style["fgcolor"] = color
                node.img_style["vt_line_color"] = color
                node.img_style["hz_line_color"] = color


        ###############
        # FASTREE
        ran_Fastree_time = datetime.datetime.now()
        Fastree_datetime = time.time()

        try:
            concat_dir = currentdir + "/concat_final/concatenated.faa"
            tree_dir = currentdir + "/" + "tree_final.nwk"
            cmd_runFastree = ["FastTree", "-out", tree_dir, concat_dir]
            FastTree_result = subprocess.run(cmd_runFastree, stdout=subprocess.PIPE)
        except:
            print("Unexpected error for Fastree no duplicates:", sys.exc_info()[0])
            raise

        Fastree_runtime = time.time() - Fastree_datetime
        print("we made it here")

        tfin = Tree(currentdir + "/tree_final.nwk")
        tfin.dist = 0
        tfin.allow_face_overlap = True
        ts = TreeStyle()
        ts.mode = 'r'
        ts.min_leaf_separation = 0
        ts.layout_fn = add_branchcolor
        tfin.set_outgroup(tfin.get_midpoint_outgroup())

        tfin.render(currentdir + "/tree_final.png", w=183, units="mm", tree_style=ts)
        #################

        if args.ref != None:
            for file in glob.glob(currentdir + "/*", recursive=True):
                if file.split("/")[-1].split(".")[-1] == "txt":
                    print("NO ZIP", file)
                    continue
                if file.split("/")[-1].split(".")[-1] == "png":
                    print("NO ZIP", file)
                    continue
                if file.split("/")[-1].split("_")[0] == "logfile":
                    print("NO ZIP", file)
                    continue
                if file.split("/")[-1] == "aligned_final":
                    print("NO ZIP", file)
                    continue
                if file.split("/")[-1] == "concat_final":
                    print("NO ZIP", file)
                    continue
                if file.split("/")[-1] == "tree_final.nwk":
                    print("NO ZIP", file)
                    continue
                elif True:
                    print("ZIPPING", file)
                    if os.path.isdir(file):
                        subprocess.run(['zip', file] + glob.glob(file + "/*"))
                        shutil.rmtree(file)
                    else:
                        with zipfile.ZipFile(file, 'w') as myzip:
                            myzip.write(file)
                            myzip.close()

    except Exception as e:
        print("ERROR FOR WRITING STDOUT OF SGTREE_PIPE gen.py", e.__doc__, "\n", str(e))
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

orig_stdout = sys.stdout
f = open(currentdir + '/BG_out.txt', 'w')
sys.stdout = f

print("START:", start_time, "END", str(datetime.datetime.now()))

sys.stdout = orig_stdout
f.close()

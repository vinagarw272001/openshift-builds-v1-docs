# This script processes the output of an asciibinder or asciidoctor run
# It expects this output in the "out" file
# This script finds the "not found" lines and so detects which files are not found
# It then creates an actions.sh file to copy the files from your openshift-docs repo directory

# The script is specific to openshift-docs structure: it expects the files to be
#   only one subdirectory deep

# To use this script with asciibinder:
# 1. ensure that you already have the _topic_maps/_topic_map.yaml file only includes your assemblies
# 2. ensure all these assembly files are already present in your repo
# 3. place this file in the root directory of your repo
# 4. run:
#    $ asciibinder build
# 5. see the references to files being not found.
#      If the build succeeds with no fles "not found", you are done!
#      If you are done, you can view yor build results in _preview
# 6. run the build again, saving the output to a file named "out":
#    $ asciibinder build >out 2>&1
# 7. run this script:
#    $ python process-out.py
# 8. run the actions.sh file that this script created (you can, of course, view the file first):
#     $ bash actions.sh
# 9. repeat from step 4, until the build succeeds with no files "not found"

# NOTE: If two build results are the same, soemthing is not working right.
#    In this case, check that the images, modules, and snippets directories exist

# The location of your openshift-docs repository
# You should have the main branch checked out and pulled
openshift_doc_repo="/home/vinagarw/Documents/shipwright/openshift-docs/"

import os.path

errlines=open("out").readlines()
actions=open("actions.sh","w")

for line in errlines:
    if line.find("not found")==-1:
        continue

    # find the file name
    (head,fname)=os.path.split(line.split()[-1])

    # record the directory, which should be modules/snippets/images
    (head,fdir)=os.path.split(head)


    fpathname=os.path.join(fdir,fname)
    action="cp "+os.path.join(openshift_doc_repo,fpathname)+" "+fdir+"\n"
    actions.write(action)

actions.close()


# spare code in case we need to add processing subdirectories

#    fdir=""
#    fdir_added=""
#    while not fdir_added in ["modules","snippets","images","_attributes"]:
#        if head=="": # this should never happen...
#            print("Expected directory name not found for line: ")
#            print(line)
#            exit(1)
#        (head,fdir_added)=os.path.split(head)
#        fdir=os.path.join(fdir_added,fdir)
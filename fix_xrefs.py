# This script fixes xrefs when splitting a repo out from openshift-docs

# This script assumes that the product was one directory originally
# The internal product links are all replaces with a single new product directory
# This means you will need to do additional work when restructuring
# However, all the links *outside* the product get converted to hard links to d.o.c

# To use this script:
# 1. Place this script in the root directory of the repo
# 2. review and edit the settings below
# 3. run the script:
#    $ python fix_xrefs.py

# Only the files where any xrefs are changed are "touched",
#    so you can see which files were changed by the modify timestamp

# The directories in which the asciidoc files should be processed
# Do not add _attributes and snippets
# Do not add modules since modules are not allowed to have xrefs in the OCP repo
# (check them for xrefs manually anyway by a full text search for xref just in modules)
# DO NOT REMOVE THE SQUARE BRACKETS, this is a list even if it only has one member
directories_to_process = ["pipelines"]

# The full reference to the directory of the product,
#    with the starting .. part and the trailing /
# xrefs with this reference will be converted to new internal xrefs
# for pipelines it is "../../cicd/pipelines"
ref_to_product_directory = "../../cicd/pipelines"

# Tne new reference to the directory of the product, to replace the old one
new_ref_to_product_directory = "../pipelines"

# The reference to the top directory of the repo, with the trailing /
# for pipelines it is "../../" because pipelines is under cicd/pipelines
# xrefs that do not have the product directlry but have this reference will
#   be converted to links to docs.openshift.com
ref_to_top_directory = "../../"

# The root part of the links to docs.openshift.com
root_link = "https://docs.openshift.com/container-platform/latest/"

import os
for dir in directories_to_process:
    for entry in os.scandir(dir):
        if entry.is_dir():
            continue
        fname=entry.path
        if fname.find(".adoc")<0:
            continue

        # load the file's entire content
        content=open(fname).read()
        # accumulator for processed content
        content_processed=""
        # marker that the content was changed
        content_changed=False

        # find the first xref
        xref_pos=content.find("xref:")
        while xref_pos >= 0:
            # move everything before the xref to processed
            content_processed+=content[:xref_pos]
            content=content[xref_pos:]

            # find the next [ and the next newline

            bracket=content.find("[")
            new_line=content.find("\n")

            # if the [ was not found or comes after the newline, this is not a valid xref
            # in this case we output a warning
            if (bracket<0) or (new_line>0 and new_line<bracket):
                print ("In file: "+fname)
                print ("Invalid xref:")
                if new_line>0: # if there is a newline, the invalid xref ends there
                    print(content[:new_line])
                    content_processed+=content[:new_line]
                    content=content[new_line:]
                else: # if there is no newline, the invalid xref is the entire remaining content
                    print(content)
                    content_processed+=content
                    content=""
                print()

                # find the next xref
                xref_pos=content.find("xref:")
                continue

            xref_text=content[:bracket]
            content=content[bracket:]

            # check if this xref refers to the same product
            if xref_text.find(ref_to_product_directory)>0:
                content_changed=True
                xref_text=xref_text.replace(ref_to_product_directory,new_ref_to_product_directory)
            elif xref_text.find(ref_to_top_directory)>0:
                content_changed=True
                xref_text=xref_text.replace("xref:","link:").replace(ref_to_top_directory,root_link).replace(".adoc",".html")
            else:
                print ("In file: "+fname)
                print ("xref not leading to product or top directory:")
                print(xref_text)
                print()

            content_processed+=xref_text

            # find the next xref
            xref_pos=content.find("xref:")

        # as the loop has ended, there are no more xrefs remaining
        # we add the remaining content to the processed content to get the full new content
        content_processed+=content

        if content_changed:
            # rewrite the file with the new content
            of=open(fname,"w")
            of.write(content_processed)
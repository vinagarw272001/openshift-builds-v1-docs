# This script finds all attributes in a set of ADOC files
# Actually, it finds things that look like attributes, as in {something}
# So, of course, other things in curly brackets become false positives

# The script outputs the list to a file named attribute_list
# Every attribute (or not-really-attribute) is listed only once

# The script takes no parameters. To use this script:

# 1. Place this file into the root directory of your repository
# 2. Edit the list of directories a few lines below. Note: DO NOT add the _attributes directory
# 3. Run the script:
#     $ python find_attributes.py
# 4. Enjoy your attribute_list file  

import os
attrs=set()

# replace "pipelines" with one or more directories with ADOC files to scan
# you can use / to list directories inside directories
# Note that the code does NOT recurse into subdirectories
for dir in ["modules","snippets","builds"]:
    for entry in os.scandir(dir):
        if entry.is_dir():
            continue
        fname=entry.path
        if fname.find(".adoc")<0:
            continue

        print(fname)

        # load the file's entire content
        content=open(fname).read()

        # find the first {
        open_curly_bracket=content.find("{")
        while open_curly_bracket >= 0:
            # trim the content before the { and the { itself
            content=content[open_curly_bracket+1:]

            # find the next \n and the next }
            close_curly_bracket=content.find("}")
            new_line=content.find("\n")

            # if the next } is simply not found, end processing this file
            if close_curly_bracket==-1:
                break

            # if the next newline is found and is closer than the next }, this is not an attribute
            # just find the next { and go on
            if (new_line>=0) and (new_line<close_curly_bracket):
                open_curly_bracket=content.find("{")
                continue

            # attribute is likely found
            attr=content[:close_curly_bracket]
            # screen for some false positives found in YAML etc
            if not ((" " in attr) or (":" in attr) or ("{" in attr) or ("\\" in attr)
                    or ("<" in attr) or ("." in attr)):
                attrs.add(attr)

            # find the next { and continue
            open_curly_bracket=content.find("{")

# write out the attributes
of=open("attribute_list","w")
for attr in attrs:
    of.write(attr+"\n")
of.close()
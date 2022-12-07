grep -E "s__|clade" merged_abundance_table.txt | sed 's/^.*s__//g' | cut -f1,3-8 | sed -e 's/clade_name/body_site/g' > merged_abundance_table_species.txt
